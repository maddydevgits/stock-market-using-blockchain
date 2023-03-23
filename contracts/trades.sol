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
  uint[] _ttradeids;

  function createShare(address username, uint shares, uint shareprices) public {
    _usernames.push(username);
    _shares.push(shares);
    _shareprices.push(shareprices);
  }

  function increaseSharePrice(address username,uint shareprice) public {
    uint i;
    for(i=0;i<_usernames.length;i++) {
      if(_usernames[i]==username)
        _shareprices[i]+=shareprice;
    }
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

  function sellShare(address username,address company, uint noofshares,uint shareprice) public returns(bool){

    uint i;
    for(i=0;i<_tusernames.length;i++) {
      if(_tusernames[i]==username && _tcompanies[i]==company && _tshares[i]==noofshares && _tshareprices[i]==shareprice) {
        delete _tusernames[i];
        delete _tcompanies[i];
        delete _tshares[i];
        delete _tshareprices[i];
        return true;
      }
    }
    return false;
  }

  function viewTradeShares() public view returns (address[] memory, address[] memory, uint[] memory,uint[] memory){
    return(_tusernames,_tcompanies,_tshares,_tshareprices);
  } 
}
