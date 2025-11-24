// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Pausable} from "@openzeppelin-contracts-5.5.0/utils/Pausable.sol";

contract PausableHarness is Pausable {
    function pause() external {
        _pause();
    }

    function unpause() external {
        _unpause();
    }

    function onlyWhenPaused() external whenPaused {}

    function onlyWhenNotPaused() external whenNotPaused {}
}