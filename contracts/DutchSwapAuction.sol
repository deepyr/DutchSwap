pragma solidity ^0.6.9;
// SPDX-License-Identifier: GPL-3.0-or-later

import "./SafeMath.sol";
import "../../interfaces/IERC20.sol";


// ----------------------------------------------------------------------------
// DutchSwap Auction Contract
//
//
// MVP prototype. DO NOT USE!
//                        
// (c) Adrian Guerrera. Deepyr Pty Ltd.                          
// May 26 2020                                  
// ----------------------------------------------------------------------------


contract DutchSwapAuction  {

    using SafeMath for uint256;
    uint256 private constant TENPOW18 = 10 ** 18;
    /// @dev The placeholder ETH address.
    address private constant ETH_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    uint256 public amountRaised;
    uint256 public startDate;
    uint256 public endDate;
    uint256 public startPrice;
    uint256 public minimumPrice;
    uint256 public tokenSupply;
    bool public finalised;
    IERC20 public auctionToken; 
    IERC20 public paymentCurrency; 
    address payable public wallet;
    mapping(address => uint256) public commitments;

    event AddedCommitment(address addr, uint256 commitment, uint256 price);

    /// @dev Init function 
    function initDutchAuction(
        address _token, 
        uint256 _tokenSupply, 
        uint256 _startDate, 
        uint256 _endDate,
        address _paymentCurrency, 
        uint256 _startPrice, 
        uint256 _minimumPrice, 
        address payable _wallet
    ) 
        external 
    {
        require(_endDate > _startDate);
        require(_startPrice > _minimumPrice);
        require(_minimumPrice > 0);

        auctionToken = IERC20(_token);
        paymentCurrency = IERC20(_paymentCurrency);

        require(IERC20(auctionToken).transferFrom(msg.sender, address(this), _tokenSupply));

        tokenSupply =_tokenSupply;
        startDate = _startDate;
        endDate = _endDate;
        startPrice = _startPrice;
        minimumPrice = _minimumPrice; 
        wallet = _wallet;
        finalised = false;
    }


    // Dutch Auction Price Function
    // ============================
    //  
    // Start Price ----- 
    //                   \ 
    //                    \
    //                     \
    //                      \ ------------ Clearing Price
    //                     / \            = AmountRaised/TokenSupply
    //      Token Price  --   \
    //                  /      \ 
    //                --        ----------- Minimum Price
    // Amount raised /          End Time
    //

    /// @notice The average price of each token from all commitments. 
    function tokenPrice() public view returns (uint256) {
        return amountRaised.mul(TENPOW18).div(tokenSupply);
    }

    /// @notice Token price decreases at this rate during auction.
    function priceGradient() public view returns (uint256) {
        uint256 numerator = startPrice.sub(minimumPrice);
        uint256 denominator = endDate.sub(startDate);
        return numerator.div(denominator);
    }

      /// @notice Returns price during the auction 
    function priceFunction() public view returns (uint256) {
        /// @dev Return Auction Price
        if (now <= startDate) {
            return startPrice;
        }
        if (now >= endDate) {
            return minimumPrice;
        }
        uint256 priceDiff = now.sub(startDate).mul(priceGradient());
        uint256 price = startPrice.sub(priceDiff);
        return price;
    }

    /// @notice The current clearing price of the Dutch auction
    function clearingPrice() public view returns (uint256) {
        /// @dev If auction successful, return tokenPrice
        if (tokenPrice() > priceFunction()) {
            return tokenPrice();
        }
        return priceFunction();
    }

    /// @notice How many tokens the user is able to claim
    function tokensClaimable(address _user) public view returns (uint256) {
        return commitments[_user].mul(TENPOW18).div(clearingPrice());
    }

    /// @notice Total amount of tokens committed at current auction price
    function totalTokensCommitted() public view returns(uint256) {
        return amountRaised.mul(TENPOW18).div(clearingPrice());
    }

    /// @notice Successful if tokens sold equals tokenSupply
    function auctionSuccessful() public view returns (bool){
        return totalTokensCommitted() >= tokenSupply && tokenPrice() >= minimumPrice;
    }

    /// @notice Returns bool if successful or time has ended
    function auctionEnded() public view returns (bool){
        return auctionSuccessful() || now > endDate;
    }

    //--------------------------------------------------------
    // Commit to buying tokens 
    //--------------------------------------------------------

    /// @notice Buy Tokens by committing ETH to this contract address 
    receive () external payable {
        commitEth(msg.sender);
    }

    /// @notice Commit ETH to buy tokens on sale
    function commitEth (address payable _from) public payable {
        require(address(paymentCurrency) == ETH_ADDRESS);
        // Get ETH able to be committed
        uint256 ethToTransfer = calculateCommitment( msg.value);

        // Accept ETH Payments
        uint256 ethToRefund = msg.value.sub(ethToTransfer);
        if (ethToTransfer > 0) {
            addCommitment(_from, ethToTransfer);
        }
        // Return any ETH to be refunded
        if (ethToRefund > 0) {
            _from.transfer(ethToRefund);
        }
    }

    /// @notice Commits to an amount during an auction
    function addCommitment(address _addr,  uint256 _commitment) internal {
        require(now >= startDate && now <= endDate);
        commitments[_addr] = commitments[_addr].add(_commitment);
        amountRaised = amountRaised.add(_commitment);
        emit AddedCommitment(_addr, _commitment, tokenPrice());
    }

    /// @notice Commit approved ERC20 tokens to buy tokens on sale
    function commitTokens (uint256 _amount) public {
        commitTokensFrom(msg.sender, _amount);
    }

    /// @dev Users must approve contract prior to committing tokens to auction
    function commitTokensFrom (address _from, uint256 _amount) public {
        require(address(paymentCurrency) != ETH_ADDRESS);
        uint256 tokensToTransfer = calculateCommitment( _amount);
        if (tokensToTransfer > 0) {
            require(IERC20(paymentCurrency).transferFrom(_from, address(this), _amount));
            addCommitment(_from, tokensToTransfer);
        }
    }

    /// @notice Returns the amout able to be committed during an auction
    function calculateCommitment( uint256 _commitment) 
        public view returns (uint256 committed) 
    {
        uint256 maxCommitment = tokenSupply.mul(clearingPrice()).div(TENPOW18);
        if (amountRaised.add(_commitment) > maxCommitment) {
            return maxCommitment.sub(amountRaised);
        }
        return _commitment;
    }


    //--------------------------------------------------------
    // Finalise Auction
    //--------------------------------------------------------

    /// @notice Auction finishes successfully above the reserve
    /// @dev Transfer contract funds to initialised wallet. 
    function finaliseAuction () public {
        require(!finalised); 
        finalised = true;

        /// @notice Auction did not meet reserve price.
        if( auctionEnded() && tokenPrice() < minimumPrice ) {
            _tokenPayment(auctionToken, wallet, tokenSupply);       
            return;      
        }
        /// @notice Successful auction! Transfer tokens bought.
        if (auctionSuccessful()) {
            _tokenPayment(paymentCurrency, wallet, amountRaised);
        }

    }

    /// @notice Withdraw your tokens once the Auction has ended.
    function withdrawTokens() public {
        uint256 fundsCommitted = commitments[ msg.sender];
        uint256 tokensToClaim = tokensClaimable(msg.sender);
        commitments[ msg.sender] = 0;

        /// @notice Auction did not meet reserve price.
        /// @dev Return committed funds back to user.
        if( auctionEnded() && tokenPrice() < minimumPrice ) {
            _tokenPayment(paymentCurrency, msg.sender, fundsCommitted);       
            return;      
        }
        /// @notice Successful auction! Transfer tokens bought.
        /// @dev AG: Should hold and distribute tokens vs mint
        /// @dev AG: Could be only > min to allow early withdraw  
        if (auctionSuccessful() && tokensToClaim > 0 ) {
            _tokenPayment(auctionToken, msg.sender, tokensToClaim);
        }
    }

    /// @dev Helper function to handle both ETH and ERC20 payments
    function _tokenPayment(IERC20 _token, address payable _to, uint256 _amount) internal {
        if (address(_token) == ETH_ADDRESS) {
            _to.transfer(_amount); 
        } else {
            require(_token.transfer(_to, _amount));
        }
    }

}