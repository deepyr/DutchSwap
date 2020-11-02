
from brownie import accounts, web3, Wei, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *





##############################################
# Tokens
##############################################

@pytest.fixture(scope='module', autouse=True)
def token_factory(BokkyPooBahsFixedSupplyTokenFactory):

    token_factory = BokkyPooBahsFixedSupplyTokenFactory.deploy({'from': accounts[0]})
    return token_factory

@pytest.fixture(scope='module', autouse=True)
def auction_token(FixedSupplyToken):
    token_owner = accounts[0]
    name = 'BASE TOKEN'
    symbol = 'TKN'
    initial_supply = 10*AUCTION_TOKENS
    auction_token = FixedSupplyToken.deploy({'from': token_owner})
    tx = auction_token.init(token_owner, symbol,name, 18,initial_supply, {'from': token_owner})
    return auction_token

@pytest.fixture(scope='module', autouse=True)
def payment_token(FixedSupplyToken):
    token_owner = accounts[0]
    name = 'PAY TOKEN'
    symbol = 'PAY'
    initial_supply = 10*PAYMENT_TOKENS
    payment_token = FixedSupplyToken.deploy({'from': token_owner})
    tx = payment_token.init(token_owner, symbol,name, 18,initial_supply, {'from': token_owner})
    return payment_token

# Uncomment to test tokens made from FixedTokenFactory
# @pytest.fixture(scope='module', autouse=True)
# def payment_token(token_factory, FixedSupplyToken):
#     token_owner = accounts[0]
#     name = 'PAY TOKEN'
#     symbol = 'PAY'
#     initial_supply = PAYMENT_TOKENS
#     tx = token_factory.deployTokenContract(symbol,name, 18,initial_supply, {'from': token_owner, 'value': '0.2 ethers'})
#     payment_token = FixedSupplyToken.at(tx.return_value)
#     return payment_token


@pytest.fixture(scope='module', autouse=True)
def vault_token(FixedSupplyToken):
    token_owner = accounts[0]
    name = 'VAULT TOKEN'
    symbol = 'VAULT'
    initial_supply = 10*PAYMENT_TOKENS
    vault_token = FixedSupplyToken.deploy({'from': token_owner})
    tx = vault_token.init(token_owner, symbol,name, 18,initial_supply, {'from': token_owner})
    return vault_token

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


