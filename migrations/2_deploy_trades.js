const trades=artifacts.require('trades');

module.exports=function(deployer){
    deployer.deploy(trades);
}