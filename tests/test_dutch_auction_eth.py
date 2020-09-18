from brownie import accounts, web3, Wei, reverts, chain
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


def test_dutch_auction_totalTokensCommitted(dutch_auction):
    assert dutch_auction.totalTokensCommitted() == 0

def test_dutch_auction_transferEth(dutch_auction):
    token_buyer =  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    tx = token_buyer.transfer(dutch_auction, eth_to_transfer)
    assert 'AddedCommitment' in tx.events

def test_dutch_auction_commitEth(dutch_auction):
    token_buyer =  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    tx = dutch_auction.commitEth({'from': token_buyer, 'value': eth_to_transfer})
    assert 'AddedCommitment' in tx.events
    
def test_dutch_auction_tokensClaimable(dutch_auction):
    assert dutch_auction.tokensClaimable(accounts[2]) == 0
    token_buyer =  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    dutch_auction.commitEth({'from': token_buyer, 'value': eth_to_transfer})
    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    assert dutch_auction.tokensClaimable(accounts[2], {'from': accounts[0]}) == AUCTION_TOKENS

    
def test_dutch_auction_twoPurchases(dutch_auction):

    token_buyer_a=  accounts[2]
    token_buyer_b =  accounts[3]
    assert dutch_auction.tokensClaimable(token_buyer_a, {'from': accounts[0]}) == 0
    assert dutch_auction.tokensClaimable(token_buyer_b, {'from': accounts[0]}) == 0

    eth_to_transfer = 20 * TENPOW18
    tx = dutch_auction.commitEth({'from': token_buyer_a, 'value': eth_to_transfer})
    assert 'AddedCommitment' in tx.events
    tx = dutch_auction.commitEth({'from': token_buyer_b, 'value': 4*eth_to_transfer})
    assert 'AddedCommitment' in tx.events
    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    # AG need to double check these numbers
    assert dutch_auction.tokensClaimable(token_buyer_a, {'from': accounts[0]}) == AUCTION_TOKENS / 5
    assert dutch_auction.tokensClaimable(token_buyer_b, {'from': accounts[0]}) == 4*AUCTION_TOKENS / 5


    # assert round(dutch_auction.tokensClaimable(token_buyer_b) * AUCTION_TOKENS / TENPOW18**2) == 8000


def test_dutch_auction_tokenPrice(dutch_auction):
    assert dutch_auction.tokenPrice() == 0
    token_buyer=  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    tx = dutch_auction.commitEth({'from': token_buyer, 'value': eth_to_transfer})
    assert 'AddedCommitment' in tx.events
    assert dutch_auction.tokenPrice() == eth_to_transfer * TENPOW18 / AUCTION_TOKENS

def test_dutch_auction_ended(dutch_auction):

    assert dutch_auction.auctionEnded({'from': accounts[0]}) == False
    chain.sleep(AUCTION_TIME)
    chain.mine()
    assert dutch_auction.auctionEnded({'from': accounts[0]}) == True


def test_dutch_auction_claim(dutch_auction):
    token_buyer = accounts[2]
    eth_to_transfer = 100 * TENPOW18

    with reverts():
        dutch_auction.withdrawTokens({'from': accounts[0]})
    
    dutch_auction.commitEth({'from': token_buyer, 'value': eth_to_transfer})
    assert dutch_auction.finalised({'from': accounts[0]}) == False

    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    assert dutch_auction.auctionSuccessful({'from': accounts[0]}) == True

    dutch_auction.withdrawTokens({'from': token_buyer})

    # Check for multiple withdraws
    with reverts():
        dutch_auction.withdrawTokens({'from': token_buyer})
        dutch_auction.withdrawTokens({'from': accounts[0]})

    dutch_auction.finaliseAuction({'from': accounts[0]})
    with reverts():
        dutch_auction.finaliseAuction({'from': accounts[0]})


def test_dutch_auction_claim_not_enough(dutch_auction, auction_token):
    token_buyer = accounts[2]
    eth_to_transfer = 0.01 * TENPOW18

    dutch_auction.commitEth({'from': token_buyer, 'value': eth_to_transfer})
    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    dutch_auction.withdrawTokens({'from': token_buyer})
    assert auction_token.balanceOf(token_buyer, {'from': token_buyer}) == 0 




def test_dutch_auction_clearingPrice(dutch_auction):
    chain.sleep(100)
    chain.mine()
    assert dutch_auction.clearingPrice() <= AUCTION_START_PRICE
    assert dutch_auction.clearingPrice() > AUCTION_RESERVE

    chain.sleep(AUCTION_TIME)
    chain.mine()
    assert dutch_auction.clearingPrice() == AUCTION_RESERVE

