pragma solidity ^0.6.9;

import "../Utils/Owned.sol";
import "./ERC721Base.sol";

contract NFT is Owned, ERC721Base {
    using SafeMath for uint256;

    struct Token {
        uint256 price;
        string metaId;
        bool isForSale;
    }

    bool private initialised;

    uint256 public tokenId;

    mapping(uint256 => Token) public tokens;

    event TokenMinted(uint256 tokenId, string metaId);
    event TokenBurned(uint256 tokenId, string metaId);
    event TokenBought(uint256 tokenId, string metaId, uint256 amount);

    function initNFT(string memory _name, string memory _symbol) public {
        require(!initialised);
        initERC721(_name, _symbol);
        _initOwned(msg.sender);
        tokenId = 0;
        initialised = true;
    }

    function mintToken(
        address _to,
        uint256 _price,
        string memory _metaId,
        bool _isForSale
    ) external onlyOwner {
        tokenId = tokenId.add(1);
        tokens[tokenId].price = _price;
        tokens[tokenId].metaId = _metaId;
        tokens[tokenId].isForSale = _isForSale;
        _mint(_to, tokenId);
        emit TokenMinted(tokenId, _metaId);
    }

    function burnToken(uint256 _tokenId) public {
        require(msg.sender == ownerOf(_tokenId));
        _burn(_tokenId);
        emit TokenBurned(_tokenId, tokens[_tokenId].metaId);
    }

    function buyToken(uint256 _tokenId) public payable {
        require(msg.value >= tokens[_tokenId].price, "Price issue");
        require(tokens[_tokenId].isForSale, "Token is not for sale");

        address payable ownerOfToken = payable(ownerOf(tokenId));

        if (tokens[_tokenId].price >= 0) {
            ownerOfToken.transfer(msg.value);
        }

        _safeTransfer(ownerOfToken, _msgSender(), _tokenId, "");
        tokens[_tokenId].isForSale = false;

        emit TokenBought(_tokenId, tokens[_tokenId].metaId, msg.value);
    }

    function setTokenPrice(uint256 _tokenId, uint256 _newPrice) public {
        require(msg.sender == ownerOf(_tokenId));
        tokens[_tokenId].price = _newPrice;
    }

    function setTokenStatus(uint256 _tokenId, bool _isForSale) public {
        require(msg.sender == ownerOf(_tokenId));
        tokens[_tokenId].isForSale = _isForSale;
    }
}
