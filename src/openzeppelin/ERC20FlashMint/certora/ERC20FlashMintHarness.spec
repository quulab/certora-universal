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
    // ERC3156FlashLender
    function maxFlashLoan(address)                    external returns (uint256) envfree;
    function flashFee(address,uint256)                external returns (uint256) envfree;
    function flashLoan(address,address,uint256,bytes) external returns (bool);
    // ERC3156FlashBorrower
    function _.onFlashLoan(address,address,uint256,uint256,bytes) external => DISPATCHER(true);
    // ERC20FlashMint
    // non standard ERC-3156 functions
    function flashFeeReceiver() external returns (address) envfree;
    // function summaries below
    function _._update(address from, address to, uint256 amount) internal => specUpdate(from, to, amount) expect void ALL;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Ghost: track mint and burns in the CVL                                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
ghost mapping(address => mathint)                     trackedMintAmount;
ghost mapping(address => mathint)                     trackedBurnAmount;
ghost mapping(address => mapping(address => mathint)) trackedTransferredAmount;

function specUpdate(address from, address to, uint256 amount) {
    if (from == 0 && to == 0) { assert(false); } // defensive

    if (from == 0) {
        trackedMintAmount[to] = amount;
    } else if (to == 0) {
        trackedBurnAmount[from] = amount;
    } else {
        trackedTransferredAmount[from][to] = amount;
    }
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: When doing a flashLoan, "amount" is minted and burnt, additionally, the fee is either burnt                   │
│ (if the fee recipient is 0) or transferred (if the fee recipient is not 0)                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule checkMintAndBurn(env e) {
    address receiver;
    address token;
    uint256 amount;
    bytes data;

    uint256 fees = flashFee(token, amount);
    address recipient = flashFeeReceiver();

    flashLoan(e, receiver, token, amount, data);

    assert trackedMintAmount[receiver] == to_mathint(amount);
    assert trackedBurnAmount[receiver] == amount + to_mathint(recipient == 0 ? fees : 0);
    assert (fees > 0 && recipient != 0) => trackedTransferredAmount[receiver][recipient] == to_mathint(fees);
}