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
| OpenZeppelin | DoubleEndedQueue | `certoraRun src/openzeppelin/DoubleEndedQueue/certora/DoubleEndedQueueHarness.conf` | [Output](https://prover.certora.com/output/8691664/51f471b0e7ef4d91bb17c6b80c2339d2/?anonymousKey=a0b5697706e1241bb6126d2a8055fb659164bbe4) |
| OpenZeppelin | ERC20 | `certoraRun src/openzeppelin/ERC20/certora/ERC20Harness.conf` | [Output](https://prover.certora.com/output/8691664/6e3f9dd50442459897efc7513fd9a92d/?anonymousKey=ac097e430797538be4ea853880f62bc66d905daf) |
| OpenZeppelin | ERC20FlashMint | `certoraRun src/openzeppelin/ERC20FlashMint/certora/ERC20FlashMintHarness.conf` | [Output](https://prover.certora.com/output/8691664/08a836896bca4b5088845605327c66a6/?anonymousKey=d58938604617fd6d28cb8b415f93fbbc5fd712e6) |
| OpenZeppelin | ERC20Wrapper | `certoraRun src/openzeppelin/ERC20Wrapper/certora/ERC20WrapperHarness.conf` | [Output](https://prover.certora.com/output/8691664/3267f77e49a34d029088362f86d89452/?anonymousKey=09e1c929326f377b3e11cf8e3a65a7eb9e8d819b) |
| OpenZeppelin | ERC721 | `certoraRun src/openzeppelin/ERC721/certora/ERC721Harness.conf` | [Output](https://prover.certora.com/output/8691664/cca676c73bbf4f35810d4282e19ff98c/?anonymousKey=3d5834e9df2d169b138e7812f5fb9e5ad8eea833) |
| OpenZeppelin | EnumerableMap | `certoraRun src/openzeppelin/EnumerableMap/certora/EnumerableMapHarness.conf` | [Output](https://prover.certora.com/output/8691664/082f2368561a427e8800b15ee520d310/?anonymousKey=94440088dc59e5ed576b7ce1ead23c931734e6fa) |
| OpenZeppelin | EnumerableSet | `certoraRun src/openzeppelin/EnumerableSet/certora/EnumerableSetHarness.conf` | [Output](https://prover.certora.com/output/8691664/29276bdf97ae4117875f43f82d92ec19/?anonymousKey=7fd0e8e6470094bc6e90f80c3b3be7b5ad7487f2) |
| OpenZeppelin | Initializable | `certoraRun src/openzeppelin/Initializable/certora/InitializableHarness.conf` | [Output](https://prover.certora.com/output/8691664/e6af966ccd8045678780647f35637248/?anonymousKey=40f048d52155267d3c26fa4a87bb6393cfdeaf00) |
| OpenZeppelin | Nonces | `certoraRun src/openzeppelin/Nonces/certora/NoncesHarness.conf` | [Output](https://prover.certora.com/output/8691664/2ee3efeaca8e4811978383b5c9879eae/?anonymousKey=d24f616cea02d17521fee789a23e57a6dc846051) |
| OpenZeppelin | Ownable | `certoraRun src/openzeppelin/Ownable/certora/OwnableHarness.conf` | [Output](https://prover.certora.com/output/8691664/d08fe910a1c643399a1d7fbd4522e164/?anonymousKey=f26c3999b1b6aa64cc3d896f7d639d8e26826644) |
| OpenZeppelin | Ownable2Step | `certoraRun src/openzeppelin/Ownable2Step/certora/Ownable2StepHarness.conf` | [Output](https://prover.certora.com/output/8691664/02a063c3bdf3466d9b3342f30c65b8f0/?anonymousKey=7910bffa9d2b9a5e9e6337177bfd2ddcdbe76107) |
| OpenZeppelin | Pausable | `certoraRun src/openzeppelin/Pausable/certora/PausableHarness.conf` | [Output](https://prover.certora.com/output/8691664/dcacf356222a4809b5be36f228b21f59/?anonymousKey=61d173b85ea39e82f1b23a735fecdaab0bf7c1cc) |
