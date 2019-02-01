#import the relevant classes from pydero
from pydero import Contract,Connection

#specify the scid
scid='d1668fce0d0e9c3191b7b8d174ddde9269ffbfb6f0bf85b07b3747411c541454'

#create a Connection instance, specifying IP address and port of the running wallet and daemon. Note that the wallet must be running with the --rpc-server flag
conn = Connection('http://127.0.0.1:30309','http://127.0.0.1:30306')

#specify abi compatible with the smart contract source code
abi = {"ChangeValue":{"new_val1":"Uint64","new_val2":"Uint64"},"DepositAndChangeValue":{"new_val1":"Uint64","value":"Uint64","new_val2":"Uint64"},"DepositAndChangeValueAndStrings":{"new_val1":"Uint64","value":"Uint64","new_val2":"Uint64","new_str1":"String","new_str2":"String"},"Withdraw":{"new_val1":"Uint64","amount":"Uint64","new_val2":"Uint64"}}

#create an instance of the Contract class
contract = Contract(abi,connection=conn,scid=scid)

print(contract.get_attribute('number'))
print(contract.get_attribute('string1'))
print(contract.get_attribute('string2'))

#now you can call functions on the contract
#print(contract.ChangeValue(9,11))
#print(contract.DepositAndChangeValue(10,3100000000000,22))
#print(contract.DepositAndChangeValueAndStrings(10,3100000000000,20,"ASDF","QWERTY"))
#print(contract.Withdraw(5,5000000000000,7))





