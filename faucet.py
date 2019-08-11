#import the relevant classes from pydero
from pydero import Contract,Connection

#see the smart contract source code simple_test.bas or on the dero stargate explorer:
#http://pool.dero.io:8080/tx/2849f5c32d385b8b972e53dde0abd5b6458f8eb9367f1215e7e95b819f739592

#specify the scid
scid='5845680ef31cc8b0e8ad43248473adfeae7501d3611cb98c4df34444711ed61b'

#create a Connection instance, specifying IP address and port of the running wallet. Note that the wallet must be running with the --rpc-server flag
conn = Connection('http://127.0.0.1:30309','http://127.0.0.1:30306')

#specify abi compatible with the smart contract source code
abi = {"GetDeroFaucet":{}}

#create an instance of the Contract class
contract = Contract(abi,connection=conn,scid=scid)

print(contract.GetDeroFaucet())
