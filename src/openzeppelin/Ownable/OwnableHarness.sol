// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "@openzeppelin-contracts-5.5.0/access/Ownable.sol";

contract OwnableHarness is Ownable {
    constructor(address initialOwner) Ownable(initialOwner) {}

    function restricted() external onlyOwner {}
}
