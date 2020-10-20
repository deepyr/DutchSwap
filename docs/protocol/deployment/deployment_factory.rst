.. meta::
    :keywords: deployment scripts

.. _deployment_factory_scripts:

Dutchswap Factory Deployment
================================

Environment
-------------------------------------------
**Local Environment Setup** 

This needs to set up with the following requirements:

* `Install brownie  <https://eth-brownie.readthedocs.io/en/stable/install.html>`_
* `Install Ganache CLI <https://www.npmjs.com/package/ganache-cli>`_

Scripts
---------
We have already deployed Dutchswap Factory Contract for the respective testnet and also in mainnet

The links to addresses are Deployed Smart Contract page. 

If you want to deploy your own Factory Contracts please take these steps:

Deploy ERC20 Token Factory
------------------------------

* We have a token factory smart contract **BokkyPooBahsFixedSupplyTokenFactory**. First lets deploy it::
    
    token_factory = BokkyPooBahsFixedSupplyTokenFactory.deploy({'from': accounts[0]})

Deploy Dutch Auction Factory:
---------------------------------

* First we create a template for dutch auction by deploying DutchSwapAuction smart contract::

    dutch_auction_template = DutchSwapAuction.deploy({'from': accounts[0]})

* We deploy the DutchSwapFactory contract to create a new Dutch Swap Auction::

    auction_factory = DutchSwapFactory.deploy({"from": accounts[0]})

* We initialize our DutchSwapFactory with dutch_auction_template we created::
    
    auction_factory.initDutchSwapFactory(dutch_auction_template, 0, {"from": accounts[0]})

Okay, so we have created a token factory to supply to our Auction and a Auction Factory to create an auction.
Please follow this link for further deployment:

:ref:`deployment_auction`_
