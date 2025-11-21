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
| OpenZeppelin | ERC20 | `certoraRun src/openzeppelin/ERC20/certora/ERC20Harness.conf` | [Output](https://prover.certora.com/output/8691664/ddfd6ba876e24559bdb4ea989b74cfeb/?anonymousKey=33254d36e1e59c4e7f9ed9f65efcf500fa22e44a) |
