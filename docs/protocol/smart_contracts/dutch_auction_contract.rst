.. meta::
    :keywords: Smart Contracts

.. _dutch_auction_contract:

Dutch Auction Contract
======================

initDutchAuction
---------

This initialises the smart contract, can only be called once. 

::
    function initDutchAuction(
        address _token, 
        uint256 _tokenSupply, 
        uint256 _startDate, 
        uint256 _endDate,
        address _paymentCurrency, 
        uint256 _startPrice, 
        uint256 _minimumPrice, 
        address payable _wallet ) external {
            // ...
        }


Getters
-------

tokenPrice:: 
    function tokenPrice() public view returns (uint256) { .. }

priceGradient:: 
    function priceGradient() public view returns (uint256) {
