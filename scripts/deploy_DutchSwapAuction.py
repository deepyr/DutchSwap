from brownie import *
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



def deploy_dutch_auction_template():
    dutch_auction_template = DutchSwapAuction.deploy({'from': accounts[0]})
    return dutch_auction_template


def deploy_auction_factory(dutch_auction_template):
    auction_factory = DutchSwapAuctionFactory.deploy({"from": accounts[0]})
    auction_factory.initDutchAuctionFactory(dutch_auction_template, 0, {"from": accounts[0]})
    assert auction_factory.numberOfAuctions( {'from': accounts[0]}) == 0 
    return auction_factory


def deploy_dutch_auction(auction_factory, auction_token):

    wallet = accounts[1]
    tx = auction_factory.deployDutchAuction(auction_token, AUCTION_TOKENS, AUCTION_START,AUCTION_END,ETH_ADDRESS, AUCTION_START_PRICE, AUCTION_RESERVE, wallet, {"from": accounts[0]})

    dutch_auction = DutchSwapAuction.at(web3.toChecksumAddress(tx.events['DutchAuctionDeployed']['addr']))
    assert dutch_auction.clearingPrice() == AUCTION_START_PRICE
    return dutch_auction


def deploy_auction_token():
    auction_token = BokkyPooBahsFixedSupplyTokenFactory.deployTokenContract(
       symbol, name,18,totalSupply, {'from': accounts[0]})
    return auction_token



def main():
    # add accounts if active network is ropsten
    if network.show_active() == 'ropsten':
        # accounts[0] = 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')
        # accounts[1] = 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')

        # Token Factory
        token_factory_address = web3.toChecksumAddress('0x0A75F8dB4084263ed7dd8a3C44881cE279e85340')
        token_factory = BokkyPooBahsFixedSupplyTokenFactory.at(auction_factory_address)

        # DutchSwap Template
        auction_template_address = web3.toChecksumAddress('0x95Efabf64e483634314BbC638CD22E749ce4bb05')
        dutch_auction_template = DutchSwapAuction.at(auction_template_address)
 
        # DutchSwap Factory
        auction_factory_address = web3.toChecksumAddress('0x0A75F8dB4084263ed7dd8a3C44881cE279e85340')
        auction_factory = DutchAuctionFactory.at(auction_factory_address)
    
    if network.show_active() == 'mainnet':
        # Import encrypted keyfile for key security
        # (or deploy with burner address and change owner after deployment 

        # Token Factory
        token_factory_address = web3.toChecksumAddress('0xA550114ee3688601006b8b9f25e64732eF774934')
        token_factory = DutchAuctioBokkyPooBahsFixedSupplyTokenFactorynFactory.at(auction_factory_address)



    auction_token = deploy_auction_token()
    dutch_auction_template =  deploy_dutch_auction_template()
    auction_factory = deploy_auction_factory(dutch_auction_template)
    dutch_auction = deploy_dutch_auction(auction_factory, auction_token)





