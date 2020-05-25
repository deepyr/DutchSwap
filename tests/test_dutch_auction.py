from brownie import accounts, web3, Wei, reverts, rpc
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *


# AG: What if the token is not minable during an auction? Should commit tokens to auction

# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_dutch_auction_tokensClaimed(dutch_auction):
    assert dutch_auction.tokensClaimed() == 0


def test_dutch_auction_commitEth(dutch_auction):
    token_buyer =  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    tx = token_buyer.transfer(dutch_auction, eth_to_transfer)
    assert 'AddedCommitment' in tx.events

    
def test_dutch_auction_tokensClaimable(dutch_auction):
    assert dutch_auction.tokensClaimable(accounts[2]) == 0
    token_buyer =  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    tx = token_buyer.transfer(dutch_auction, eth_to_transfer)
    assert 'AddedCommitment' in tx.events
    rpc.sleep(AUCTION_TIME+100)
    rpc.mine()
    assert dutch_auction.tokensClaimable(accounts[2]) == "1000 ether"

    
def test_dutch_auction_twoPurchases(dutch_auction):
    assert dutch_auction.tokensClaimable(accounts[2]) == 0
    token_buyer_a=  accounts[2]
    token_buyer_b =  accounts[3]

    eth_to_transfer = 20 * TENPOW18
    tx = token_buyer_a.transfer(dutch_auction, 20 * TENPOW18)
    assert 'AddedCommitment' in tx.events
    tx = token_buyer_b.transfer(dutch_auction, 80 * TENPOW18)
    assert 'AddedCommitment' in tx.events
    assert dutch_auction.tokensClaimable(token_buyer_a) == "200 ether"
    assert dutch_auction.tokensClaimable(token_buyer_b) == "800 ether"


def test_dutch_auction_tokenPrice(dutch_auction):
    assert dutch_auction.tokenPrice() == 0
    token_buyer=  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    tx = token_buyer.transfer(dutch_auction, eth_to_transfer)
    assert 'AddedCommitment' in tx.events
    assert dutch_auction.tokenPrice() == eth_to_transfer * TENPOW18 / AUCTION_TOKENS

def test_dutch_auction_ended(dutch_auction):

    assert dutch_auction.auctionEnded({'from': accounts[0]}) == False
    rpc.sleep(AUCTION_TIME)
    rpc.mine()
    assert dutch_auction.auctionEnded({'from': accounts[0]}) == True


def test_dutch_auction_claim(dutch_auction):
    token_buyer = accounts[2]
    eth_to_transfer = 100 * TENPOW18

    dutch_auction.claim()
    
    tx = token_buyer.transfer(dutch_auction,eth_to_transfer)
    with reverts():
        dutch_auction.finaliseAuction()
    
    rpc.sleep(AUCTION_TIME+100)
    rpc.mine()
    dutch_auction.claim({'from': token_buyer})
    dutch_auction.claim({'from': accounts[0]})
    assert dutch_auction.auctionSuccessful({'from': accounts[0]}) == True

    dutch_auction.finaliseAuction()


def test_dutch_auction_claim_not_enough(dutch_auction):
    token_buyer = accounts[2]
    eth_to_transfer = 0.01 * TENPOW18

    tx = token_buyer.transfer(dutch_auction,eth_to_transfer)
    rpc.sleep(AUCTION_TIME+100)
    rpc.mine()
    dutch_auction.claim({'from': token_buyer})



def test_dutch_auction_auctionPrice(dutch_auction):
    rpc.sleep(100)
    rpc.mine()
    assert dutch_auction.auctionPrice() <= AUCTION_START_PRICE
    assert dutch_auction.auctionPrice() > AUCTION_RESERVE

    rpc.sleep(AUCTION_TIME)
    rpc.mine()
    assert dutch_auction.auctionPrice() == AUCTION_RESERVE

