// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Account} from "@openzeppelin-contracts-5.5.0/account/Account.sol";
import {AccountERC7579Patched} from "./AccountERC7579Patched.sol";
import {SignerEIP7702} from "@openzeppelin-contracts-5.5.0/utils/cryptography/signers/SignerEIP7702.sol";
import {ERC7739} from "@openzeppelin-contracts-5.5.0/utils/cryptography/signers/draft-ERC7739.sol";
import {ERC721Holder} from "@openzeppelin-contracts-5.5.0/token/ERC721/utils/ERC721Holder.sol";
import {ERC1155Holder} from "@openzeppelin-contracts-5.5.0/token/ERC1155/utils/ERC1155Holder.sol";
import {PackedUserOperation} from "@openzeppelin-contracts-5.5.0/interfaces/draft-IERC4337.sol";
import {AbstractSigner} from "@openzeppelin-contracts-5.5.0/utils/cryptography/signers/AbstractSigner.sol";

abstract contract AccountERC7702WithModulesMock is
    Account,
    AccountERC7579Patched,
    SignerEIP7702,
    ERC7739,
    ERC721Holder,
    ERC1155Holder
{
    function _validateUserOp(
        PackedUserOperation calldata userOp,
        bytes32 userOpHash,
        bytes calldata signature
    ) internal virtual override(Account, AccountERC7579Patched) returns (uint256) {
        return super._validateUserOp(userOp, userOpHash, signature);
    }

    /// @dev Resolve implementation of ERC-1271 by both ERC7739 and AccountERC7579 to support both schemes.
    function isValidSignature(
        bytes32 hash,
        bytes calldata signature
    ) public view virtual override(ERC7739, AccountERC7579Patched) returns (bytes4) {
        // ERC-7739 can return the fn selector (success), 0xffffffff (invalid) or 0x77390001 (detection).
        // If the return is 0xffffffff, we fallback to validation using ERC-7579 modules.
        bytes4 erc7739magic = ERC7739.isValidSignature(hash, signature);
        return erc7739magic == bytes4(0xffffffff) ? AccountERC7579Patched.isValidSignature(hash, signature) : erc7739magic;
    }

    /// @dev Enable signature using the ERC-7702 signer.
    function _rawSignatureValidation(
        bytes32 hash,
        bytes calldata signature
    ) internal view virtual override(AbstractSigner, AccountERC7579Patched, SignerEIP7702) returns (bool) {
        return SignerEIP7702._rawSignatureValidation(hash, signature);
    }
}