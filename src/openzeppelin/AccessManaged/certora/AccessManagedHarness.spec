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
    //=================
    // AccessManaged
    //=================
    function authority()              external returns (address) envfree;
    function isConsumingScheduledOp() external returns (bytes4)  envfree;
    function setAuthority(address)    external;

    //================
    // FV
    //================
    function someFunction()                       external;
    function authority_canCall_immediate(address) external returns (bool);
    function authority_canCall_delay(address)     external returns (uint32);
    function authority_getSchedule(address)       external returns (uint48);

    // Summarization for external calls (cause havoc in isConsumingScheduledOpClean invariant):

    // Called by AccessManager.updateAuthority() on target contracts. This modifies
    // the target contract's authority but doesn't affect the AccessManager's _consumingSchedule state.
    function _.setAuthority(address) external => NONDET;

    // Called by AccessManaged._checkCanCall() to consume scheduled operations on the AccessManager.
    // This function should complete successfully and only affect the AccessManager's internal state,
    // not the _consumingSchedule state of the calling AccessManaged contract.
    function _.consumeScheduledOp(address, bytes) external => NONDET;

    // For unresolved external calls (like low-level target.call{value: value}(data))
    // made via Address.functionCallWithValue in AccessManager.execute().
    unresolved external in _._ => DISPATCH [] default NONDET;
}

//==============
// Invariants
//==============

// `isConsumingScheduledOp()` clean
invariant isConsumingScheduledOpClean()
    isConsumingScheduledOp() == to_bytes4(0);

//=============
// Unit
//=============

// `restricted` modifies on `someFunction()` works as expected
rule callRestrictedFunction(env e) {
    bool   immediate      = authority_canCall_immediate(e, e.msg.sender);
    uint32 delay          = authority_canCall_delay(e, e.msg.sender);
    uint48 scheduleBefore = authority_getSchedule(e, e.msg.sender);

    someFunction@withrevert(e);
    bool success = !lastReverted;

    uint48 scheduleAfter  = authority_getSchedule(e, e.msg.sender);

    // can only call if immediate, or (with delay) by consuming a scheduled op
    assert success => (
        immediate ||
        (
            delay > 0 &&
            isSetAndPast(e, scheduleBefore) &&
            scheduleAfter == 0
        )
    );
}
