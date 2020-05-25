pragma solidity ^0.6.2;
 
import "./IERC20.sol";

interface IMintableToken is IERC20 {

    function mint(address to, uint256 amount) external;

}
