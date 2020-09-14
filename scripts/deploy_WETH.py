from brownie import *
import time


def deploy_weth_token():
    weth_token = WETH9.deploy({'from': accounts[0]})
    return weth_token


def main():
    # add accounts if active network is ropsten
    if network.show_active() == 'ropsten':
        # 0x2A40019ABd4A61d71aBB73968BaB068ab389a636
        accounts.add('4ca89ec18e37683efa18e0434cd9a28c82d461189c477f5622dae974b43baebf')

        # 0x1F3389Fc75Bf55275b03347E4283f24916F402f7
        accounts.add('fa3c06c67426b848e6cef377a2dbd2d832d3718999fbe377236676c9216d8ec0')


    weth_token = deploy_weth_token()




# Running 'Users.adrian.Documents.GitHub.DutchSwapDeepyr.scripts.deploy_WETH.main'...
# Transaction sent: 0x738124a81a0793fd587cb52f96e647d3b8724ee1ef17d0acf1e8da10cd803d8b
#   Gas price: 1.0 gwei   Gas limit: 505999
# Waiting for confirmation...
#   WETH9.constructor confirmed - Block: 8572996   Gas used: 505999 (100.00%)
#   WETH9 deployed at: 0xbf81FD58BAC258905f052DEd3F6535Ea25336Fb3