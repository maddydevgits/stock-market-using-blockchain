// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract trades {
  address[] _usernames;
  uint[] _shares;
  uint[] _shareprices;

  address[] _tusernames;
  address[] _tcompanies;
  uint[] _tshares;
  uint[] _tshareprices;

  function createShare(address username, uint shares, uint shareprices) public {
    _usernames.push(username);
    _shares.push(shares);
    _shareprices.push(shareprices);
  }

  function viewShares() public view returns(address[] memory, uint[] memory, uint[] memory) {
    return(_usernames,_shares,_shareprices);
  }

  function tradeShare(address username,address company,uint noofshares,uint shareprice) public {
    _tusernames.push(username);
    _tcompanies.push(company);
    _tshares.push(noofshares);
    _tshareprices.push(shareprice);
  }

  function viewTradeShares() public view returns (address[] memory, address[] memory, uint[] memory,uint[] memory){
    return(_tusernames,_tcompanies,_tshares,_tshareprices);
  } 
}
