from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *


# BokkyPooBah's Fixed Token 


# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_token_factory_init(token_factory):
    assert token_factory.numberOfChildren() == 1
    assert token_factory.minimumFee() == '0.1 ether'


def test_token_factory_minimumFee(token_factory):
    assert token_factory.minimumFee() == '0.1 ether'
    token_factory.setMinimumFee('0.2 ether')
    assert token_factory.minimumFee() == '0.2 ether'

