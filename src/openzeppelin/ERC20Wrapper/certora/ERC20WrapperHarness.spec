using ERC20Harness as underlying;

//===========
// Helpers
//===========

// environment
definition nonzero(address account) returns bool = account != 0;
definition nonpayable(env e) returns bool = e.msg.value == 0;
definition nonzerosender(env e) returns bool = nonzero(e.msg.sender);
definition sanity(env e) returns bool = clock(e) > 0 && clock(e) <= max_uint48;

// math
definition min(mathint a, mathint b) returns mathint = a < b ? a : b;
definition max(mathint a, mathint b) returns mathint = a > b ? a : b;

// time
definition clock(env e) returns mathint = to_mathint(e.block.timestamp);
definition isSetAndPast(env e, uint48 timepoint) returns bool = timepoint != 0 && to_mathint(timepoint) <= clock(e);

//========
// Core
//========

methods {
    // ERC20
    function name()                                external returns (string)  envfree;
    function symbol()                              external returns (string)  envfree;
    function decimals()                            external returns (uint8)   envfree;
    function totalSupply()                         external returns (uint256) envfree;
    function balanceOf(address)                    external returns (uint256) envfree;
    function allowance(address,address)            external returns (uint256) envfree;
    function approve(address,uint256)              external returns (bool);
    function transfer(address,uint256)             external returns (bool);
    function transferFrom(address,address,uint256) external returns (bool);
    // ERC2612
    function permit(address,address,uint256,uint256,uint8,bytes32,bytes32) external;
    function nonces(address)    external returns (uint256) envfree;
    function DOMAIN_SEPARATOR() external returns (bytes32) envfree;
    // ERC20Wrapper
    function underlying()                          external returns(address) envfree;
    function depositFor(address, uint256)          external returns(bool);
    function withdrawTo(address, uint256)          external returns(bool);
    function recover(address)                      external returns(uint256);

    function underlying.totalSupply()              external returns (uint256) envfree;
    function underlying.balanceOf(address)         external returns (uint256) envfree;
    function underlying.allowance(address,address) external returns (uint256) envfree;

    unresolved external in _._ => DISPATCH(optimistic=true) [
        underlying.transferFrom(address, address, uint256),
        underlying.transfer(address, uint256)
    ];
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Helper: consequence of `totalSupplyIsSumOfBalances` applied to underlying                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
definition sumOfUnderlyingBalancesLowerThanUnderlyingSupply(address a, address b) returns bool =
    a != b => underlying.balanceOf(a) + underlying.balanceOf(b) <= to_mathint(underlying.totalSupply());

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Invariant: total supply is sum of balances                                       
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sload uint256 balance _balances[KEY address addr] {
    require sumOfBalances >= balance;
}

hook Sstore _balances[KEY address addr] uint256 newValue (uint256 oldValue) {
    sumOfBalances = sumOfBalances - oldValue + newValue;
}

invariant totalSupplyIsSumOfBalances()
    totalSupply() == sumOfBalances;

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Invariant: wrapped token should not allow any third party to spend its tokens                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
invariant noAllowance(address user)
    underlying.allowance(currentContract, user) == 0
    {
        preserved ERC20Harness.approve(address spender, uint256 value) with (env e) {
            require e.msg.sender != currentContract;
        }
        preserved ERC20Harness.permit(address owner, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) with (env e) {
            require owner != currentContract;
        }
    }

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Invariant: wrapped token can't be undercollateralized (solvency of the wrapper)                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
invariant totalSupplyIsSmallerThanUnderlyingBalance()
    totalSupply() <= underlying.balanceOf(currentContract) &&
    underlying.balanceOf(currentContract) <= underlying.totalSupply() &&
    underlying.totalSupply() <= max_uint256
    {
        preserved with (env e) {
            requireInvariant totalSupplyIsSumOfBalances;
            require e.msg.sender != currentContract;
            require sumOfUnderlyingBalancesLowerThanUnderlyingSupply(e.msg.sender, currentContract);
        }
        preserved ERC20Harness.transferFrom(address from, address to, uint256 amount) with (env e) {
            requireInvariant noAllowance(e.msg.sender);
            require sumOfUnderlyingBalancesLowerThanUnderlyingSupply(from, to);
        }
        preserved ERC20Harness.burn(address from, uint256 amount) with (env e) {
            // If someone can burn from the wrapper, than the invariant obviously doesn't hold.
            require from != currentContract;
            require sumOfUnderlyingBalancesLowerThanUnderlyingSupply(from, currentContract);
        }
    }

rule noSelfWrap() {
    assert currentContract != underlying();
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: depositFor liveness and effects                                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule depositFor(env e) {
    require nonpayable(e);

    address sender = e.msg.sender;
    address receiver;
    address other;
    uint256 amount;

    // sanity
    require currentContract != underlying();
    requireInvariant totalSupplyIsSumOfBalances;
    requireInvariant totalSupplyIsSmallerThanUnderlyingBalance;
    require sumOfUnderlyingBalancesLowerThanUnderlyingSupply(currentContract, sender);

    uint256 balanceBefore                   = balanceOf(receiver);
    uint256 supplyBefore                    = totalSupply();
    uint256 senderUnderlyingBalanceBefore   = underlying.balanceOf(sender);
    uint256 senderUnderlyingAllowanceBefore = underlying.allowance(sender, currentContract);
    uint256 wrapperUnderlyingBalanceBefore  = underlying.balanceOf(currentContract);
    uint256 underlyingSupplyBefore          = underlying.totalSupply();

    uint256 otherBalanceBefore              = balanceOf(other);
    uint256 otherUnderlyingBalanceBefore    = underlying.balanceOf(other);

    depositFor@withrevert(e, receiver, amount);
    bool success = !lastReverted;

    // liveness
    assert success <=> (
        sender   != currentContract               && // invalid sender
        sender   != 0                             && // invalid sender
        receiver != currentContract               && // invalid receiver
        receiver != 0                             && // invalid receiver
        amount   <= senderUnderlyingBalanceBefore && // deposit doesn't exceed balance
        amount   <= senderUnderlyingAllowanceBefore  // deposit doesn't exceed allowance
    );

    // effects
    assert success => (
        to_mathint(balanceOf(receiver)) == balanceBefore + amount &&
        to_mathint(totalSupply()) == supplyBefore + amount &&
        to_mathint(underlying.balanceOf(currentContract)) == wrapperUnderlyingBalanceBefore + amount &&
        to_mathint(underlying.balanceOf(sender)) == senderUnderlyingBalanceBefore - amount
    );

    // no side effect
    assert underlying.totalSupply() == underlyingSupplyBefore;
    assert balanceOf(other)           != otherBalanceBefore           => other == receiver;
    assert underlying.balanceOf(other) != otherUnderlyingBalanceBefore => (other == sender || other == currentContract);
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: withdrawTo liveness and effects                                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule withdrawTo(env e) {
    require nonpayable(e);

    address sender = e.msg.sender;
    address receiver;
    address other;
    uint256 amount;

    // sanity
    require currentContract != underlying();
    requireInvariant totalSupplyIsSumOfBalances;
    requireInvariant totalSupplyIsSmallerThanUnderlyingBalance;
    require sumOfUnderlyingBalancesLowerThanUnderlyingSupply(currentContract, receiver);

    uint256 balanceBefore                   = balanceOf(sender);
    uint256 supplyBefore                    = totalSupply();
    uint256 receiverUnderlyingBalanceBefore = underlying.balanceOf(receiver);
    uint256 wrapperUnderlyingBalanceBefore  = underlying.balanceOf(currentContract);
    uint256 underlyingSupplyBefore          = underlying.totalSupply();

    uint256 otherBalanceBefore              = balanceOf(other);
    uint256 otherUnderlyingBalanceBefore    = underlying.balanceOf(other);

    withdrawTo@withrevert(e, receiver, amount);
    bool success = !lastReverted;

    // liveness
    assert success <=> (
        sender   != 0               && // invalid sender
        receiver != currentContract && // invalid receiver
        receiver != 0               && // invalid receiver
        amount   <= balanceBefore      // withdraw doesn't exceed balance
    );

    // effects
    assert success => (
        to_mathint(balanceOf(sender)) == balanceBefore - amount &&
        to_mathint(totalSupply()) == supplyBefore - amount &&
        to_mathint(underlying.balanceOf(currentContract)) == wrapperUnderlyingBalanceBefore - (currentContract != receiver ? amount : 0) &&
        to_mathint(underlying.balanceOf(receiver)) == receiverUnderlyingBalanceBefore + (currentContract != receiver ? amount : 0)
    );

    // no side effect
    assert underlying.totalSupply() == underlyingSupplyBefore;
    assert balanceOf(other)           != otherBalanceBefore           => other == sender;
    assert underlying.balanceOf(other) != otherUnderlyingBalanceBefore => (other == receiver || other == currentContract);
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: recover liveness and effects                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule recover(env e) {
    require nonpayable(e);

    address receiver;
    address other;

    // sanity
    require currentContract != underlying();
    requireInvariant totalSupplyIsSumOfBalances;
    requireInvariant totalSupplyIsSmallerThanUnderlyingBalance;

    mathint value                        = underlying.balanceOf(currentContract) - totalSupply();
    uint256 supplyBefore                 = totalSupply();
    uint256 balanceBefore                = balanceOf(receiver);

    uint256 otherBalanceBefore           = balanceOf(other);
    uint256 otherUnderlyingBalanceBefore = underlying.balanceOf(other);

    recover@withrevert(e, receiver);
    bool success = !lastReverted;

    // liveness
    assert success <=> receiver != 0;

    // effect
    assert success => (
        to_mathint(balanceOf(receiver)) == balanceBefore + value &&
        to_mathint(totalSupply()) == supplyBefore + value &&
        totalSupply() == underlying.balanceOf(currentContract)
    );

    // no side effect
    assert underlying.balanceOf(other) == otherUnderlyingBalanceBefore;
    assert balanceOf(other) != otherBalanceBefore => other == receiver;
}