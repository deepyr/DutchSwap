pragma solidity ^0.6.9;


import "../../interfaces/IERC20.sol";


contract Owned {

    address private mOwner;   
    bool private initialised;    
    address public newOwner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(isOwner());
        _;
    }

    function _initOwned(address _owner) internal {
        require(!initialised);
        mOwner = address(uint160(_owner));
        initialised = true;
        emit OwnershipTransferred(address(0), mOwner);
    }

    function owner() public view returns (address) {
        return mOwner;
    }
    function isOwner() public view returns (bool) {
        return msg.sender == mOwner;
    }

    function transferOwnership(address _newOwner) public {
        require(isOwner());
        newOwner = _newOwner;
    }

    function acceptOwnership() public {
        require(msg.sender == newOwner);
        emit OwnershipTransferred(mOwner, newOwner);
        mOwner = address(uint160(newOwner));
        newOwner = address(0);
    }
    function recoverTokens(address token, uint tokens) public {
        require(isOwner());
        if (token == address(0)) {
            payable(mOwner).transfer((tokens == 0 ? address(this).balance : tokens));
        } else {
            IERC20(token).transfer(mOwner, tokens == 0 ? IERC20(token).balanceOf(address(this)) : tokens);
        }
    }
}
