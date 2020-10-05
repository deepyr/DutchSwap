from brownie import *
from .contract_addresses import *
import time


TENPOW18 = 10 ** 18
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
ETH_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

AUCTION_TOKENS = 1000 * TENPOW18
AUCTION_DAYS = 2
AUCTION_START_PRICE = 100 * TENPOW18
AUCTION_RESERVE = 0.001 * TENPOW18

AUCTION_START = int(time.time()) + 200   # Few minutes to deploy
AUCTION_END = AUCTION_START + 60 * 60 * 24 * AUCTION_DAYS


def deploy_token_factory():
    token_factory = BokkyPooBahsFixedSupplyTokenFactory.deploy({'from': accounts[0]})
    return token_factory


def deploy_auction_token(token_factory):
    symbol = "TT5"
    name = "Test Token"
    totalSupply = 1000000000000000000000000
    tx = token_factory.deployTokenContract(symbol,name,18,totalSupply,{'from': accounts[0], "value": "0.11 ethers"})
    auction_token = FixedSupplyToken.at(web3.toChecksumAddress(tx.events['TokenDeployed']['token']))
    print("FixedSupplyToken deployed at: " + str(auction_token))

    return auction_token


def deploy_dutch_auction_template():
    dutch_auction_template = DutchSwapAuction.deploy({'from': accounts[0]})
    return dutch_auction_template


def deploy_auction_factory(dutch_auction_template):
    auction_factory = DutchSwapFactory.deploy({"from": accounts[0]})
    auction_factory.initDutchSwapFactory(dutch_auction_template, 0, {"from": accounts[0]})
    assert auction_factory.numberOfAuctions( {'from': accounts[0]}) == 0 
    return auction_factory


def deploy_dutch_auction(auction_factory, auction_token):

    wallet = accounts[1]

    auction_token.approve(auction_factory,AUCTION_TOKENS, {"from": accounts[0]})
    tx = auction_factory.deployDutchAuction(auction_token, AUCTION_TOKENS, AUCTION_START,AUCTION_END,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    assert 'DutchAuctionDeployed' in tx.events
    dutch_auction = DutchSwapAuction.at(web3.toChecksumAddress(tx.events['DutchAuctionDeployed']['addr']))
    assert dutch_auction.clearingPrice() == AUCTION_START_PRICE
    print("DutchSwap Auction deployed at: " + str(dutch_auction))

    return dutch_auction


def main():
    use_exisiting_token_factory = True
    use_exisiting_auction_factory = False
    # add accounts if active network is ropsten
    if network.show_active() in ['ropsten', 'rinkeby', 'kovan', 'goerli']:
        # accounts[0] = 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')
        # accounts[1] = 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')

    if network.show_active() == 'mainnet':
        # Import encrypted keyfile for key security
        # (or deploy with burner address and change owner after deployment 
        use_exisiting_token_factory = False
        use_exisiting_auction_factory = False
        
    # Token Factory
    if use_exisiting_token_factory == True:
        
        token_factory_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["token_factory"])
        token_factory = BokkyPooBahsFixedSupplyTokenFactory.at(token_factory_address)
        print("BokkyPooBahsFixedSupplyTokenFactory: " + str(token_factory))
    else:
        token_factory = deploy_token_factory()
    
    # DutchSwap Factory
    if use_exisiting_auction_factory == True:
        auction_factory_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["auction_factory"])
        auction_factory = DutchSwapFactory.at(auction_factory_address)
        print("DutchSwapFactory: " + str(auction_factory))
    else:
        dutch_auction_template =  deploy_dutch_auction_template()
        auction_factory = deploy_auction_factory(dutch_auction_template)

    auction_token = deploy_auction_token(token_factory)
    dutch_auction = deploy_dutch_auction(auction_factory, auction_token)


# Run `brownie run deploy_DutchSwapFactory.py --network rinkeby`
# Brownie v1.11.0 - Python development framework for Ethereum

