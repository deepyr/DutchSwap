from brownie import *
import time


def deploy_proxy_admin():
    proxy_admin = ProxyAdmin.deploy({'from': accounts[0]})
    return proxy_admin

def deploy_proxy(contract, proxy_admin):
    proxy = TransparentUpgradeableProxy.deploy(contract, proxy_admin, "",{'from': accounts[0]})
    return proxy

def deploy_auction_factory():
    dutch_auction_template =  DutchSwapAuction.deploy({'from': accounts[0]})
    auction_factory = DutchSwapFactory.deploy({"from": accounts[0]})
    auction_factory.initDutchSwapFactory(dutch_auction_template, 0, {"from": accounts[0]})
    assert auction_factory.numberOfAuctions( {'from': accounts[0]}) == 0 
    return auction_factory


def main():
    # add accounts if active network is ropsten
    if network.show_active() == 'ropsten':
        # 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')

        # 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')


    proxy_admin = deploy_proxy_admin()
    auction_factory = deploy_auction_factory()
    proxy = deploy_proxy(auction_factory, proxy_admin)