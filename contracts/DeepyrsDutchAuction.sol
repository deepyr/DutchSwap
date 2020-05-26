pragma solidity ^0.6.2;

import "./SafeMath.sol";
import "../../interfaces/IMintableToken.sol";


// ------------------------------------------------------------------
// Deepyr's Dutch Auction
//
//
// MVP prototype. DO NOT USE!
//                        
// (c) Adrian Guerrera.  MIT Licence.                            
// May 26 2020                                  
// ------------------------------------------------------------------


contract DeepyrsDutchAuction  {

    using SafeMath for uint256;
    uint256 private constant TENPOW18 = 10 ** 18;

    uint256 public amountRaised;
    uint256 public startDate;
    uint256 public endDate;
    uint256 public startPrice;
    uint256 public minimumPrice;
    uint256 public tokenSupply;
    IMintableToken public token; 
    address payable public wallet;
    mapping(address => uint256) public commitments;

    event AddedCommitment(address addr, uint256 commitment);

    /// @dev Init function 
    function initDutchAuction(
        address _token, 
        uint256 _tokenSupply, 
        uint256 _startDate, 
        uint256 _endDate, 
        uint256 _startPrice, 
        uint256 _minimumPrice, 
        address payable _wallet
    ) 
        external 
    {
        require(_endDate > _startDate);
        require(_startPrice > _minimumPrice);
        token = IMintableToken(_token);
        tokenSupply =_tokenSupply;
        startDate = _startDate;
        endDate = _endDate;
        startPrice = _startPrice;
        minimumPrice = _minimumPrice; 
        wallet = _wallet;
    }

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
        uint256 priceFunction = startPrice.sub(priceDiff);
        return priceFunction;
    }

    /// @notice The current Dutch auction price
    function auctionPrice() public view returns (uint256) {
        /// @dev If auction successful, return tokenPrice
        if (tokenPrice() > priceFunction()) {
            return tokenPrice();
        }
        return priceFunction();
    }

    /// @notice How many tokens the user is able to claim
    function tokensClaimable(address _user) public view returns (uint256) {
        return commitments[_user].mul(TENPOW18).div(auctionPrice());
    }

    /// @notice Total amount of tokens committed at current auction price
    function totalTokensCommitted() public view returns(uint256) {
        return amountRaised.mul(TENPOW18).div(auctionPrice());
    }


    /// @notice Returns bool if amount committed exceeds tokens available
    function auctionEnded() public view returns (bool){
        return now > endDate;
    }

    /// @notice Returns bool if amount committed exceeds tokens available
    function auctionSuccessful() public view returns (bool){
        return totalTokensCommitted() >= tokenSupply;
    }

 
    /// @notice Buy Tokens by committing ETH to this contract address 
    receive () external payable {
        require(now >= startDate && now <= endDate);
        // Get ETH able to be committed
        uint256 ethToTransfer = calculateCommitment( msg.value);

        // Accept ETH Payments
        uint256 ethToRefund = msg.value.sub(ethToTransfer);
        if (ethToTransfer > 0) {
            addCommitment(msg.sender, ethToTransfer);
        }
        // Return any ETH to be refunded
        if (ethToRefund > 0) {
            msg.sender.transfer(ethToRefund);
        }
    }

    /// @notice Returns the amout able to be committed during an auction
    function calculateCommitment( uint256 _commitment) 
        public view returns (uint256 committed) 
    {
        uint256 maxCommitment = tokenSupply.mul(auctionPrice()).div(TENPOW18);
        if (amountRaised.add(_commitment) > maxCommitment) {
            return maxCommitment.sub(amountRaised);
        }
        return _commitment;
    }

    /// @notice Commits to an amount during an auction
    function addCommitment(address _addr,  uint256 _commitment) internal {
        commitments[_addr] = commitments[_addr].add(_commitment);
        amountRaised = amountRaised.add(_commitment);
        emit AddedCommitment(_addr, _commitment);
    }


    /// @notice Auction finishes successfully above the reserve
    /// @dev Transfer contract funds to initialised wallet. 
    function finaliseAuction () public {
        require(auctionSuccessful());
        wallet.transfer(amountRaised);        
   
    }

    /// @notice Withdraw your tokens once the Auction has ended.
    function withdrawTokens() public  {
        uint256 fundsCommitted = commitments[ msg.sender];
        uint256 tokensToClaim = tokensClaimable(msg.sender);
        commitments[ msg.sender] = 0;

        /// @notice Auction did not meet reserve price.
        /// @dev Return committed funds back to user.
        if( auctionEnded() && tokenPrice() < minimumPrice ) {
            msg.sender.transfer(fundsCommitted);
            return ;        
        }
        /// @notice Successful auction! Mint tokens owed.
        if (auctionSuccessful() && tokensToClaim > 0 ) {
            token.mint( msg.sender,tokensToClaim);
        }
    }

}