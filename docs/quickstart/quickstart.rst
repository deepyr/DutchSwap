.. _quickstart:

==========
Quickstart
==========

This page provides a quick overview of DutchSwap. It relies mostly on examples and assumes a level of familiarity with smart contract dvelopment. 
For more in-depth content, you should read the documentation sections under "Getting Started" in the table of contents.

DutchSwap is a smart contract framework for creating Dutch Auctions on Ethereum.

.. note::

    This framework is based on swapping ETH or ERC20 tokens in batches using a Dutch auction mechanism. To fully understand the documentation of the solution outlined, you must have a basic knowledge of Solidity. In case of any questions or misunderstandings, it is recommended to refer to the corresponding documentation at the link: `Solidity docs <https://solidity.readthedocs.io/en/v0.4.24/index.html>`_

The main idea of a Dutch auction is to determine a fair price for a batch of the same item. Fungible tokens with no previous price are a perfect use case as they will allow for price discovery by the end of the auction. 

If you have any questions about the DutchSwap protocol, feel free to ask on `Gitter <https://gitter.im/dutchswap/community>`_.

Creating your auction
=====================

The first step for you, as for seller is to create auction where you will be able to start business. To do that you only need to follow the next steps.

    - To create an auction, first of all you need to create your account. Click a Signup button and follow the instructions. It’s as simple as that.
    - Each auction is based on a close relationship with the cryptocurrency. Therefore, you need to connect your account with Ethereum wallet. If you don't have your personal Ethereum wallet yet, you need to create it. To do this, we recommend following the documentation of `Metamask <https://metamask.io/>`_. It is the fastest, most reliable and easiest way to start your business.
    - Whether you did this simple setup, you are able to create your first auction. Click the appropriate tab on the left side of the screen. You will see a window indicating the following steps required to create an auction.
    - The first thing you need to enter is a Token. Token - particular fungible and tradable asset or a utility created over an initial coin offering. If you don’t have one yet, you should create it first.
    - Here where your own data should come to place. Decide what should be the best approach for your business and fill the fields:
        - Amount - quantity of token supply that you want to sell.
        - Prices - set the starting price and the end one for your offer.
        
        .. note::

            Remember that the starting price must be higher than the ending price.
        
        - Dates - pick appropriative dates for your auction
    - Congratulation on this! Now you have created your auction and have full access to its data. Change it whatever it needed and manage your business with comfort.




Creating a New Token
====================

    Token is one of the most important components of smart contracts.

    `Main article:` :ref:`init`

The first step to using DutchSwap is to create a new token.

To setup token, you need to enter required data in the appropriative fields.

.. note::

    Keep in mind that DutchSwap will automatically receive the address of your Ethereum wallet connected to your account.

    - It starts with entering Token’s name - should be unique value(such as Tether, Chainlink).
    - After that put in a symbol associated with your token. It should be in uppercase and consist not more than from 3 symbols
    - In the next step, you have the option to set decimals. It defines digits in the fraction part. Recommended value is 18.

.. note::

    After creating your special token, you will be able to use it directly in newly created auctions



Improving our project
=====================

Our project is constantly evolving. Every month more and more features are added to it and it becomes larger and larger. It is no surprise that competent specialists in this field are needed to develop such a large project.

If you found any bug or you know how to make this project better, we are ready to listen your suggestions.

If you are an excellent blockchain specialist and have a desire to participate in the development of the project, feel free to contact us to discuss the details of cooperation.

Support
=======

If you have ever got stuck at working with auction or you found flaws in the mechanism of the algorithm feel free to contact us by the links below.


You can visit the "`DutchSwap Studio <https://dutchswap.com>`_", 
