// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import { ERC20Mock } from "@openzeppelin-contracts-5.5.0/mocks/token/ERC20Mock.sol";
import { Test, console } from "forge-std/Test.sol";
import { ERC4626Harness } from "../../..//src/defi/ERC4626/harnesses/ERC4626Harness.sol";

contract ERC4624Test is Test {
    ERC20Mock token;
    ERC4626Harness vault;

    address user = makeAddr("user");
    address user2 = makeAddr("user2");

    function setUp() public {
        token = new ERC20Mock();
        vault = new ERC4626Harness(address(token));

        token.mint(user, 100 ether);
        token.mint(user2, 100 ether);

        vm.prank(user);
        token.approve(address(vault), type(uint256).max);

        vm.prank(user2);
        token.approve(address(vault), type(uint256).max);
    }

    function testERC4626() public {
        // deposit
        vm.prank(user);
        vault.deposit(100 ether, user);

        // redeem
        vm.prank(user);
        vault.redeem(100 ether, user, user);

        console.log("Token balance (user):", token.balanceOf(user));
        console.log("Shares balance (user):", vault.balanceOf(user));
    }
}
