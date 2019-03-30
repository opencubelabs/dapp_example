# IPFS + Ethereum Dapp Example

## Requirements

* Python 2.7+
* Bottle Py
* IPFS Python API
* Crypto module
* IPFS client 
* Metamask wallet

## Remix Code

pragma solidity ^0.5.1;

contract Contract { 
    
    string ipfsHash;

    function set(string memory x) public { ipfsHash = x; }

    function get() public view returns (string memory) { return ipfsHash; }

}