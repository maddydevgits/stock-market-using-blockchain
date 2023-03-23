from flask import Flask, render_template,redirect,request,session
import json
from web3 import Web3,HTTPProvider

_companies=['TCS','Infosys','Tech Mahindra','HCL','Wipro']

def connect_with_register_blockchain(acc):
    server='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(server))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/register.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return (contract,web3)

def connect_with_trades_blockchain(acc):
    server='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(server))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/trades.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return (contract,web3)

app=Flask(__name__)
app.secret_key='sacet'

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/registerUser',methods=['post'])
def registerUser():
    walletaddr=request.form['walletaddr']
    password=int(request.form['password'])
    role=int(request.form['role'])
    print(walletaddr,password)
    try:
        contract,web3=connect_with_register_blockchain(0)
        tx_hash=contract.functions.registerUser(walletaddr,password,role).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return redirect('/')
    except:
        return render_template('index.html',err1='Account Exist')

@app.route('/loginUser',methods=['post'])
def loginUser():
    walletaddr=request.form['walletaddr1']
    password=request.form['password1']
    try:
        contract,web3=connect_with_register_blockchain(0)
        state=contract.functions.loginUser(walletaddr,int(password)).call()
        if state==True:
            _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
            userIndex=_usernames.index(walletaddr)
            role=_roles[userIndex]
            session['username']=walletaddr
            session['role']=role
            if(role==0):
                return redirect('/cdashboard')
            elif(role==1):
                return redirect('/dashboard')
        else:
            return render_template('index.html',err1='Invalid Credentials')
    except:
        return render_template('index.html',err1='Create Account First')

@app.route('/dashboard')
def dashboardPage():
    contract,web3=connect_with_trades_blockchain(0)
    _usernames,_shares,_shareprices=contract.functions.viewShares().call()
    data=[]
    for i in range(len(_usernames)):
        dummy=[]
        dummy.append(_companies[i])
        dummy.append(_shares[i])
        dummy.append(_shareprices[i])
        data.append(dummy)
    return render_template('dashboard.html',dashboard_data=data,len=len(data))

@app.route('/cdashboard')
def cdashboardPage():
    contract,web3=connect_with_trades_blockchain(0)
    _usernames,_shares,_shareprices=contract.functions.viewShares().call()
    data=[]
    for i in range(len(_usernames)):
        if(_usernames[i]==session['username']):
            dummy=[]
            dummy.append(_usernames[i])
            dummy.append(_shares[i])
            dummy.append(_shareprices[i])
            data.append(dummy)
    return render_template('cdashboard.html',dashboard_data=data,len=len(data))

@app.route('/createshare')
def createSharePage():
    return render_template('createshare.html')

@app.route('/createShareForm',methods=['post'])
def createShareForm():
    noofshares=request.form['noofshares']
    shareprice=request.form['shareprice']
    print(noofshares,shareprice)
    contract,web3=connect_with_trades_blockchain(0)
    tx_hash=contract.functions.createShare(session['username'],int(noofshares),int(shareprice)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('createshare.html',res='Shares Created on Stock Market')

@app.route('/investors')
def investorsPage():
    contract,web3=connect_with_trades_blockchain(0)
    _tusernames,_tcompanies,_tshares,_tshareprices=contract.functions.viewTradeShares().call()
    data=[]
    for i in range(len(_tusernames)):
        if(_tcompanies[i]==session['username']):
            dummy=[]
            dummy.append(_tusernames[i])
            dummy.append(_tshares[i])
            dummy.append(_tshareprices[i])
            data.append(dummy)
    return render_template('investors.html',dashboard_data=data,len=len(data))

@app.route('/purchasestock')
def purchasestock():
    walletaddr=session['username']
    role=session['role']
    contract,web3=connect_with_register_blockchain(0)
    _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
    for i in range(len(_usernames)):
        if _usernames[i]==walletaddr:
            amount=_amounts[i]
    
    data=[]
    contract,web3=connect_with_trades_blockchain(0)
    _usernames,_shares,_shareprices=contract.functions.viewShares().call()
    for i in range(len(_usernames)):
        dummy=[]
        dummy.append(_companies[i])
        dummy.append(_usernames[i])
        dummy.append(_shares[i])
        dummy.append(_shareprices[i])
        data.append(dummy)
    return render_template('purchasestock.html',balance=amount,dashboard_data=data,len=len(data))

@app.route('/stock/<id>')
def purchasestock1(id):
    print(id)
    session['id']=int(id)
    walletaddr=session['username']
    role=session['role']
    contract,web3=connect_with_register_blockchain(0)
    _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
    for i in range(len(_usernames)):
        if _usernames[i]==walletaddr:
            amount=_amounts[i]
    data=[]
    contract,web3=connect_with_trades_blockchain(0)
    _usernames,_shares,_shareprices=contract.functions.viewShares().call()
    shareprice=_shareprices[int(id)]
    session['shareprice']=shareprice
    return render_template('purchasestock1.html',balance=amount,dashboard_data=shareprice)

@app.route('/purchaseShareForm',methods=['get','post'])
def purchaseShareForm():
    walletaddr=session['username']
    id=session['id']
    noofshares=int(request.form['noofshares'])
    print(id,noofshares)
    contract,web3=connect_with_register_blockchain(0)
    _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
    for i in range(len(_usernames)):
        if _usernames[i]==walletaddr:
            amount=_amounts[i]
    
    if(noofshares*session['shareprice']<amount):
        balance=amount-(noofshares*session['shareprice'])
        contract,web3=connect_with_register_blockchain(0)
        tx_hash=contract.functions.updateBalance(session['username'],balance).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)


        contract,web3=connect_with_trades_blockchain(0)
        _usernames,_shares,_shareprices=contract.functions.viewShares().call()
        company=_usernames[id]        
        tx_hash=contract.functions.tradeShare(session['username'],company,int(noofshares),session['shareprice']).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print('Share can be purchased')
        print(id)
        session['id']=int(id)
        walletaddr=session['username']
        role=session['role']
        contract,web3=connect_with_register_blockchain(0)
        _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
        for i in range(len(_usernames)):
            if _usernames[i]==walletaddr:
                amount=_amounts[i]
        data=[]
        contract,web3=connect_with_trades_blockchain(0)
        _usernames,_shares,_shareprices=contract.functions.viewShares().call()
        shareprice=_shareprices[int(id)]
        session['shareprice']=shareprice
        return render_template('purchasestock1.html',res='Shares Purchased',balance=amount,dashboard_data=shareprice)
    else:
        print('Shares cant be purchased')

