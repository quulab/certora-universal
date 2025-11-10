# certora-universal

Universal set of certora rules.

## Common
Catches:
- reachability (all methods have a none reverting path)

```
certoraRun src/common/certora/Common.conf
```

Output: https://prover.certora.com/output/8691664/426d12fa3fc24c859286d34cf723b2e4/?anonymousKey=12e7693b3fe3e6427a0f15007c4b0a610c32983a

## OpenZeppelin

### ERC20
```
certoraRun src/openzeppelin/ERC20/certora/ERC20Harness.conf
```

Output: https://prover.certora.com/output/8691664/ddfd6ba876e24559bdb4ea989b74cfeb/?anonymousKey=33254d36e1e59c4e7f9ed9f65efcf500fa22e44a
