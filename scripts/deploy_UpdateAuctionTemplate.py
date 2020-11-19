from brownie import *
from .contract_addresses import *
import time


TENPOW18 = 10 ** 18
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
ETH_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'


def deploy_dutch_auction_template():
    dutch_auction_template = DutchSwapAuction.deploy({'from': accounts[0]})
    return dutch_auction_template

def deploy_auction_factory(dutch_auction_template):
    auction_factory = DutchSwapFactory.deploy({"from": accounts[0]})
    auction_factory.initDutchSwapFactory(dutch_auction_template, 0, {"from": accounts[0]})
    assert auction_factory.numberOfAuctions( {'from': accounts[0]}) == 0 
    return auction_factory

def update_auction_template(auction_factory, dutch_auction_template):
    auction_factory.setDutchAuctionTemplate(dutch_auction_template, {"from": accounts[0]})
    return auction_factory


def main():
    use_exisiting_auction_factory = True
    # add accounts if active network is ropsten
    if network.show_active() in ['ropsten', 'rinkeby', 'kovan', 'goerli']:
        # accounts[0] = 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')
        # accounts[1] = 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')

    if network.show_active() == 'mainnet':
        accounts.load("dutchswap")
        # Import encrypted keyfile for key security
        # (or deploy with burner address and change owner after deployment         
    
    # DutchSwap Factory
    if use_exisiting_auction_factory == True:
        auction_factory_address = web3.toChecksumAddress(CONTRACTS[network.show_active()]["auction_factory"])
        auction_factory = DutchSwapFactory.at(auction_factory_address)
        print("DutchSwapFactory: " + str(auction_factory))
    else:
        auction_factory = deploy_auction_factory(dutch_auction_template)

    dutch_auction_template =  deploy_dutch_auction_template()
    dutch_auction = update_auction_template(auction_factory, dutch_auction_template)

