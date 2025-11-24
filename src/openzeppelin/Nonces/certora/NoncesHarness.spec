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
    function nonces(address) external returns (uint256) envfree;
    function useNonce(address) external returns (uint256) envfree;
    function useCheckedNonce(address,uint256) external envfree;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Helpers                                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
function nonceSanity(address account) returns bool {
    return nonces(account) < max_uint256;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Function correctness: useNonce uses nonce                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule useNonce(address account) {
    require nonceSanity(account);

    address other;

    mathint nonceBefore = nonces(account);
    mathint otherNonceBefore = nonces(other);

    mathint nonceUsed = useNonce@withrevert(account);
    bool success = !lastReverted;

    mathint nonceAfter = nonces(account);
    mathint otherNonceAfter = nonces(other);

    // liveness
    assert success, "doesn't revert";

    // effect
    assert nonceAfter == nonceBefore + 1 && nonceBefore == nonceUsed, "nonce is used";

    // no side effect
    assert otherNonceBefore != otherNonceAfter => other == account, "no other nonce is used";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Function correctness: useCheckedNonce uses only the current nonce                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule useCheckedNonce(address account, uint256 currentNonce) {
    require nonceSanity(account);

    address other;

    mathint nonceBefore = nonces(account);
    mathint otherNonceBefore = nonces(other);

    useCheckedNonce@withrevert(account, currentNonce);
    bool success = !lastReverted;

    mathint nonceAfter = nonces(account);
    mathint otherNonceAfter = nonces(other);

    // liveness
    assert success <=> to_mathint(currentNonce) == nonceBefore, "works iff current nonce is correct";

    // effect
    assert success => nonceAfter == nonceBefore + 1, "nonce is used";

    // no side effect
    assert otherNonceBefore != otherNonceAfter => other == account, "no other nonce is used";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: nonce only increments                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule nonceOnlyIncrements(address account) {
    require nonceSanity(account);

    mathint nonceBefore = nonces(account);

    env e; method f; calldataarg args;
    f(e, args);

    mathint nonceAfter = nonces(account);

    assert nonceAfter == nonceBefore || nonceAfter == nonceBefore + 1, "nonce only increments";
}