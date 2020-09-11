.. _quickstart:

==========
Quickstart
==========

.. note::
    Visit the `DutchSwap Venture Studio <https://dutchswap.com>`_ as you read and try it out for yourself! ", 


This page provides a quick overview of DutchSwap. It assumes a level of familiarity with smart contract development, the Ethereum network and ERC20 tokens and will rely on some simple examples. 
For more in-depth content, continue to the further information under "Getting Started" in the table of contents. **UNDER CONSTRUCTION**

DutchSwap is a smart contract framework for creating Dutch auctions on Ethereum.

The idea of a Dutch auction is to determine a fair price for a batch of items. In particular, new projects and tokens with no previous price are perfect as they allow the market an even playing field for price discovery. Though there are many positives to using a Dutch auction for a fixed supply of any item, this document will cover the creation and auction of a brand new ERC20 token.  

.. note::
    To interact with DutchSwap, you'll first need to connect your Ethereum wallet. DutchSwap support many options for this, but we recommend `Metamask <https://metamask.io/>`_.



1 - Creating a New Token
========================


The first step to using DutchSwap is having a token to sell.
.. note::
    If you already have some ERC20 tokens you wish to sell, continue to step 2.
 
 To mint your own new ERC20 token, you need to do the following:

- Enter your Token’s name
- Add a symbol associated with your token
- Set a total supply

DutchSwap will mint the tokens for you and deposit them into your wallet. After creating your ERC20 tokens, you're ready to set up your auction. 




2 - Starting a Dutch Auction
============================

The process for creating an auction for your token is simple, you only need to follow the next steps:

    - Click "New Auction" tab on the left side of the DutchSwap studio. You will see a window indicating the steps required to create an auction.
    - Enter the details of the ERC20 Token you're wishing to sell. 
    - Set your auction details, including:
        - Amount - quantity of token supply that you want to sell.
        - Prices - set the starting price high and the end price as low as you're willing to go.        
        - Dates - pick appropriative start and end dates for your auction.

    Congratulation! You have created your auction and have full access to its data. Change it whatever is needed and manage your token sale with comfort.


.. note::
    You must be able to transfer the number of tokens for sale to the auction contract, otherwise it will fail.

.. note:: 
    The auction starting price must be greater than the ending price. Dutch auctions start high, and drop in price until sold out. 


3 - Claiming your tokens
========================

The dutch auction ends when the sale ends and the final price is greater or equal to the minimum price of the seller, or if the auction period finishes without all the tokens being sold. 

At the end of the auction, simply click "Claim"

- If the auction was successful, you will claim the tokens you have won at auction. 
- If the auction has ended below the minimum, your claim will be for your original tokens.

