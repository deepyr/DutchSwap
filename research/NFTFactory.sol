pragma solidity ^0.6.9;

import "../Utils/CloneFactory.sol";
import "../../interfaces/INFT.sol";
import "./NFT.sol";
import "../Utils/Owned.sol";
import "../Utils/SafeMathPlus.sol";

contract NFTFactory is Owned, CloneFactory {
    using SafeMath for uint256;

    address public nftTemplate;
    uint256 public minimumFee = 0 ether;
    address[] public nfts;
    address payable public fundWallet;
    mapping(address => bool) public isChildToken;

    event NFTDeployed(address indexed owner, address indexed addr, address nft);
    event NFTTemplateUpdated(address oldNFT, address newNFT);
    event MinimumFeeUpdated(uint256 oldFee, uint256 newFee);
    event FundWalletUpdated(address oldFundWallet, address newFundWallet);

    function initNFTFactory(address _nftTemplate, uint256 _minimumFee, address payable _fundWallet)
        public
    {
        nftTemplate = _nftTemplate;
        minimumFee = _minimumFee;
        fundWallet = _fundWallet;
        _initOwned(msg.sender);

    }

    function deployNFT(string memory _name, string memory _symbol)
        public
        payable
        returns (address nft)
    {
        require(msg.value >= minimumFee);
        nft = createClone(nftTemplate);
        isChildToken[address(nft)] = true;
        nfts.push(address(nft));
        INFT(nft).initNFT(_name, _symbol);
        emit NFTDeployed(msg.sender, address(nft), nftTemplate);
    }

    function setNFTTemplate( address _nftTemplate) public onlyOwner {
        emit NFTTemplateUpdated(nftTemplate, _nftTemplate);
        nftTemplate = _nftTemplate;
    }

    function setMinimumFee(uint256 _minimumFee) public onlyOwner {
        minimumFee = _minimumFee;
        emit MinimumFeeUpdated(minimumFee, _minimumFee);
    }

    function setFundWallet(address payable _fundWallet) public onlyOwner {
        fundWallet = _fundWallet;
        emit FundWalletUpdated(fundWallet, _fundWallet);
    }

    function numberOfNFTs() public view returns (uint256) {
        return nfts.length;
    }

    function withdrawFunds() public onlyOwner {
        fundWallet.transfer(address(this).balance);
    }

    receive() external payable {
        revert();
    }
}
