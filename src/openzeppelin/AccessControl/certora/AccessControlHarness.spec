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
    function DEFAULT_ADMIN_ROLE() external returns (bytes32) envfree;
    function hasRole(bytes32, address) external returns(bool) envfree;
    function getRoleAdmin(bytes32) external returns(bytes32) envfree;
    function grantRole(bytes32, address) external;
    function revokeRole(bytes32, address) external;
    function renounceRole(bytes32, address) external;
}

//==========
// High
//==========

// Only `grantRole()`, `revokeRole()` and `renounceRole()` can alter permissions
rule onlyGrantCanGrant(env e, method f, bytes32 role, address account) {
    calldataarg args;

    bool hasRoleBefore = hasRole(role, account);
    f(e, args);
    bool hasRoleAfter = hasRole(role, account);

    assert (
        !hasRoleBefore &&
        hasRoleAfter
    ) => (
        f.selector == sig:grantRole(bytes32, address).selector
    );

    assert (
        hasRoleBefore &&
        !hasRoleAfter
    ) => (
        f.selector == sig:revokeRole(bytes32, address).selector ||
        f.selector == sig:renounceRole(bytes32, address).selector
    );
}

//==========
// Unit
//==========

// `grantRole()` only affects the specified user/role combo
rule grantRoleEffect(env e, bytes32 role) {
    require nonpayable(e);

    bytes32 otherRole;
    address account;
    address otherAccount;

    bool isCallerAdmin = hasRole(getRoleAdmin(role), e.msg.sender);
    bool hasOtherRoleBefore = hasRole(otherRole, otherAccount);

    grantRole@withrevert(e, role, account);
    bool success = !lastReverted;

    bool hasOtherRoleAfter = hasRole(otherRole, otherAccount);

    // liveness
    assert success <=> isCallerAdmin;

    // effect
    assert success => hasRole(role, account);

    // no side effect
    assert hasOtherRoleBefore != hasOtherRoleAfter => (role == otherRole && account == otherAccount);
}

// `revokeRole()` only affects the specified user/role combo
rule revokeRoleEffect(env e, bytes32 role) {
    require nonpayable(e);

    bytes32 otherRole;
    address account;
    address otherAccount;

    bool isCallerAdmin = hasRole(getRoleAdmin(role), e.msg.sender);
    bool hasOtherRoleBefore = hasRole(otherRole, otherAccount);

    revokeRole@withrevert(e, role, account);
    bool success = !lastReverted;

    bool hasOtherRoleAfter = hasRole(otherRole, otherAccount);

    // liveness
    assert success <=> isCallerAdmin;

    // effect
    assert success => !hasRole(role, account);

    // no side effect
    assert hasOtherRoleBefore != hasOtherRoleAfter => (role == otherRole && account == otherAccount);
}

// `renounceRole()` only affects the specified user/role combo
rule renounceRoleEffect(env e, bytes32 role) {
    require nonpayable(e);

    bytes32 otherRole;
    address account;
    address otherAccount;

    bool hasOtherRoleBefore = hasRole(otherRole, otherAccount);

    renounceRole@withrevert(e, role, account);
    bool success = !lastReverted;

    bool hasOtherRoleAfter = hasRole(otherRole, otherAccount);

    // liveness
    assert success <=> account == e.msg.sender;

    // effect
    assert success => !hasRole(role, account);

    // no side effect
    assert hasOtherRoleBefore != hasOtherRoleAfter => (role == otherRole && account == otherAccount);
}