@app.route('/mystocks')
def mystocks():
    contract,web3=connect_with_register_blockchain(0)
    _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
    companieslist=[]
    for i in range(len(_usernames)):
        if(_roles[i]==0):
            companieslist.append(_usernames[i])

    contract,web3=connect_with_trades_blockchain(0)
    _tusernames,_tcompanies,_tshares,_tshareprices=contract.functions.viewTradeShares().call()
    data=[]
    for i in range(len(_tusernames)):
        if(_tusernames[i]==session['username']):
            dummy=[]
            companiesIndex=companieslist.index(_tcompanies[i])
            dummy.append(_companies[companiesIndex])
            dummy.append(_tcompanies[i])
            dummy.append(_tshares[i])
            dummy.append(_tshareprices[i])
            data.append(dummy)
    return (render_template('mystocks.html',dashboard_data=data,len=len(data)))

@app.route('/sellstock/<id1>')
def sellstock(id1):
    print(id1)
    contract,web3=connect_with_register_blockchain(0)
    _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
    companieslist=[]
    for i in range(len(_usernames)):
        if(_roles[i]==0):
            companieslist.append(_usernames[i])

    session['id1']=int(id1)
    contract,web3=connect_with_trades_blockchain(0)
    _tusernames,_tcompanies,_tshares,_tshareprices=contract.functions.viewTradeShares().call()
    data=[]
    for i in range(len(_tusernames)):
        if(_tusernames[i]==session['username']):
            dummy=[]
            companiesIndex=companieslist.index(_tcompanies[i])
            dummy.append(_companies[companiesIndex])
            dummy.append(_tcompanies[i])
            dummy.append(_tshares[i])
            dummy.append(_tshareprices[i])
            data.append(dummy)
    
    scompaniesIndex=data[session['id1']][0]
    stcompanies=data[session['id1']][1]
    stshares=data[session['id1']][2]
    stshareprices=data[session['id1']][3]
    contract,web3=connect_with_trades_blockchain(0)
    tx_hash=contract.functions.sellShare(session['username'],stcompanies,stshares,stshareprices).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)

    contract,web3=connect_with_trades_blockchain(0)
    _usernames,_shares,_shareprices=contract.functions.viewShares().call()
    company=_usernames.index(stcompanies)
    sp=_shareprices[company]

    contract,web3=connect_with_register_blockchain(0)
    _usernames,_passwords,_roles,_amounts=contract.functions.viewUsers().call()
    userIndex=_usernames.index(session['username'])
    balance=_amounts[userIndex]+sp
    tx_hash=contract.functions.updateBalance(session['username'],balance).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/mystocks')




@app.route('/logout')
def logoutPage():
    session['username']=None
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)