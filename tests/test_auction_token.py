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

