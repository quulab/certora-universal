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
    // Ownable2Step
    function owner() external returns (address) envfree;
    function pendingOwner() external returns (address) envfree;
    function transferOwnership(address) external;
    function acceptOwnership() external;
    function renounceOwnership() external;
    // Ownable2StepHarness
    function restricted() external;
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Function correctness: transferOwnership sets the pending owner                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule transferOwnership(env e) {
    require nonpayable(e);

    address newOwner;
    address current = owner();

    transferOwnership@withrevert(e, newOwner);
    bool success = !lastReverted;

    assert success <=> e.msg.sender == current, "unauthorized caller";
    assert success => pendingOwner() == newOwner, "pending owner not set";
    assert success => owner() == current, "current owner changed";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Function correctness: renounceOwnership removes the owner and the pendingOwner                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule renounceOwnership(env e) {
    require nonpayable(e);

    address current = owner();

    renounceOwnership@withrevert(e);
    bool success = !lastReverted;

    assert success <=> e.msg.sender == current, "unauthorized caller";
    assert success => pendingOwner() == 0, "pending owner not cleared";
    assert success => owner() == 0, "owner not cleared";
}

/*
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Function correctness: acceptOwnership changes owner and reset pending owner                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule acceptOwnership(env e) {

    require nonpayable(e);

    address current = owner();
    address pending = pendingOwner();

    acceptOwnership@withrevert(e);
    bool success = !lastReverted;

    assert success <=> e.msg.sender == pending, "unauthorized caller";
    assert success => pendingOwner() == 0, "pending owner not cleared";
    assert success => owner() == pending, "owner not transferred";
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
│ Rule: ownership and pending ownership can only change in specific ways                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
*/
rule ownerOrPendingOwnerChange(env e, method f) {
    address oldCurrent = owner();
    address oldPending = pendingOwner();

    calldataarg args;
    f(e, args);

    address newCurrent = owner();
    address newPending = pendingOwner();

    // If owner changes, must be either acceptOwnership or renounceOwnership
    assert oldCurrent != newCurrent => (
        (e.msg.sender == oldPending && newCurrent == oldPending && newPending == 0 && f.selector == sig:acceptOwnership().selector) ||
        (e.msg.sender == oldCurrent && newCurrent == 0          && newPending == 0 && f.selector == sig:renounceOwnership().selector)
    );

    // If pending changes, must be either acceptance or reset
    assert oldPending != newPending => (
        (e.msg.sender == oldCurrent && newCurrent == oldCurrent &&                    f.selector == sig:transferOwnership(address).selector) ||
        (e.msg.sender == oldPending && newCurrent == oldPending && newPending == 0 && f.selector == sig:acceptOwnership().selector) ||
        (e.msg.sender == oldCurrent && newCurrent == 0          && newPending == 0 && f.selector == sig:renounceOwnership().selector)
    );
}