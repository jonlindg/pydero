# pydero

Pydero is a small python library for interacting with smart contracts on the DERO STARGATE testnet. See the python scripts simple_test.py and test2.py for how to use it. Installing smart contracts is currently now supported, only executing a function on an already installed smart contract on the DERO block dag or query the value of stored variables in the smart contract. Executing a function requires a running dero cli-wallet with the flag --rpc-server. Retrieving the value of a stored variable requires a derod process running.
