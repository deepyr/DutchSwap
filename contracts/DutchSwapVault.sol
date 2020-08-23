pragma solidity ^0.6.9;

import "./Utils/SafeMath.sol";
import "../interfaces/IERC20.sol";
import "../interfaces/IPetylAuction.sol";

// SPDX-License-Identifier: GPL-3.0-or-later

// ----------------------------------------------------------------------------
// Petyl Token Vault
// Get a refund for a percentage of tokens after a set time
// NOT FINISHED!
//
// MVP prototype. DO NOT USE!
//                        
// (c) Adrian Guerrera. Deepyr Pty Ltd.  
// From Petyl Protocol
// https://github.com/deepyr/petyl
//                          
// May 26 2020                                  
// ----------------------------------------------------------------------------


contract DutchSwapVault {

    using SafeMath for uint256;
    uint256 private constant TENPOW18 = 10 ** 18;
    /// @dev The placeholder ETH address.
    address private constant ETH_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    // ERC20 basic token contract being held
    IDutchAuction public auction;
    IERC20 public auctionToken; 
    IERC20 public paymentCurrency; 

    // timestamp when token refund is enabled
    bool private initialised;
    uint256 public refundTime;
    uint256 public refundRate;
    mapping(address => uint256) private refunded;


    /**
     * @notice Initialise contract parameters
     */
    function initDutchVault ( IDutchAuction _auction, uint256 _amountToRefund, uint256 _refundTime) public {
        // solhint-disable-next-line not-rely-on-time
        require(!initialised);

        require(refundTime > block.timestamp, "Timelock: refund time is before current time");
        auction = _auction;
        refundTime = _refundTime;
        refundRate = _amountToRefund.mul(TENPOW18).div(auction.tokenSupply());

        auctionToken = IERC20(auction.auctionToken());
        paymentCurrency = IERC20(auction.paymentCurrency());

        // Needs to account for ETH payments
        paymentCurrency.transferFrom(address(_auction), address(this), _amountToRefund);
        initialised = true;
    }

    /**
     * @return the amount of tokens claimable.
     */
    function tokensRefundable(address _user) public view returns (uint256) {
        return auction.tokensClaimed(_user).sub(refunded[msg.sender]);
    }

    function refundAmount(address _user) public view returns (uint256) {
        return refundRate.mul(tokensRefundable(msg.sender)).div(TENPOW18);
    }

    /**
     * @notice Refund tokens held by vault.
     */
    function refund() public  {
        // solhint-disable-next-line not-rely-on-time
        require(block.timestamp >= refundTime, "Timelock: current time is before refund time");
        require(tokensRefundable(msg.sender) > 0, "Timelock: no tokens to refund");

        uint256 tokensToTransfer = refundAmount(msg.sender);
        refunded[msg.sender] = tokensRefundable(msg.sender);

        // Transfer the tokens owed
        require(IERC20(auctionToken).transferFrom(msg.sender, address(auction.wallet()), tokensToTransfer));
        _tokenPayment(paymentCurrency, msg.sender,refundAmount(msg.sender) );
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