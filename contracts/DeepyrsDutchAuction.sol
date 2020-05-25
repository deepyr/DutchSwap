pragma solidity ^0.6.2;

import "./SafeMath.sol";
import "../../interfaces/IMintableToken.sol";


// ----------------------------------------------------------------------------
// Deepyr's Dutch Auction
//
//
// MVP prototype. DO NOT USE!
//                        
// (c) Adrian Guerrera.  MIT Licence.                            
// May 26 2020                                  
// ----------------------------------------------------------------------------


contract DeepyrsDutchAuction  {

    using SafeMath for uint256;
    uint256 private constant TENPOW18 = 10 ** 18;

    uint256 public totalCommitments;
    uint256 public startDate;
    uint256 public endDate;
    uint256 public startPrice;
    uint256 public reservePrice;
    uint256 public tokensAvailable;
    IMintableToken public token; 
    address payable public wallet;
    mapping(address => uint256) public commitments;

    event AddedCommitment(address addr, uint256 commitment);

    /// @dev Init function 
    function initDutchAuction(address _token, uint256 _tokensAvailable, uint256 _startDate, uint256 _endDate, uint256 _startPrice, uint256 _reservePrice, address payable _wallet) external {
        require(_endDate > _startDate);
        require(_startPrice > _reservePrice);
        token = IMintableToken(_token);
        tokensAvailable =_tokensAvailable;
        startDate = _startDate;
        endDate = _endDate;
        startPrice = _startPrice;
        reservePrice = _reservePrice; 
        wallet = _wallet;
    }

    /// @notice Token price decreases at this rate during auction.
    function invGradient() public view returns (uint256) {
        uint256 numerator = startPrice.sub(reservePrice);
        uint256 denominator = endDate.sub(startDate);
        return numerator.div(denominator);
    }

    /// @notice Returns price during the auction 
    function auctionPrice() public view returns (uint256) {
        if (now <= startDate) {
            return startPrice;
        }
        if (now >= endDate) {
            return reservePrice;
        }
        uint256 priceDiff = now.sub(startDate).mul(invGradient());
        uint priceFunction = startPrice.sub(priceDiff);
        if (tokenPrice() > priceFunction) {
            return tokenPrice();
        }
        return priceFunction;
    }

    /// @notice Current amount of tokens committed for a given auction price
    function tokensClaimed() public view returns(uint256) {
        return totalCommitments.mul(TENPOW18).div(auctionPrice());
    }

    /// @notice The average price of each token from all commitments. 
    function tokenPrice() public view returns (uint256) {
        return totalCommitments.mul(TENPOW18).div(tokensAvailable);
    }

    /// @notice How many tokes the user is 
    function tokensClaimable(address _user) public view returns (uint256) {
        if(commitments[_user] == 0) {
            return 0;
        }
        return commitments[_user].mul(TENPOW18).div(tokenPrice());
    }

    /// @notice Returns bool if amount committed exceeds tokens available
    function auctionEnded() public view returns (bool){
        return now >= endDate;
    }

    /// @notice Returns bool if amount committed exceeds tokens available
    function auctionSuccessful() public view returns (bool){
        return tokensClaimed() >= tokensAvailable;
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
    function calculateCommitment( uint256 _commitment) public view returns (uint256 committed) {
        uint256 maxCommitment = tokensAvailable.mul(auctionPrice()).div(TENPOW18);
        if (totalCommitments.add(_commitment) >= maxCommitment) {
            return maxCommitment.sub(totalCommitments);
        }
        return _commitment;
    }

    /// @notice Commits to an amount during an auction
    function addCommitment(address _addr,  uint256 _commitment) internal {
        commitments[_addr] = commitments[_addr].add(_commitment);
        totalCommitments = totalCommitments.add(_commitment);
        emit AddedCommitment(_addr, _commitment);
    }


    /// @notice Auction finishes successfully, above the reserve, then transfer funds to wallet. 
    /// @dev This doesnt nessasarily have to have an auctionEnded requirement. 
    function finaliseAuction () public {
        require(auctionSuccessful());
        wallet.transfer(totalCommitments);        
   
    }

    /// @notice 
    function claim() public  {
        uint256 fundsCommitted = commitments[ msg.sender];
        uint256 tokensToClaim = tokensClaimable(msg.sender);
        commitments[ msg.sender] = 0;

        /// @notice Auction ended below reserve price, return funds.
        if( auctionEnded() && tokenPrice() < reservePrice ) {
            msg.sender.transfer(fundsCommitted);
            return ;        
        }
        /// @notice Successful auction! Mint tokens owed.
        if (auctionSuccessful() && tokensToClaim > 0 ) {
            token.mint( msg.sender,tokensToClaim);
        }
    }

}