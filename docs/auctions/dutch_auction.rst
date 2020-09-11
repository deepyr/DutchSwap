.. _dutch_auction:

===============
What is a Dutch Auction
===============

First, a little history lesson of how and why Dutch auctions came to be. Dutch auctions arose in the auction houses, cafes and drinking houses of the Netherlands during the Dutch Golden Age. During this period, the Dutch had established themselves as a world power primarily on the back of a maritime trading empire. Dutch traders and merchants had at times sole access to many of the most coveted materials and wares from throughout the world, with the means and infrastructure to enter trade throughout all of Europe.

This unique situation and the massive expanse of trade, financing and market making it brought with it eventually led to the creation of many of the financial institutions we still rely on today - merchant banking, stock markets and futures contracts for example. Crucial in the area of market price discovery in these new and emerging ventures was the creation of the Dutch Auction - originally a mechanism to ensure sellers could move all of their stock for an amount they needed to continue operation, while allowing individuals in the market to dictate a fair investment they were happy with.

We see the growing Ethereum community facing many of the same requirement in how they set prices for the many varied Ethereum and ERC20 token projects out there. We believe that the market should determine the price of a token rather than you or I, that price setting should happen in the open - not in the dark. 
The Dutch Auction mechanism achieves this fairness for two main reasons.:
    - First, at every auction everyone who buys, buys it at the same price.
    - Second, the market determines that price itself. 

These are the characteristics that have kept Dutch auctions in use for 400 years and why we think we can provide a lot of value to the Ethereum community. Although they are not yet so popular in our world, they have already proven themselves for centuries in the fields of business and trade in particular.



How a DutchSwap Auction Works
-------------------------

    - Every auction has a set amount of tokens available to be bought. 
    - The price is initially set at a high price and during the auction continues to drop. 
    - When a buyer bids they are setting their total spend and a maximum individual price for the token.
    - As the individual price continues to drop, buyers total spend stays the same the amount of token they receive increases.
    - The price drops until either all the tokens are sold at auction, or it hits the minimum price set by the seller.


Why would I need a Dutch auction?
----------------------------------
Because this type of auction solves the following problems:

    - The fairest method for selling more than one of the same object.
    - Descending prices ensure bidders will bid early, and honestly. 
    - Lowest bid price for all means people commit what they think it is worth, yet are likely to get it cheaper.
    - Everything is done out in the open, transparency to everyone involved.

.. note::

    **A VERY simple example - V wants to sell 100 tokens. X, Y & Z see value behind this token and wish to take part in a dutch auction of the tokens. Bidding begins at $5 per token, and will drop in price $1 every hour. At $4, X commits to $50 worth of tokens - X sees a deal and doesn't want somebody buying all the tokens up! Nobody else bids however and the auction continues. At $2, Y believes the market will jump in so they bid - $50 worth and the auction ends. Both pay their $50 and receive their tokens. X receives twice as many tokens as they would have at $4, Y receives $50 worth of tokens at a price they're happy with. Z, who waited too long, misses out entirely.**


The biggest benefit of such auctions is that they are meant to democratize public offerings. As it happens currently, the process for conducting a typical IPO is controlled well before it reaches an open market.



Recent Dutch Auctions 
--------------------

The research and development behind DutchSwap was inspired by the Google IPO which was a dutch auction by OpenIPO and both the Algorand and Gnosis dutch auctions.
More details on the Algorand auction mechanism can be found here: `Algo Auction <https://algorand.foundation/algo-auctions>`_ 
We do not support the Algorand refund vault but will do so in v2. 

