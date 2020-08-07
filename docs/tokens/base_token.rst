.. _base_token:

===========
Base Tokens
===========

Most ERC20 tokens can be sold in a dutch Auction. For those without exisitng tokens, our token factory can mint Base Tokens. 
Base token type is an ERC20 token from the DutchSwap protocol. It is essentially an ERC20 with some advanced features from the ERC777 standard and some bonus code to make them work with the DutchSwap contract. 

Minting a Base Token
====================

To mint your own can be done using the Token Factory.


Functions
=========
Full list of functions can be found in the Referrence docs. 

Send vs Transfer 
================
This is a naming convention from both ERC20 and ERC777 which is used to distinguish them. We have included both the Transfered and Sent events to comply with both standards. 



ERC1820 Registry
================
This is a key part of the ERC777 standard and used as a hook for additional functionality within the DutchSwap protocol.
