
from brownie import accounts, web3, Wei, rpc
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *





##############################################
# Auction
##############################################

# @pytest.fixture(scope='module', autouse=True)
# def auction_token(TestToken):

#     token_owner = accounts[0]
#     name = 'BASE TOKEN'
#     symbol = 'TKN'
#     initial_supply = 0

#     auction_token = TestToken.deploy(token_owner, name, symbol, initial_supply,{'from': accounts[0]})

#     return auction_token



@pytest.fixture(scope='module', autouse=True)
def dutch_auction(DutchSwapAuction, auction_token):
    startDate = rpc.time() +10
    endDate = startDate + AUCTION_TIME
    wallet = accounts[1]

    dutch_auction = DutchSwapAuction.deploy({'from': accounts[0]})
    dutch_auction.initDutchAuction(auction_token, AUCTION_TOKENS, startDate, endDate, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    auction_token.setMintOperator(dutch_auction, True, {"from": accounts[0]})
    assert dutch_auction.auctionPrice() == AUCTION_START_PRICE
    rpc.sleep(10)
    return dutch_auction
