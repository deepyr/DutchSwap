
from brownie import accounts, web3, Wei, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *





##############################################
# Token Factory
##############################################

@pytest.fixture(scope='module', autouse=True)
def token_factory(BokkyPooBahsFixedSupplyTokenFactory):

    token_factory = BokkyPooBahsFixedSupplyTokenFactory.deploy({'from': accounts[0]})
    return token_factory


@pytest.fixture(scope='module', autouse=True)
def auction_token(token_factory, FixedSupplyToken):

    token_owner = accounts[0]
    name = 'BASE TOKEN'
    symbol = 'TKN'
    initial_supply = AUCTION_TOKENS
    tx = token_factory.deployTokenContract(symbol,name, 18,initial_supply, {'from': token_owner, 'value': '0.2 ethers'})
    auction_token = FixedSupplyToken.at(tx.return_value)

    return auction_token


##############################################
# Auction
##############################################


@pytest.fixture(scope='module', autouse=True)
def dutch_auction_template(DutchSwapAuction):
    dutch_auction_template = DutchSwapAuction.deploy({'from': accounts[0]})
    return dutch_auction_template



@pytest.fixture(scope='module', autouse=True)
def auction_factory(DutchSwapFactory, dutch_auction_template):
    auction_factory = DutchSwapFactory.deploy({"from": accounts[0]})
    auction_factory.initDutchSwapFactory(dutch_auction_template, 0, {"from": accounts[0]})
    assert auction_factory.numberOfAuctions( {'from': accounts[0]}) == 0 

    return auction_factory





@pytest.fixture(scope='module', autouse=True)
def dutch_auction(DutchSwapAuction, auction_factory, auction_token):
    startDate = chain.time() +10
    endDate = startDate + AUCTION_TIME
    wallet = accounts[1]
    tx = auction_token.approve(auction_factory, AUCTION_TOKENS, {'from': accounts[0]})
    tx = auction_factory.deployDutchAuction(auction_token, AUCTION_TOKENS, startDate, endDate,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    dutch_auction = DutchSwapAuction.at(tx.return_value)
    assert dutch_auction.clearingPrice() == AUCTION_START_PRICE
    chain.sleep(10)
    return dutch_auction



# @pytest.fixture(scope='module', autouse=True)
# def dutch_auction(DutchSwapAuction, auction_token):
#     startDate = chain.time() +10
#     endDate = startDate + AUCTION_TIME
#     wallet = accounts[1]

#     dutch_auction = DutchSwapAuction.deploy({'from': accounts[0]})
#     dutch_auction.initDutchAuction(auction_token, AUCTION_TOKENS, startDate, endDate, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
#     auction_token.setMintOperator(dutch_auction, True, {"from": accounts[0]})
#     assert dutch_auction.auctionPrice() == AUCTION_START_PRICE
#     chain.sleep(10)
#     return dutch_auction


##############################################
# NFT
##############################################


@pytest.fixture(scope='module', autouse=True)
def nft(NFT):
    nft = NFT.deploy({'from': accounts[0]})

    name = 'Non Fungible Token'
    symbol = 'NFT'

    nft.initNFT(
               name
               , symbol
               , {"from": accounts[0]})
    assert nft.name() == name
    assert nft.symbol() == symbol
    assert nft.owner() == accounts[0]

    return nft

@pytest.fixture(scope='module', autouse=True)
def nft_factory(NFTFactory, nft):
    nft_factory = NFTFactory.deploy({'from': accounts[0]})
    minimum_fee = 0.1 * TENPOW18
    fund_wallet = accounts[1]
    nft_factory.initNFTFactory(nft, minimum_fee, fund_wallet, {'from': accounts[0]})
    
    assert nft_factory.minimumFee() == minimum_fee
    assert nft_factory.nftTemplate() == nft
    assert nft_factory.fundWallet() == fund_wallet

    return nft_factory
