// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Common {
    uint256 number;

    function reachabilitySuccess() public {
        number++;
    }

    function reachabilityFail() public {
        revert("Always fails");
    }
}
