# pydero

Pydero is a python wrapper for interacting with smart contracts on the DERO STARGATE testnet. Installing smart contracts is currently not supported, only executing a function on an already installed smart contract on the DERO block dag or query the value of stored variables in the smart contract. Executing a function requires a running dero cli-wallet with the flag --rpc-server. Retrieving the value of a stored variable requires a derod process running. 

# usage

First import the relevant classes
```
from pydero import Contract, Connection
```

Instantiate a python Contract object by the command 

```
contract = Contract(abi=abi,connection=connection,scid=scid)

```

connection should be an instance of the Connection class, scid should be a string with the scid of the smart contract on the dero blockdag. abi should be a dictionary of the form corresponding to the functions and parameters of the smart contract and the parameter types should be strings that are either "Uint64" or "String". For example, if the contract has two functions called Function1 and Function2, the first with one Uint64 and one String parameter and the second with no parameters, the abi is


```
from collections import OrderedDict
abi={"Function1":OrderedDict({"ParameterName1":"Uint64","ParameterName2":"String"}),"Function2":{}}

```

The order of function parameters is important, and therefore it is recommended to use an OrderedDict instead. Instead of specifying the abi manually, it can be loaded from the dero blockdag. This requires a valid scid and a working connection to a dero daemon.
```
contract.set_abi_from_db()
```

 To call a function on the contract, we simple do


```
contract.Function1(123,"abc")
```

To obtain the value of a stored variable called Foo:
```
contract.get_attribute("Foo")
```

We can also query different information form the running wallet, for example
```
connection.get_balance()
```

We can also query the daemon for information, for example
```
connection.get_last_block_header()
```


See the python scripts simple_test.py and test2.py for more examples.
