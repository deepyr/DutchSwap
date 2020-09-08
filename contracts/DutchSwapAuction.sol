pragma solidity ^0.6.9;

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
//::::::::::: @#::::::::::: @#:::::::::::: #@j:::::::::::::::::::::::::
//::::::::::: ##::::::::::: @#:::::::::::: #@j:::::::::::::::::::::::::
//::::::::::: ##::::::::::: @#:::::::::::: #@j:::::::::::::::::::::::::
//::::: ########: ##:: ##:: DUTCh>: ihD%y: #@Whdqy:::::::::::::::::::::
//::: ###... ###: ##:: ##:: @B... @@7...t: N@N.. R@K:::::::::::::::::::
//::: ##::::: ##: ##:: ##:: @Q::: @Q.::::: N@j:: z@Q:::::::::::::::::::
//:::: ##DuTCH##: .@QQ@@#:: hQQQh <R@QN@Q: N@j:: z@Q:::::::::::::::::::
//::::::.......: =Q@y....:::....:::......::...:::...:::::::::::::::::::
//:::::::::::::: h@W? sWAP@! 'DW;:::::: KK. ydSWAP@t: NNKNQBdt:::::::::
//:::::::::::::: 'zqRqj*. L@R h@w: QQ: L@5 Q@... d@@: @@U... @Q::::::::
//:::::::::::::::::...... Q@^ ^@@N@wt@BQ@ <@Q^::: @@: @@}::: @@:::::::: 
//:::::::::::::::::: U@@QKt... D@@L.. B@Q.. KDUTCH@Q: @@QQ#QQq:::::::::
//:::::::::::::::::::.....::::::...:::...::::.......: @@!.....:::::::::
//::::::::::::::::::::::::::::::::::::::::::::::::::: @@!::::::::::::::
//::::::::::::::::::::::::::::::::::::::::::::::::::: @@!::::::::::::::
//::::::::::::::01101100:01101111:01101111:01101011::::::::::::::::::::
//:::::01100100:01100101:01100101:01110000:01111001:01110010:::::::::::
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
//
// DutchSwap Auction V1.0
//
// https://dutchswap.com                      
// https://github.com/deepyr/DutchSwap
//
// Authors:
// * Adrian Guerrera / Deepyr Pty Ltd
//     May 26 2020                                  
//
// Part of the Petyl Protocol
// ----------------------------------------------------------------------------
// SPDX-License-Identifier: GPL-3.0-or-later
// ----------------------------------------------------------------------------

import "./Utils/SafeMath.sol";

