// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin-contracts-5.4.0/token/ERC20/ERC20.sol";

contract ERC20Harness is ERC20 {
    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}
}
