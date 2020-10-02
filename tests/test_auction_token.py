from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *

# BokkyPooBah's Fixed Token 
# These contracts are in heavy use thoughout Etheruem, written by one of the greats. 
# Testing the contract factory here is more of a placeholder to check the config file

# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


# def test_fixed_token_init(auction_token):
#     assert auction_token.totalSupply({'from': accounts[0]}) == 10*AUCTION_TOKENS

def test_fixed_token_approve(payment_token):
    token_buyer =  accounts[2]
    token_spender =  accounts[3]
    token_receiver =  accounts[4]

    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.approve(token_spender, tokens_to_transfer * 100, {'from':token_buyer})
    assert 'Approval' in tx.events

def test_fixed_token_transferTokens( payment_token):
    token_buyer =  accounts[2]
    token_spender =  accounts[3]
    token_receiver =  accounts[4]

    tokens_to_transfer = 20 * TENPOW18
    tx = payment_token.transfer(token_buyer, tokens_to_transfer, {'from':accounts[0]})
    tx = payment_token.approve(token_spender, tokens_to_transfer * 100, {'from':token_buyer})
    tx = payment_token.transferFrom(token_buyer, token_receiver, tokens_to_transfer , {'from':token_spender})
    assert 'Transfer' in tx.events
