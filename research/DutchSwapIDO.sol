pragma solidity ^0.6.9;

import "./OpenZeppelin/SafeMath.sol";
import "../interfaces/IERC20.sol";
import "../interfaces/IDutchAuction.sol";
                                                            
                                                              
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
//::::::::::: @#::::::::::: @#:::::::::::: #@j:::::::::::::::::::::::::
//::::::::::: ##::::::::::: @#:::::::::::: #@j:::::::::::::::::::::::::
//::::::::::: ##::::::::::: @#:::::::::::: #@j:::::::::::::::::::::::::
//::::: ########: ##:: jU* DUTCh>: ihD%Ky: #@Whdqy:::::::::::::::::::::
//::: ###... ###: ##:: #@j: @B... @@7...t: N@N.. R@K:::::::::::::::::::
//::: ##::::: ##: ##::.Q@t: @Q::: @Q.::::: N@j:: z@Q:::::::::::::::::::
//:::: ##DuTCH##: %@QQ@@S`: hQQQh <R@QN@Q* N@j:: z@Q:::::::::::::::::::
//::::::.......: =Q@y....:::....:::......::...:::...:::::::::::::::::::
//:::::::::::::: h@W? sWAP@! 'DW;::::::.KK. ydSWAP@t: NNKNQBdt:::::::::
//:::::::::::::: 'zqRqj*. L@R h@w: QQ: L@5 Q@z.. d@@: @@U... @Q::::::::
//:::::::::::::::::...... Q@^ ^@@N@wt@BQ@ <@Q^::: @@: @@}::: @@:::::::: 
//:::::::::::::::::: U@@QKt... D@@L...B@Q.. KDUTCH@Q: @@QQ#QQq:::::::::
//:::::::::::::::::::.....::::::...:::...::::.......: @@!.....:::::::::
//::::::::::::::::::::::::::::::::::::::::::::::::::: @@!::::::::::::::
//::::::::::::::::::::::::::::::::::::::::::::::::::: @@!::::::::::::::
//::::::::::::::01101100:01101111:01101111:01101011::::::::::::::::::::
//:::::01100100:01100101:01100101:01110000:01111001:01110010:::::::::::
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
//
// DutchSwap Initial Dex Offering
//   Copyright (c) 2020 DutchSwap.com
//
// Claim proceeds of a dutch auction and list them on Uniswap. 
// NOT FINISHED!
//
// MVP prototype. DO NOT USE YET!
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  
// If not, see <https://github.com/deepyr/DutchSwap/>.
//
// The above copyright notice and this permission notice shall be included 
// in all copies or substantial portions of the Software.
//
// Authors:
// * Adrian Guerrera / Deepyr Pty Ltd
//
// ---------------------------------------------------------------------
// SPDX-License-Identifier: GPL-3.0-or-later                        
// ---------------------------------------------------------------------



contract DutchSwapIDO {

    using SafeMath for uint256;
    uint256 private constant TENPOW18 = 10 ** 18;
    /// @dev The placeholder ETH address.
    address private constant ETH_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    // ERC20 basic token contract being held
    IDutchAuction public auction;
    address public auctionToken; 
    address public paymentCurrency; 

    // timestamp when token refund is enabled
    bool private initialised;
    uint256 public refundTime;
    uint256 public refundPct;  // 90 = 90% refunded to user
    uint256 public refundDuration;
    mapping(address => uint256) private refunded;


    /**
     * @notice Initialise contract parameters
     */
    function initAuctionIDO( address _auction) public {
        // solhint-disable-next-line not-rely-on-time
        require(!initialised);
        require(_refundPct < 100 && _refundPct > 0);

        auction = IDutchAuction(_auction);
        require(refundTime > auction.endDate(), "Timelock: refund time is before endDate");
        require(auction.wallet() == address(this));

        // might need a refund duration, say 1 week
        auctionToken = auction.auctionToken();
        paymentCurrency = auction.paymentCurrency();

        initialised = true;
    }

    // Things it needs to do
    // [] Create Uniswap pool
    // [] Wrap half funds as WETH
    // [] Mint LP tokens

    /**
     * @return the amount of tokens claimable.
     */


    /**
     * @notice Reject direct ETH payments.
     */
    receive () external payable {
        revert();
    }

    //--------------------------------------------------------
    // Helper Functions
    //--------------------------------------------------------

    // There are many non-compliant ERC20 tokens... this can handle most, adapted from UniSwap V2
    // I'm trying to make it a habit to put external calls last (reentrancy)
    // You can put this in an internal function if you like.
    function _safeTransfer(address token, address to, uint256 amount) internal {
        // solium-disable-next-line security/no-low-level-calls
        (bool success, bytes memory data) = token.call(
            // 0xa9059cbb = bytes4(keccak256("transferFrom(address,address,uint256)"))
            abi.encodeWithSelector(0xa9059cbb, to, amount)
        );
        require(success && (data.length == 0 || abi.decode(data, (bool)))); // ERC20 Transfer failed 
    }

    function _safeTransferFrom(address token, address from, uint256 amount) internal {
        // solium-disable-next-line security/no-low-level-calls
        (bool success, bytes memory data) = token.call(
            // 0x23b872dd = bytes4(keccak256("transferFrom(address,address,uint256)"))
            abi.encodeWithSelector(0x23b872dd, from, address(this), amount)
        );
        require(success && (data.length == 0 || abi.decode(data, (bool)))); // ERC20 TransferFrom failed 
    }

    /// @dev Helper function to handle both ETH and ERC20 payments
    function _tokenPayment(address _token, address payable _to, uint256 _amount) internal {
        if (address(_token) == ETH_ADDRESS) {
            _to.transfer(_amount);
        } else {
            _safeTransfer(_token, _to, _amount);
        }
    }


}