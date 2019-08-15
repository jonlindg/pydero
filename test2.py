#import the relevant classes from pydero
from pydero import Contract,Connection
from pydero.utils import from_dero
import requests
#specify the scid
scid='d1668fce0d0e9c3191b7b8d174ddde9269ffbfb6f0bf85b07b3747411c541454'

#create a Connection instance, specifying IP address and port of the running wallet and daemon. Note that the wallet must be running with the --rpc-server flag
#conn = Connection('http://127.0.0.1:30309','http://127.0.0.1:30306')
conn = Connection('http://127.0.0.1:30309','http://62.210.79.219:30306')

#specify abi compatible with the smart contract source code
abi = {"ChangeValue":{"new_val1":"Uint64","new_val2":"Uint64"},"DepositAndChangeValue":{"new_val1":"Uint64","value":"Uint64","new_val2":"Uint64"},"DepositAndChangeValueAndStrings":{"new_val1":"Uint64","value":"Uint64","new_val2":"Uint64","new_str2":"String","new_str1":"String"},"Withdraw":{"new_val1":"Uint64","amount":"Uint64","new_val2":"Uint64"}}

#create an instance of the Contract class
contract = Contract(abi=None,connection=conn,scid=scid)
contract.set_abi_from_db()
#print(contract.get_abi())
#print(conn.get_address())
#print(conn.get_balance())
#print(conn.get_wallet_height())
#print(conn.get_block_count())
#print(conn.get_last_block_header())
#print(conn.get_block_header_by_hash('101979b481e7a9664569983c71bb35a360c36bce9d62013225852b86e221a22b'))
#print(conn.get_block_header_by_height(123))
#print(contract.get_abi_from_db())
print(contract.get_variable(['number','string1','string2','number']))
#print(contract.get())
#print(conn.get_last_block_header())
print(contract.get_balance(in_dero=True))
print(contract.DepositAndChangeValue.args)
#print(conn.get_balance())
#print(contract.get_balance(in_dero=True))
#print(contract.get_attribute('string1'))
#print(contract.get_attribute('string2'))#'28d39e391578511ef1ba545c882ad248d7628ed24bb289732324ca8070b1ddb0'
#print(conn.get_balance())
#curl -X POST http://127.0.0.1:30309/json_rpc -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":"0","method":"transfer_split","params":{"mixin":5,"get_tx_key": true , "sc_tx":{"entrypoint":"DepositAndChangeValue","scid":"d1668fce0d0e9c3191b7b8d174ddde9269ffbfb6f0bf85b07b3747411c541454" , "params":{ "new_val1":1, "new_val2":5} } }}'

#print(conn.transfer([(10,'dEToNsSBSisbRuwBwVjRG6j4GXRJXbHruPQZsiCoaYYcQeQp28KQiB4MpeyWC89sKr58JuqD6LQaYA1UhNk1GZfx8cqqC7pepJ')]).json())

#now you can call functions on the contract
#r=contract.ChangeValue(100,21)
#r=contract.DepositAndChangeValueAndStrings(10,4)
#print(r.json(),r.status_code,requests.codes.ok)
#print(contract.DepositAndChangeValue(1,from_dero(0),21,payable=True))
#print(contract.DepositAndChangeValueAndStrings(10,30100000000000,20,"ASDF113","QWERTY213"))
#print(contract.Withdraw(5,from_dero(3.0),8))





