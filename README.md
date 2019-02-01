# pydero

Pydero is a small python library for interacting with smart contracts on the DERO STARGATE testnet. Installing smart contracts is currently not supported, only executing a function on an already installed smart contract on the DERO block dag or query the value of stored variables in the smart contract. Executing a function requires a running dero cli-wallet with the flag --rpc-server. Retrieving the value of a stored variable requires a derod process running. 

# usage

First import the relevant classes
```
from pydero import Contract, Connection
```

Instantiate a python Contract object by the command 

```
contract = Contract(abi,connection=connection,scid=scid)

```

connection should be an instance of the Connection class, scid should be a string with the scid of the smart contract on the dero blockdag. abi should be a dictionary of the form corresponding to the functions and parameters of the smart contract and the parameter types should be strings that are either "Uint64" or "String". For example, if the contract has two functions called Function1 and Function2, the first with one Uint64 and one String parameter and the second with no parameters, the abi is


```
abi={"Function1":{"ParameterName1":"Uint64","ParameterName2":"String"},"Function2":{}}

```
 To call a function on the contract, we simple do


```
contract.Function1(123,"abc")
```

To obtain the value of a stored variable called Foo:
```
contract.get_attribute("Foo")
```

See the python scripts simple_test.py and test2.py for more examples.
