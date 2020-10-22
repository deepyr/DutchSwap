.. meta::
    :keywords: Smart Contracts

.. _auction_factory_contract:

DutchSwap Factory Contract
======================

Functions
-----------

* `function initDutchSwapFactory( address _dutchAuctionTemplate, uint256 _minimumFee)`

Call this function by first passing it the deployed  DutchSwapAuction contract in _dutchAuctionTemplate.

* `function addCustomAuction(address _auction)`

You can add a Dutch Swap Auction you have created without using the `function deployDutchAuction`

* `function removeFinalisedAuction(address _auction)`

Remove the function that has ended or removeFinalisedAuction

* function deployDutchAuction(
        address _token, 
        uint256 _tokenSupply, 
        uint256 _startDate, 
        uint256 _endDate, 
        address _paymentCurrency,
        uint256 _startPrice, 
        uint256 _minimumPrice, 
        address payable _wallet)

The parameters to pass are as follows:

1._token: This is the address of ERC20 Token we just created

2._tokenSupply:The supply of total number of tokens for the auction(uint256). This must be in wei(ie totalSupply * 10**18)

3._startDate: The start date for the auction(uint)

4._endDate: The end date for the auction(uint)]

5._paymentCurrency: Address of the currency you want to be paid with. Can be ethereum address(0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE) or a token address

6._startPrice: Start Price for the token to start auction(in  wei). This should be the maximum price you want your token to be valued at

7._minimumPrice: Minimum price you want the token to be valued at.

8._wallet: The address that you want your payment to be received at if the auction is successfuly. It is also the address that you will receive your tokens at if the auction is not successful.


