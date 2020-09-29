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


def test_auction_factory_numberOfAuctions(auction_factory):
    assert auction_factory.numberOfAuctions({'from': accounts[0]}) == 0

def test_auction_factory_deployTokenContract(auction_factory, auction_token):
    startDate = chain.time() +10
    endDate = startDate + AUCTION_TIME
    wallet = accounts[1]
    tx = auction_token.approve(auction_factory, AUCTION_TOKENS, {'from': accounts[0]})
    tx = auction_factory.deployDutchAuction(auction_token, AUCTION_TOKENS, startDate, endDate,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    assert 'DutchAuctionDeployed' in tx.events
    assert auction_factory.numberOfAuctions({'from': accounts[0]}) == 1

def test_auction_factory_setMinimumFee(auction_factory):
    new_fee_amount = 0.2 *  TENPOW18
    assert auction_factory.minimumFee({'from': accounts[0]}) == 0
    tx = auction_factory.setMinimumFee(new_fee_amount, {'from': accounts[0]})
    assert 'MinimumFeeUpdated' in tx.events
    with reverts():
        tx = auction_factory.setMinimumFee(0, {'from': accounts[1]})
    assert auction_factory.minimumFee({'from': accounts[0]}) == new_fee_amount
