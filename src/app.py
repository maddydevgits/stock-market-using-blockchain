from flask import Flask, render_template,redirect,request,session
import json
from web3 import Web3,HTTPProvider

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
    return render_template('dashboard.html')

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

@app.route('/logout')
def logoutPage():
    session['username']=None
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)