contract DutchSwapAuction  {

    using SafeMath for uint256;
    /// @dev The placeholder ETH address.
    address private constant ETH_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    uint256 public startDate;
    uint256 public endDate;
    uint256 public startPrice;
    uint256 public minimumPrice;
    uint256 public totalTokens;  // Amount to be sold
    uint256 public priceDrop; // Price reduction from startPrice at endDate
    uint256 public commitmentsTotal;
    bool public finalised;
    address public auctionToken;
    address public paymentCurrency;
    address payable public wallet;  // Where the auction funds will get paid
    mapping(address => uint256) public commitments;
    mapping(address => uint256) public claimed;

    event AddedCommitment(address addr, uint256 commitment);

    /// @dev Init function
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
        external
    {
        require(_endDate > _startDate);
        require(_startPrice > _minimumPrice);
        require(_minimumPrice > 0);

        auctionToken = _token;
        paymentCurrency = _paymentCurrency;
        totalTokens = _totalTokens;
        startDate = _startDate;
        endDate = _endDate;
        startPrice = _startPrice;
        minimumPrice = _minimumPrice;
        wallet = _wallet;

        uint256 numerator = startPrice.sub(minimumPrice);
        uint256 denominator = endDate.sub(startDate);
        priceDrop = numerator.div(denominator);

        // There are many non-compliant ERC20 tokens... this can handle most, adapted from UniSwap V2
        // I'm trying to make it a habit to put external calls last (reentrancy)
        // You can put this in an internal function if you like.
        _safeTransferFrom(auctionToken, _funder, _totalTokens);
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
        return commitmentsTotal.mul(1e18).div(totalTokens);
    }

    /// @notice Token price decreases at this rate during auction.
    function priceGradient() public view returns (uint256) {
        return priceDrop;
    }

      /// @notice Returns price during the auction 
    function priceFunction() public view returns (uint256) {
        /// @dev Return Auction Price
        if (block.timestamp <= startDate) {
            return startPrice;
        }
        if (block.timestamp >= endDate) {
            return minimumPrice;
        }
        uint256 priceDiff = block.timestamp.sub(startDate).mul(priceGradient());
        return startPrice.sub(priceDiff);
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
        uint256 tokensAvailable = commitments[_user].mul(1e18).div(clearingPrice());
        return tokensAvailable.sub(claimed[msg.sender]);
    }

    /// @notice Total amount of tokens committed at current auction price
    function totalTokensCommitted() public view returns(uint256) {
        return commitmentsTotal.mul(1e18).div(clearingPrice());
    }

    /// @notice Successful if tokens sold equals totalTokens
    function auctionSuccessful() public view returns (bool){
        return totalTokensCommitted() >= totalTokens && tokenPrice() >= minimumPrice;
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
            _addCommitment(_from, ethToTransfer);
        }
        // Return any ETH to be refunded
        if (ethToRefund > 0) {
            _from.transfer(ethToRefund);
        }
    }

    /// @notice Commits to an amount during an auction
    function _addCommitment(address _addr,  uint256 _commitment) internal {
        require(block.timestamp >= startDate && block.timestamp <= endDate);
        commitments[_addr] = commitments[_addr].add(_commitment);
        commitmentsTotal = commitmentsTotal.add(_commitment);
        emit AddedCommitment(_addr, _commitment);
    }

    /// @notice Commit approved ERC20 tokens to buy tokens on sale
    function commitTokens(uint256 _amount) public {
        commitTokensFrom(msg.sender, _amount);
    }

    /// @dev Users must approve contract prior to committing tokens to auction
    function commitTokensFrom(address _from, uint256 _amount) public {
        require(address(paymentCurrency) != ETH_ADDRESS);
        uint256 tokensToTransfer = calculateCommitment( _amount);
        if (tokensToTransfer > 0) {
            _safeTransferFrom(paymentCurrency, _from, _amount);
            _addCommitment(_from, tokensToTransfer);
        }
    }

    /// @notice Returns the amout able to be committed during an auction
    function calculateCommitment( uint256 _commitment) 
        public view returns (uint256 committed) 
    {
        uint256 maxCommitment = totalTokens.mul(clearingPrice()).div(1e18);
        if (commitmentsTotal.add(_commitment) > maxCommitment) {
            return maxCommitment.sub(commitmentsTotal);
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
        
        if (commitmentsTotal.mul(1e18).div(totalTokens) >= clearingPrice())
        {
            // Successful auction
            _tokenPayment(paymentCurrency, wallet, commitmentsTotal);
        }
        else
        {
            // Failed auction
            require(block.timestamp > endDate);
            _tokenPayment(auctionToken, wallet, totalTokens);
        }
        finalised = true;
    }

    /// @notice Withdraw your tokens once the Auction has ended.
    function withdrawTokens() public {
        uint256 fundsCommitted = commitments[ msg.sender];
        uint256 tokensToClaim = tokensClaimable(msg.sender);

        if( auctionEnded() && tokenPrice() < minimumPrice ) 
        {
            /// @notice Auction did not meet reserve price.
            /// @dev Return committed funds back to user.
            commitments[msg.sender] = 0; // Stop multiple withdrawals and free some gas
            _tokenPayment(paymentCurrency, msg.sender, fundsCommitted);       
        }
        else if (auctionSuccessful() && tokensToClaim > 0) 
        {
            /// @notice Successful auction! Transfer claimed tokens.
            /// @dev AG: Should hold and distribute tokens vs mint
            /// @dev AG: Could be only > min to allow early withdraw  
            claimed[ msg.sender] = tokensToClaim;
            _tokenPayment(auctionToken, msg.sender, tokensToClaim);
        }
    }


    //--------------------------------------------------------
    // Helper Functions
    //--------------------------------------------------------

    // There are many non-compliant ERC20 tokens... this can handle most, adapted from UniSwap V2
    // I'm trying to make it a habit to put external calls last (reentrancy)
    // You can put this in an internal function if you like.
    function _safeTransfer(address token, address to, uint256 amount) public {
        // solium-disable-next-line security/no-low-level-calls
        (bool success, bytes memory data) = token.call(
            // 0xa9059cbb = bytes4(keccak256("transferFrom(address,address,uint256)"))
            abi.encodeWithSelector(0xa9059cbb, to, amount)
        );
        require(success && (data.length == 0 || abi.decode(data, (bool))), "XS2: Transfer failed at ERC20");
    }

    function _safeTransferFrom(address token, address from, uint256 amount) public {
        // solium-disable-next-line security/no-low-level-calls
        (bool success, bytes memory data) = token.call(
            // 0x23b872dd = bytes4(keccak256("transferFrom(address,address,uint256)"))
            abi.encodeWithSelector(0x23b872dd, from, address(this), amount)
        );
        require(success && (data.length == 0 || abi.decode(data, (bool))), "XS2: TransferFrom failed at ERC20");
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