# Compiling contracts...
#   Solc version: 0.6.12
#   Optimizer: Enabled  Runs: 200
#   EVM Version: Istanbul
# Generating build data...
#  - ApproveAndCallFallback...
#  - BokkyPooBahsFixedSupplyTokenFactory...
#  - FixedSupplyToken...
#  - TokenInterface...
#  - DutchSwapFactory...
#  - WETH9...
#  - DutchSwapVault...
#  - SafeMath...
#  - CloneFactory...
#  - ReentrancyGuard...
#  - Owned...
#  - DutchSwapAuction...

# /Users/adrian/Library/Python/3.8/lib/python/site-packages/brownie/_config.py:192: DeprecationWarning: The `network` field in `brownie-config.yaml` has been deprecated. Network settings are now handled via `brownie networks` in the CLI. Remove `network` from /Users/adrian/Documents/GitHub/DutchSwapDeepyr/brownie-config to silence this warning.
#   warnings.warn(
# DutchswapdeepyrProject is the active project.

# Running 'scripts/deploy_DutchSwapFactory.py::main'...
# BokkyPooBahsFixedSupplyTokenFactory: 0x1C3e1D406E64004416Fd592C55f9eDeD1A76Bae8
# Transaction sent: 0xa3d8c8edf48a7ff2ad36d3619e6bcdc9ef032e6b6a6289b843c24e943c1ef856
#   Gas price: 1.0 gwei   Gas limit: 1032142
# Waiting for confirmation...
#   DutchSwapAuction.constructor confirmed - Block: 7313460   Gas used: 1032142 (100.00%)
#   DutchSwapAuction deployed at: 0x6C61c6d448810dD022318A03538Db1ACcdeC3B65

# Transaction sent: 0xa45672e06320fd447e4c3827c4b8f67a325102d7521a216bca105f4ed2330fd1
#   Gas price: 1.0 gwei   Gas limit: 868928
# Waiting for confirmation...
#   DutchSwapFactory.constructor confirmed - Block: 7313461   Gas used: 868928 (100.00%)
#   DutchSwapFactory deployed at: 0x30E5620794dDe007f9F071344Ecdd44C959Bb4B6

# Transaction sent: 0xc98e71abb645160273cdbdc626197243f7975cfb07b824e612c4fe02737cb149
#   Gas price: 1.0 gwei   Gas limit: 68360
# Waiting for confirmation...
#   DutchSwapFactory.initDutchSwapFactory confirmed - Block: 7313462   Gas used: 66868 (97.82%)

# Transaction sent: 0x7e984cfa84bc51bf933c985621e5b40522607cfe969c79357654aa85c460bb91
#   Gas price: 1.0 gwei   Gas limit: 1046946
# Waiting for confirmation...
#   BokkyPooBahsFixedSupplyTokenFactory.deployTokenContract confirmed - Block: 7313463   Gas used: 1044769 (99.79%)

# FixedSupplyToken deployed at: 0xf40A98954b66638A700dd20de5809227a5F64410
# Transaction sent: 0xcb9e7cfcadfaac75a82e96834182a7e0656d9b16f73aedb1d7b5b4fbf5c0a565
#   Gas price: 1.0 gwei   Gas limit: 43990
# Waiting for confirmation...
#   FixedSupplyToken.approve confirmed - Block: 7313464   Gas used: 43990 (100.00%)

# Transaction sent: 0x7a53d1efbd528aa535a6ca28fbd527f23e2a8dfa84395151bed1fb615f88680a
#   Gas price: 1.0 gwei   Gas limit: 477398
# Waiting for confirmation...
#   DutchSwapFactory.deployDutchAuction confirmed - Block: 7313465   Gas used: 418858 (87.74%)

# DutchSwap Auction deployed at: 0xd2b59001B352d35b7583F469822e3469eD390c3a