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
    // Ownable
    function owner() external returns (address) envfree;
    function transferOwnership(address) external;
    function renounceOwnership() external;
    // OwnableHarness
    function restricted() external;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Function correctness: transferOwnership changes ownership                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule transferOwnership(env e) {
    require nonpayable(e);

    address newOwner;
    address current = owner();

    transferOwnership@withrevert(e, newOwner);
    bool success = !lastReverted;

    assert success <=> (e.msg.sender == current && newOwner != 0), "unauthorized caller or invalid arg";
    assert success => owner() == newOwner, "current owner changed";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Function correctness: renounceOwnership removes the owner                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule renounceOwnership(env e) {
    require nonpayable(e);

    address current = owner();

    renounceOwnership@withrevert(e);
    bool success = !lastReverted;

    assert success <=> e.msg.sender == current, "unauthorized caller";
    assert success => owner() == 0, "owner not cleared";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Access control: only current owner can call restricted functions                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule onlyCurrentOwnerCanCallOnlyOwner(env e) {
    require nonpayable(e);

    address current = owner();

    calldataarg args;
    restricted@withrevert(e, args);

    assert !lastReverted <=> e.msg.sender == current, "access control failed";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Rule: ownership can only change in specific ways                                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule onlyOwnerOrPendingOwnerCanChangeOwnership(env e) {
    address oldCurrent = owner();

    method f; calldataarg args;
    f(e, args);

    address newCurrent = owner();

    // If owner changes, must be either transferOwnership or renounceOwnership
    assert oldCurrent != newCurrent => (
        (e.msg.sender == oldCurrent && newCurrent != 0 && f.selector == sig:transferOwnership(address).selector) ||
        (e.msg.sender == oldCurrent && newCurrent == 0 && f.selector == sig:renounceOwnership().selector)
    );
}