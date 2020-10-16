from brownie import *
from .contract_addresses import *
import time

# Custom parameters
TENPOW18 = 10 ** 18

# Number of tokens you wish to auction, you must be able to transfer these
AUCTION_TOKENS = 1000 * TENPOW18
AUCTION_DAYS = 20
# Dutch auctions start at a high price per token
AUCTION_START_PRICE = 100 * TENPOW18
# This is minimum reserve price per token
AUCTION_RESERVE = 0.001 * TENPOW18

# Calculated variables 
AUCTION_START = int(time.time()) + 200   # Few minutes to deploy
AUCTION_END = AUCTION_START + 60 * 60 * 24 * AUCTION_DAYS

# Constants
SYMBOL = "TT5"
NAME = "Test Token"
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
ETH_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

# Do you want to use the token factory? Set false to redeploy your own
USE_EXISTING_FACTORY = False


def deploy_auction_token(token_factory):
    tx = token_factory.deployTokenContract(SYMBOL,NAME,18,AUCTION_TOKENS,{'from': accounts[0], "value": "0.11 ethers"})
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
    # Use the already deployed contract factories to save gas
    if USE_EXISTING_FACTORY == True:
        # Token Factory
        token_factory_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["token_factory"])
        token_factory = BokkyPooBahsFixedSupplyTokenFactory.at(token_factory_address)
        print("BokkyPooBahsFixedSupplyTokenFactory: " + str(token_factory))
 
        # # DutchSwap Factory
        auction_factory_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["auction_factory"])
        auction_factory = DutchSwapFactory.at(auction_factory_address)
        print("DutchSwapFactory: " + str(auction_factory))
    
    # Deploy new factory contracts
    if USE_EXISTING_FACTORY == False:
        token_factory = deploy_token_factory()
        dutch_auction_template =  deploy_dutch_auction_template()
        auction_factory = deploy_auction_factory(dutch_auction_template)

    # Create new token to be auctioned
    auction_token = deploy_auction_token(token_factory)
    
    # Create new auction
    dutch_auction = deploy_dutch_auction(auction_factory, auction_token)





