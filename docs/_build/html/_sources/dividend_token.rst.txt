
===============
Dividned Tokens
===============
Dividend tokens are base tokens with additional functions to both accept and distribute funds to token holders.
Due to the internal accounting required to keep track of who is owed what amount, dividend tokens must be minted or converted from base tokens using a token conerter. 

Functions
=========
Full list of functions can be found in the Referrence docs. 

Deposit Dividends
=================
Accepts both ERC20 tokens and ETH
Limited to a set number of ERC20 tokens in V1 due to gas constraints and security implications.
Only the owner can add new ERC20 tokens to be accepted and paid out. 

Withdraw Funds
==============
Anyone can pull out the amount of tokens they have earnt over the time of holding a dividend token. 
Transfers are precomputed with dividends owing paid out first before sending to another party.




