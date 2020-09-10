from brownie import *
from .contract_addresses import *
import time


TENPOW18 = 10 ** 18
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
ETH_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

AUCTION_TOKENS = 1000 * TENPOW18
AUCTION_DAYS = 2
AUCTION_START_PRICE = 100 * TENPOW18
AUCTION_RESERVE = 0.001 * TENPOW18

AUCTION_START = int(time.time()) + 200   # Few minutes to deploy
AUCTION_END = AUCTION_START + 60 * 60 * 24 * AUCTION_DAYS


def deploy_token_factory():
    token_factory = BokkyPooBahsFixedSupplyTokenFactory.deploy({'from': accounts[0]})
    return token_factory


def deploy_auction_token(token_factory):
    symbol = "TT5"
    name = "Test Token"
    totalSupply = 1000000000000000000000000
    tx = token_factory.deployTokenContract(symbol,name,18,totalSupply,{'from': accounts[0], "value": "0.11 ethers"})
    auction_token = FixedSupplyToken.at(web3.toChecksumAddress(tx.events['TokenDeployed']['token']))
    print("FixedSupplyToken deployed at: " + str(auction_token))

    return auction_token


def deploy_dutch_auction_template():
    dutch_auction_template = DutchSwapAuction.deploy({'from': accounts[0]})
    return dutch_auction_template


def deploy_auction_factory(dutch_auction_template):
    auction_factory = DutchSwapFactory.deploy({"from": accounts[0]})
    auction_factory.initDutchSwapFactory(dutch_auction_template, 0, {"from": accounts[0]})
    assert auction_factory.numberOfAuctions( {'from': accounts[0]}) == 0 
    return auction_factory


def deploy_dutch_auction(auction_factory, auction_token):

    wallet = accounts[1]

    auction_token.approve(auction_factory,AUCTION_TOKENS, {"from": accounts[0]})
    tx = auction_factory.deployDutchAuction(auction_token, AUCTION_TOKENS, AUCTION_START,AUCTION_END,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})
    assert 'DutchAuctionDeployed' in tx.events
    dutch_auction = DutchSwapAuction.at(web3.toChecksumAddress(tx.events['DutchAuctionDeployed']['addr']))
    assert dutch_auction.clearingPrice() == AUCTION_START_PRICE
    print("DutchSwap Auction deployed at: " + str(dutch_auction))

    return dutch_auction


def main():
    use_exisiting_contracts = False
    # add accounts if active network is ropsten
    if network.show_active() in ['ropsten', 'rinkeby', 'kovan', 'goerli']:
        # accounts[0] = 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')
        # accounts[1] = 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')

    if network.show_active() == 'mainnet':
        # Import encrypted keyfile for key security
        # (or deploy with burner address and change owner after deployment 
        use_exisiting_contracts = False


    if use_exisiting_contracts == True:
        # Token Factory
        token_factory_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["token_factory"])
        token_factory = BokkyPooBahsFixedSupplyTokenFactory.at(token_factory_address)
        print("BokkyPooBahsFixedSupplyTokenFactory: " + str(token_factory))
 
        # # DutchSwap Factory
        auction_factory_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["auction_factory"])
        auction_factory = DutchSwapFactory.at(auction_factory_address)
        print("DutchSwapFactory: " + str(auction_factory))

    if (CONTRACTS.get(network.show_active()) is None):
        token_factory = deploy_token_factory()
        dutch_auction_template =  deploy_dutch_auction_template()
        auction_factory = deploy_auction_factory(dutch_auction_template)

    auction_token = deploy_auction_token(token_factory)
    dutch_auction = deploy_dutch_auction(auction_factory, auction_token)





