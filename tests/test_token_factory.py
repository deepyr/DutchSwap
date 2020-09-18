from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *


# BokkyPooBah's Fixed Token 
# These contracts are in heavy use thoughout Etheruem, written by one of the greats. 
# Testing the contract factory here is more of a placeholder to check if it was deployed

# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_token_factory_init(token_factory):
    # assert token_factory.numberOfChildren() == 2     # When deployed with factory
    assert token_factory.numberOfChildren() == 0     # when testing code coverage 
    assert token_factory.minimumFee({'from': accounts[0]}) == '0.1 ether'


def test_token_factory_minimumFee(token_factory):
    assert token_factory.minimumFee({'from': accounts[0]}) == '0.1 ether'
    tx = token_factory.setMinimumFee('0.2 ether', {'from': accounts[0]})
    assert token_factory.minimumFee({'from': accounts[0]}) == '0.2 ether'

