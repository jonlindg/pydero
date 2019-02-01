import time
import json

#import the relevant classes from pydero
from pydero import Contract,Connection

#specify the scid
scid='2849f5c32d385b8b972e53dde0abd5b6458f8eb9367f1215e7e95b819f739592'

#create a Connection instance, specifying IP address and port of the running wallet. Note that the wallet must be running with the --rpc-server flag
conn = Connection('http://127.0.0.1:30309','http://127.0.0.1:30306')

#specify abi compatible with the smart contract source code
abi = {"Print":{},"ChangeValue":{"new_val":"Uint64"}}

#create an instance of the Contract class
contract = Contract(abi,connection=conn,scid=scid)

resp = contract.get_attribute('number')
print(resp)
#now you can call functions on the contract
#print(contract.Print.args)
#print(contract.ChangeValue.args)
#contract.Print()
#time.sleep(10)
#contract.ChangeValue(999)
#time.sleep(10)
#contract.Print()
#time.sleep(10)
#contract.ChangeValue(1098000)





    

#curl -X POST http://127.0.0.1:30309/json_rpc -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":"0","method":"transfer_split","params":{"mixin":5,"get_tx_key": true , "sc_tx":{"entrypoint":"Print","scid":"2849f5c32d385b8b972e53dde0abd5b6458f8eb9367f1215e7e95b819f739592", "params":{} } }}'

#curl -X POST http://127.0.0.1:30309/json_rpc -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":"0","method":"transfer_split","params":{"mixin":5,"get_tx_key": true , "sc_tx":{"entrypoint":"ChangeValue","scid":"2849f5c32d385b8b972e53dde0abd5b6458f8eb9367f1215e7e95b819f739592", "params":{"new_val":"763"} } }}'
            

#    curl -X POST http://127.0.0.1:30306/gettransactions -d '{"txs_hashes":["2849f5c32d385b8b972e53dde0abd5b6458f8eb9367f1215e7e95b819f739592"], "sc_keys":["number"]}' -H 'Content-Type: application/json
