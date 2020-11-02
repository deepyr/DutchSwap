import pytest
from brownie import accounts, reverts
from settings import *

# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

@pytest.fixture(scope='function')
def test_mint_token(nft):
    _from = accounts[0]
    to = accounts[1]
    token_price = 0.1 * TENPOW18
    status = True
    old_token_id = nft.tokenId()
    old_balance = nft.balanceOf(to)
    tx = nft.mintToken(to, token_price, "", status, {"from": _from})

    assert 'TokenMinted' in tx.events
    
    new_token_id = nft.tokenId()
    new_balance = nft.balanceOf(to)
    token_owner = nft.ownerOf(new_token_id)

    assert new_token_id == old_token_id + 1
    assert new_balance == old_balance + 1
    assert token_owner == to


def test_burn_token(nft, test_mint_token):
    token_id = nft.tokenId()
    assert token_id != 0

    tx = nft.burnToken(token_id, {"from": accounts[1] })
    assert 'TokenBurned' in tx.events
    
    with reverts():
        nft.ownerOf(token_id)

def test_buy_token(nft, test_mint_token):
    token_id = nft.tokenId()
    assert token_id != 0

    value = 0.1 * TENPOW18
    old_owner = nft.ownerOf(token_id)
    tx = nft.buyToken(token_id, {"from": accounts[2], "value": value })
    assert 'TokenBought' in tx.events
    
    new_owner = nft.ownerOf(token_id)
    assert old_owner != new_owner
    assert new_owner == accounts[2]

