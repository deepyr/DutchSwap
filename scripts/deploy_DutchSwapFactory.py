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
    use_exisiting_auction_factory = True
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



# Goerli Testnet txns
# Running 'scripts/deploy_DutchSwapFactory.py::main'...
# Transaction sent: 0x8ea861f75969836e41dad80df92e3f1136dff6f2ae1101fc8f86d468373b11c9
#   Gas price: 1.23 gwei   Gas limit: 1642374
# Waiting for confirmation...
#   BokkyPooBahsFixedSupplyTokenFactory.constructor confirmed - Block: 3514016   Gas used: 1642374 (100.00%)
#   BokkyPooBahsFixedSupplyTokenFactory deployed at: 0x2c2a4b9843eC5377f4BC25797E8B3639Da1d09dD

# Transaction sent: 0xfd64947faf6d6f3ea80ac39d8691f74b9b2cfbce7f7c732bcfa05314169dd06e
#   Gas price: 1.23 gwei   Gas limit: 1013366
# Waiting for confirmation...
#   DutchSwapAuction.constructor confirmed - Block: 3514017   Gas used: 1013366 (100.00%)
#   DutchSwapAuction deployed at: 0x43Aa31AC6FB37337520c909EB9aB7529444Bfd18

# Transaction sent: 0xb80ec6809b814644c3e8d73d42dac38250fb36649287110258925bbbade4897b
#   Gas price: 1.23 gwei   Gas limit: 828983
# Waiting for confirmation...
#   DutchSwapFactory.constructor confirmed - Block: 3514019   Gas used: 828983 (100.00%)
#   DutchSwapFactory deployed at: 0x4FEeD5528f6a350269cb474bE3f726542c73C08B

# Transaction sent: 0x08f7c731f88c07bbdfb9b891987aea8e4ae6a0aae8be59725cc695223dc3750c
#   Gas price: 1.23 gwei   Gas limit: 68338
# Waiting for confirmation...
#   DutchSwapFactory.initDutchSwapFactory confirmed - Block: 3514020   Gas used: 66846 (97.82%)

# Transaction sent: 0x37757dfd99922af326cc24aa96b9aac015087af8a31acb587eb0d638970d1e6f
#   Gas price: 1.23 gwei   Gas limit: 1108791
# Waiting for confirmation...
#   BokkyPooBahsFixedSupplyTokenFactory.deployTokenContract confirmed - Block: 3514021   Gas used: 1106614 (99.80%)

# FixedSupplyToken deployed at: 0x28BB7A15A3497bfDdDb0CF5E920d08B74581D7BE
# Transaction sent: 0x90942074aa1c55b01af86db374ad4b4b5f42f9dfba0fa3b967e2945200f468dc
#   Gas price: 1.23 gwei   Gas limit: 43989
# Waiting for confirmation...
#   FixedSupplyToken.approve confirmed - Block: 3514022   Gas used: 43989 (100.00%)

# Transaction sent: 0x9ca9fa23c1c78274ddfc42303e6be2a9af4c32a3c5899307e7f8c35a7fbade24
#   Gas price: 1.23 gwei   Gas limit: 477809
# Waiting for confirmation...
#   DutchSwapFactory.deployDutchAuction confirmed - Block: 3514024   Gas used: 419263 (87.75%)

# DutchSwap Auction deployed at: 0x1e7D12fb23376c67929fEb96816374F49C3FEC49



# Kovan deployment
# # 
# Running 'scripts/deploy_DutchSwapFactory.py::main'...
# Transaction sent: 0x5ec1479e16c6227d9dd2cbc4b4cb4212f03f5f5faf0a818661bdc55d66484143
#   Gas price: 9.0 gwei   Gas limit: 1642374
#   BokkyPooBahsFixedSupplyTokenFactory.constructor confirmed - Block: 21329940   Gas used: 1642374 (100.00%)
#   BokkyPooBahsFixedSupplyTokenFactory deployed at: 0x3FE8D9113De0bF1A0Ad5c48D036197cBD264aeb2

# Transaction sent: 0x8baba531e562244b2765c0004fbb5cc87fb5518e80bcdb630721b9e36855c2b7
#   Gas price: 9.0 gwei   Gas limit: 1013366
# Waiting for confirmation...
#   DutchSwapAuction.constructor confirmed - Block: 21329941   Gas used: 1013366 (100.00%)
#   DutchSwapAuction deployed at: 0xEb3e0a258294682782e40ca0D7da8AB3506F45Fa

# Transaction sent: 0xbf43b5a21486c7a9163f1cbadbbfe24ff33645ab10d52bfa7d130df26d290cd1
#   Gas price: 9.0 gwei   Gas limit: 828983
#   DutchSwapFactory.constructor confirmed - Block: 21329942   Gas used: 828983 (100.00%)
#   DutchSwapFactory deployed at: 0x9a25CB87332E6Bc680E44fF04F14cBd9DAaF5D84

# Transaction sent: 0xcaa98d06ad8dbccf6eed8c5722b23edac1200477f9ae6072db6bc78f48639765
#   Gas price: 9.0 gwei   Gas limit: 68338
#   DutchSwapFactory.initDutchSwapFactory confirmed - Block: 21329943   Gas used: 66846 (97.82%)

# Transaction sent: 0xef5871a4dd82dd3aef73a9b676d8bcca5d522cd86a4bd85248608d6548e2185b
#   Gas price: 9.0 gwei   Gas limit: 1108791
# Waiting for confirmation...
#   BokkyPooBahsFixedSupplyTokenFactory.deployTokenContract confirmed - Block: 21329944   Gas used: 1106614 (99.80%)

# FixedSupplyToken deployed at: 0x5eBB983847d4ffA663f2ED5F33668D43EC9dBF02
# Transaction sent: 0x1cfad9f4cf51fe50e8b6364fcc82c5d9cfe2eaf0d53b69539a46eb51b873a528
#   Gas price: 9.0 gwei   Gas limit: 43989
#   FixedSupplyToken.approve confirmed - Block: 21329945   Gas used: 43989 (100.00%)

# Transaction sent: 0x740b7cb54181fd4b2b6f23eb335e0ef0698f712f7d9da75a9503777687014cfc
#   Gas price: 9.0 gwei   Gas limit: 477809
#   DutchSwapFactory.deployDutchAuction confirmed - Block: 21329946   Gas used: 419263 (87.75%)

# DutchSwap Auction deployed at: 0xC0dcff5440631A1f6d62A0562e480152De88eBeB 