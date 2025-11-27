// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CommonFail {
    //================
    // Reachability
    //================

    function reachability() public {
        revert("Always fails");
    }
}