# Auction with ETHs as the payment currency
@pytest.fixture(scope='module', autouse=True)
def dutch_auction(DutchSwapAuction, auction_token):
    
    startDate = chain.time() +10
    endDate = startDate + AUCTION_TIME
    wallet = accounts[1]
    funder = accounts[0]

    dutch_auction = DutchSwapAuction.deploy({'from': accounts[0]})
    tx = auction_token.approve(dutch_auction, AUCTION_TOKENS, {'from':funder})

    dutch_auction.initDutchAuction(funder, auction_token, AUCTION_TOKENS, startDate, endDate,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    assert dutch_auction.clearingPrice( {'from': accounts[0]}) == AUCTION_START_PRICE

    # Cannot contribute early
    # with reverts():
    #     tx = token_buyer.transfer(dutch_auction, eth_to_transfer)

    # testing pre auction calcs
    assert dutch_auction.calculateCommitment(0) == 0 
    assert dutch_auction.calculateCommitment(AUCTION_START_PRICE) == AUCTION_START_PRICE
    assert dutch_auction.calculateCommitment(AUCTION_START_PRICE*AUCTION_TOKENS / TENPOW18) == AUCTION_START_PRICE*AUCTION_TOKENS / TENPOW18
    assert dutch_auction.calculateCommitment(10 * AUCTION_START_PRICE*AUCTION_TOKENS ) == AUCTION_START_PRICE*AUCTION_TOKENS / TENPOW18

    # Move the chain to the moment the auction begins
    chain.sleep(10)
    return dutch_auction


# Auction with an ERC20 token as the payment currency
@pytest.fixture(scope='module', autouse=True)
def erc20_auction(DutchSwapAuction, auction_token, payment_token):
    startDate = chain.time() +10
    endDate = startDate + AUCTION_TIME
    wallet = accounts[1]
    funder = accounts[0]

    erc20_auction = DutchSwapAuction.deploy({'from': accounts[0]})
    tx = auction_token.approve(erc20_auction, AUCTION_TOKENS, {'from':funder})

    erc20_auction.initDutchAuction(funder, auction_token, AUCTION_TOKENS, startDate, endDate,payment_token, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    assert erc20_auction.clearingPrice( {'from': accounts[0]}) == AUCTION_START_PRICE

    # with reverts():
    #     tx = token_buyer.transfer(dutch_auction, eth_to_transfer)

    chain.sleep(10)
    return erc20_auction


# Auction with ETHs as the payment currency
@pytest.fixture(scope='module', autouse=True)
def hyperbolic_auction(DutchSwapHyperbolic, auction_token):
    
    startDate = chain.time() +10
    endDate = startDate + AUCTION_TIME
    wallet = accounts[1]
    funder = accounts[0]

    hyperbolic_auction = DutchSwapHyperbolic.deploy({'from': accounts[0]})
    tx = auction_token.approve(hyperbolic_auction, AUCTION_TOKENS, {'from':funder})

    hyperbolic_auction.initDutchAuction(funder, auction_token, AUCTION_TOKENS, startDate, endDate,ETH_ADDRESS, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    # assert hyperbolic_auction.clearingPrice( {'from': accounts[0]}) == AUCTION_START_PRICE

    # Move the chain to the moment the auction begins
    chain.sleep(10)
    return hyperbolic_auction


# Auction with ETHs as the payment currency
@pytest.fixture(scope='module', autouse=True)
def pre_auction(DutchSwapAuction, auction_token):
    
    startDate = chain.time() +100
    endDate = startDate + AUCTION_TIME
    wallet = accounts[1]
    funder = accounts[0]

    pre_auction = DutchSwapAuction.deploy({'from': accounts[0]})
    tx = auction_token.approve(pre_auction, AUCTION_TOKENS, {'from':funder})

    pre_auction.initDutchAuction(funder, auction_token, AUCTION_TOKENS, startDate, endDate,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    assert pre_auction.clearingPrice( {'from': accounts[0]}) == AUCTION_START_PRICE

    return pre_auction



##############################################
# Vault Contracts
##############################################


# Auction with ETHs as the payment currency
@pytest.fixture(scope='module', autouse=True)
def pre_auction_vault(DutchSwapVault):
    pre_auction_vault = DutchSwapVault.deploy({'from': accounts[0]})
    return pre_auction_vault

# Auction with ETHs as the payment currency
@pytest.fixture(scope='module', autouse=True)
def vault_auction(DutchSwapAuction, vault_token, pre_auction_vault):
    
    startDate = chain.time() +100
    endDate = startDate + AUCTION_TIME
    wallet = pre_auction_vault
    funder = accounts[0]

    vault_auction = DutchSwapAuction.deploy({'from': accounts[0]})
    tx = vault_token.approve(vault_auction, AUCTION_TOKENS, {'from':funder})

    vault_auction.initDutchAuction(funder, vault_token, AUCTION_TOKENS, startDate, endDate,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    assert vault_auction.clearingPrice( {'from': accounts[0]}) == AUCTION_START_PRICE

    return vault_auction

# Auction with ETHs as the payment currency
@pytest.fixture(scope='module', autouse=True)
def auction_vault(vault_auction, pre_auction_vault):
    refundPct = 1000   
    refundTime = vault_auction.endDate( {'from': accounts[0]}) + VAULT_LOCKUP
    # print("startDate: " + str(startDate))
    # print("refundTime: " + str(refundTime))
    auction_vault = pre_auction_vault
    auction_vault.initAuctionVault(vault_auction, refundPct,  refundTime, VAULT_WINDOW, {"from": accounts[0]})
    return auction_vault

##############################################
# Factory Contracts
##############################################

# Skipped for code coverage
# Factory tested seperately for coverage

# @pytest.fixture(scope='module', autouse=True)
# def factory_token(token_factory, FixedSupplyToken):
#     token_owner = accounts[0]
#     name = 'FACTORY TOKEN'
#     symbol = 'FACT'
#     initial_supply = 10*AUCTION_TOKENS
#     tx = token_factory.deployTokenContract(symbol,name, 18,initial_supply, {'from': token_owner, 'value': '0.2 ethers'})
#     factory_token = FixedSupplyToken.at(tx.return_value)
#     return factory_token


# @pytest.fixture(scope='module', autouse=True)
# def dutch_auction(DutchSwapAuction, auction_factory, auction_token):
#     startDate = chain.time() +10
#     endDate = startDate + AUCTION_TIME
#     wallet = accounts[1]
#     tx = auction_token.approve(auction_factory, AUCTION_TOKENS, {'from': accounts[0]})
#     tx = auction_factory.deployDutchAuction(auction_token, AUCTION_TOKENS, startDate, endDate,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
#     dutch_auction = DutchSwapAuction.at(tx.return_value)
#     assert dutch_auction.clearingPrice() == AUCTION_START_PRICE
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
