.. _quickstart:

==========
Quickstart
==========

This page provides a quick overview of DutchSwap. It relies mostly on examples and assumes a level of familiarity with smart contract dvelopment. 
For more in-depth content, you should read the documentation sections under "Getting Started" in the table of contents.

DutchSwap is a smart contract framework for creating Dutch Auctions on Ethereum.

.. note::

    This framework is based on swapping ETH or ERC20 tokens in batches using a Dutch auction mechanism. To fully understand the documentation of the solution outlined, you must have a basic knowledge of what a ERC20 token is and how to use Ethereum

The main idea of a Dutch auction is to determine a fair price for a batch of the items. The same item to be specific. 400 years ago it would have been batches of tulips. Today, tokens with no previous price are a perfect, as they will allow for price discovery by the end of the auction. 


.. note::
    You can visit the "`DutchSwap Venture Studio <https://dutchswap.com>`_", 



1 - Creating a New Token
========================


The first step to using DutchSwap is having a token to sell.

.. note::
    If you already have some ERC20 tokens you wish to sell, continue to step 2.

To mint your own new ERC20 token, you need to do the following.


- Connect your wallet using metamask

- Enter your Token’s name - should be unique string.
- Add a symbol associated with your token. It should be in all uppercase and 3-5 symbols long (ie TKN)
- Set a total supply. This will be the number of tokens you mint initially. 



After creating your ERC20 tokens, you will be able to sell some of them in a Dutch auction. 




2 - Starting a Dutch Auction
============================

The first step for you, as for seller is to have a token you wish to sell. To do that you only need to follow the next steps.

    - Connect your Ethereum wallet if you havent already. If you don't have your Ethereum wallet yet, you need to create one. To do this, we recommend `Metamask <https://metamask.io/>`_. It is the fastest, most reliable and easiest way to get started with anything build on the Ethereum.
    - Click "New Auction" tab on the left side of the DutchSwap studio. You will see a window indicating the following steps required to create an auction.
    - The first thing you need to enter is an ERC20 Token. If you don’t have one yet, you should create it first by going back to step 1. 
    - Fill the following fields:
        - Amount - quantity of token supply that you want to sell.
        - Prices - set the starting price and the end one for your offer.        
        - Dates - pick appropriative dates for your auction
    - Congratulation on this! Now you have created your auction and have full access to its data. Change it whatever it needed and manage your business with comfort.


.. note::
    You must be able to transfer the number of tokens for sale to the auction contract, otherwise it will fail.

.. note:: 
    The auction starting price must be greater than the ending price. Dutch auctions start high, and drop in price until sold out. 


3 - Claiming your tokens
========================

The dutch auction ends when the sale ends and the final price is greater or equal to the minimum price of the seller. 

To claim your tokens, go to the token auction page and click "Claim"

- If the auction was successful, you will claim the tokens you have won at auction, based on how much you contributed. 

- If the auction has ended below the minimum, your claim will be for your original tokens.


DutchSwap Studio
================

If you have ever got stuck at working with auction please have a look throughout the Studio UI


You can visit the "`DutchSwap Studio <https://dutchswap.com>`_", 
