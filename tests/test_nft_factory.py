import pytest
from brownie import accounts, reverts
from settings import *

# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

@pytest.fixture(scope='function')
def test_deploy_nft(nft_factory):
    name = "Non Fungible Token"
    symbol = "NFT"
    fee = 0.1 * TENPOW18
    tx = nft_factory.deployNFT(name, symbol, {"from": accounts[0], "value": fee})
    assert "NFTDeployed" in tx.events
    assert nft_factory.balance() == 0.1 * TENPOW18
    assert nft_factory.numberOfNFTs() == 1

def test_withdraw_fund(nft_factory, test_deploy_nft):
    nft_factory.withdrawFund({"from": accounts[0]})
    assert nft_factory.balance() == 0