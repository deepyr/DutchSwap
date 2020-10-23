.. meta::
    :keywords: Smart Contracts

.. _dutch_auction_contract:

Dutch Auction Contract
======================
First we deploy the Dutch Auction Contract to the blockchain. And we use it as a template to supply it to Dutch Auction Factory

The factory contract is explained in :ref:`auction_factory_contract`

The Dutch Auction is deployed using the function `deployDutchAuction` of the factory.

The function `deployDutchAuction` initializes the contract using the function initDutchAuction

initDutchAuction
-----------------

This initialises the smart contract::

    function initDutchAuction(
        address _funder,
        address _token,
        uint256 _totalTokens,
        uint256 _startDate,
        uint256 _endDate,
        address _paymentCurrency,
        uint256 _startPrice,
        uint256 _minimumPrice,
        address payable _wallet
    )

Here,

1._funder: This is the address of the factory that creates the Dutch Auction. The factory needs to be given approval by the funder(msg.sender) to spend the tokens on the funders behalf

2._token: The address of the token

3._totalTokens: The amount of supply of the tokens. It is in wei (ie totalSupply * 10**18)

4._startDate: The start date for the auction

5._endDate: The end date for the auction

6._paymentCurrency: Address of the currency you want to be paid with. Can be ethereum address(0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE) or a token address

7._startPrice: Start Price for the token to start auction(in  wei). This should be the maximum price you want your token to be valued at

8._minimumPrice: Minimum price you want the token to be valued at.

9._wallet: The address that you want your payment to be received at if the auction is successfuly. It is also the address that you will receive your tokens at if the auction is not successful.

Get Token Price:
------------------
* `function priceFunction()`

Returns price during the auction which proportionaly decreases as the time elapses.

* `function clearingPrice()`

The current clearing price of the Dutch auction. If the auction is successful, it returns the actual token price.

* `function tokenPrice()`

The average price of each token. It is derived by dividing total commitments by total tokens. The total commitment is the amount of tokens or ethers commited to the contract

Get Tokens available
-------------------------
* `function tokensClaimable(address _user)`

The number of tokens the user is able to claim. It is given by the total commitment of the user divided by the price of token(clearing price)

* `function tokensRemaining()`

Total amount of tokens left for auction

* `function totalTokensCommitted()`

Total amount of tokens committed at current auction price

How to Buy a token
---------------------

* `function commitEth() public payable`

Commit ETH to buy tokens for any address. It calculates the commitment based on the amount of ether we give to the smart contract. If we commit ethers that is greater than the maximum commitment available this function will refund

Finally it will add how much a user has commited to commitments mapping

*  `function commitTokens(uint256 _amount)`

Users must approve contract prior to committing tokens to auction. It calculates the commitment based on the amount of token we want to buy with.

Determine the commitments
--------------------------------
* `function calculateCommitment( uint256 _commitment)`

Returns the amount able to be committed during an auction. If the commitment is bigger than the maximum commitment it will subtract the surplus.

Getters
----------------------

* `function auctionSuccessful() public view returns (bool)`

Returns successful if the tokens sold equals total Tokens. That is to say the token price is greater than or equal to the clearing price.

* `function auctionEnded() public view returns (bool)`

Returns bool if auction is successful or time has ended

Finalizing the auction
------------------------

* `function finaliseAuction () public`

If the auction has successfuly finished above the reserve, then transfer the total commitments to the initialized wallet

If the function has cancelled or failed, transfer total tokens back, ie to initialized wallet

* `function withdrawTokens()`

If the auction has successfuly finished, transfer the claimed tokens to the bidders.

If the auction did not meet the reserved price, return the commited funds back to bidders.










