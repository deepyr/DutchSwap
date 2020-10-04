from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *


# AG: What if the token is not minable during an auction? Should commit tokens to auction

# AG: Withdraw early, small amounts, multiple times 
# AD: Withdraw half before minimum, 

# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_erc20_auction_commitTokens(erc20_auction, payment_token):
    token_buyer =  accounts[2]
    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer * 100, {'from':token_buyer})
    tx = erc20_auction.commitTokens(tokens_to_transfer, {'from': token_buyer})
    assert 'AddedCommitment' in tx.events
    
def test_erc20_auction_commitTokensFrom(erc20_auction, payment_token):
    token_buyer =  accounts[2]
    transfer_agent = accounts[3]
    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer * 100, {'from':token_buyer})
    tx = erc20_auction.commitTokensFrom(token_buyer,tokens_to_transfer, {'from': transfer_agent})
    assert 'AddedCommitment' in tx.events

def test_erc20_auction_commitNoTokens(erc20_auction, payment_token):
    token_buyer =  accounts[2]
    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer * 100, {'from':token_buyer})
    tokens_to_actually_transfer = 0
    # Check no token balances or commitments have changed
    tx = erc20_auction.commitTokens(tokens_to_actually_transfer, {'from': token_buyer})
    

def test_erc20_auction_tokensClaimable(erc20_auction, payment_token):
    assert erc20_auction.tokensClaimable(accounts[2]) == 0
    token_buyer =  accounts[2]
    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer, {'from':token_buyer})
    tx = erc20_auction.commitTokens(tokens_to_transfer, {'from': token_buyer})
    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    assert erc20_auction.tokensClaimable(accounts[2], {'from': accounts[0]}) == AUCTION_TOKENS

    
def test_erc20_auction_twoPurchases(erc20_auction, payment_token):

    token_buyer_a = accounts[2]
    token_buyer_b = accounts[3]
    assert erc20_auction.tokensClaimable(token_buyer_a, {'from': accounts[0]}) == 0
    assert erc20_auction.tokensClaimable(token_buyer_b, {'from': accounts[0]}) == 0

    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.transfer(token_buyer_a, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer, {'from':token_buyer_a})
    tx = erc20_auction.commitTokens(tokens_to_transfer, {'from': token_buyer_a})
    assert 'AddedCommitment' in tx.events
    tokens_to_transfer = 4*tokens_to_transfer
    tx = payment_token.transfer(token_buyer_b, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer, {'from':token_buyer_b})
    tx = erc20_auction.commitTokens(tokens_to_transfer, {'from': token_buyer_b})
    assert 'AddedCommitment' in tx.events
    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    # AG need to double check these numbers
    assert erc20_auction.tokensClaimable(token_buyer_a, {'from': accounts[0]}) == AUCTION_TOKENS / 5
    assert erc20_auction.tokensClaimable(token_buyer_b, {'from': accounts[0]}) == 4*AUCTION_TOKENS / 5


    # assert round(erc20_auction.tokensClaimable(token_buyer_b) * AUCTION_TOKENS / TENPOW18**2) == 8000


def test_erc20_auction_tokenPrice(erc20_auction, payment_token):
    assert erc20_auction.tokenPrice() == 0
    token_buyer=  accounts[2]
    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer, {'from':token_buyer})
    tx = tx = erc20_auction.commitTokens(tokens_to_transfer, {'from': token_buyer})
    assert 'AddedCommitment' in tx.events
    assert erc20_auction.tokenPrice() == tokens_to_transfer * TENPOW18 / AUCTION_TOKENS

def test_erc20_auction_ended(erc20_auction):

    assert erc20_auction.auctionEnded({'from': accounts[0]}) == False
    chain.sleep(AUCTION_TIME)
    chain.mine()
    assert erc20_auction.auctionEnded({'from': accounts[0]}) == True


def test_erc20_auction_claim(erc20_auction, payment_token):
    token_buyer = accounts[2]
    tokens_to_transfer = 100 * TENPOW18

    with reverts():
        erc20_auction.withdrawTokens({'from': accounts[0]})
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer, {'from':token_buyer})
    tx = erc20_auction.commitTokens(tokens_to_transfer, {'from': token_buyer})
    assert erc20_auction.finalised({'from': accounts[0]}) == False

    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    assert erc20_auction.auctionSuccessful({'from': accounts[0]}) == True

    erc20_auction.withdrawTokens({'from': token_buyer})

    # Check for multiple withdraws
    with reverts():
        erc20_auction.withdrawTokens({'from': token_buyer})
        erc20_auction.withdrawTokens({'from': accounts[0]})

    erc20_auction.finaliseAuction({'from': accounts[0]})
    with reverts():
        erc20_auction.finaliseAuction({'from': accounts[0]})


def test_erc20_auction_claim_not_enough(erc20_auction, auction_token, payment_token):
    token_buyer = accounts[2]
    tokens_to_transfer = 0.01 * TENPOW18
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(erc20_auction, tokens_to_transfer, {'from':token_buyer})
    tx = erc20_auction.commitTokens(tokens_to_transfer, {'from': token_buyer})
    chain.sleep(AUCTION_TIME+100)
    chain.mine()
    erc20_auction.withdrawTokens({'from': token_buyer})
    assert auction_token.balanceOf(token_buyer, {'from': token_buyer}) == 0 




def test_erc20_auction_clearingPrice(erc20_auction):
    chain.sleep(100)
    chain.mine()
    assert erc20_auction.clearingPrice() <= AUCTION_START_PRICE
    assert erc20_auction.clearingPrice() > AUCTION_RESERVE

    chain.sleep(AUCTION_TIME)
    chain.mine()
    assert erc20_auction.clearingPrice() == AUCTION_RESERVE

def test_erc20_auction_commitEthToToken(erc20_auction):
    token_buyer =  accounts[2]
    eth_to_transfer = 20 * TENPOW18
    # should not be able to send ETH to a token auction 
    with reverts():
        tx = erc20_auction.commitEth({'from': token_buyer, 'value': eth_to_transfer})
    