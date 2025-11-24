# certora-universal

Universal set of certora rules.

## Protocol categories
1. Common (applied to all types of protocols), catches:
  - reachability (all methods have a none reverting path)
2. OpenZeppelin

## Outputs
| Category | Instance | Command | Output |
|---|---|---|---|
| Common | - | `certoraRun src/common/certora/Common.conf` | [Output](https://prover.certora.com/output/8691664/426d12fa3fc24c859286d34cf723b2e4/?anonymousKey=12e7693b3fe3e6427a0f15007c4b0a610c32983a) |
| OpenZeppelin | AccessControl | `certoraRun src/openzeppelin/AccessControl/certora/AccessControlHarness.conf` | [Output](https://prover.certora.com/output/8691664/0af885939fe7424cbdcd38f112219129/?anonymousKey=1bf2ca2797bfce020df686f8bd9a2ea729a64d65) |
| OpenZeppelin | AccessControlDefaultAdminRules | `certoraRun src/openzeppelin/AccessControlDefaultAdminRules/certora/AccessControlDefaultAdminRulesHarness.conf` | [Output](https://prover.certora.com/output/8691664/39eaad36e249489ea910dcb437bb0071/?anonymousKey=b9d593862d36d7a31311ae346374ef9a6a4b07ff) |
| OpenZeppelin | AccessManaged | `certoraRun src/openzeppelin/AccessManaged/certora/AccessManagedHarness.conf` | [Output](https://prover.certora.com/output/8691664/7ff398ecfedb41298eeea0dec8393251/?anonymousKey=144a8ea022717b9cfbbb7d6dd2430908a1e23ab2) |
| OpenZeppelin | AccessManager | `certoraRun src/openzeppelin/AccessManager/certora/AccessManagerHarness.conf` | [Output](https://prover.certora.com/output/8691664/56a69f7efcce411ebe078fe6fd318bed/?anonymousKey=69882e17dba7d161e8c3ddba3f84e6f3b6e4c931) |
| OpenZeppelin | Account | `certoraRun src/openzeppelin/Account/certora/AccountHarness.conf` | [Output](https://prover.certora.com/output/8691664/ee6aae5d262945e8806f07eeccc6e272/?anonymousKey=38d5c01de79bd8a520d6712dde3655c1eab60f2b) |
| OpenZeppelin | ERC20 | `certoraRun src/openzeppelin/ERC20/certora/ERC20Harness.conf` | [Output](https://prover.certora.com/output/8691664/ddfd6ba876e24559bdb4ea989b74cfeb/?anonymousKey=33254d36e1e59c4e7f9ed9f65efcf500fa22e44a) |
