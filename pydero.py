#-----Discord: @Kurret--------------------
#-----------------------------------------
#-----Use at your own risk, the author----
#-----takes no responsibility in ---------
#-----case of loss of funds---------------
#-----------------------------------------
#-----------------------------------------
#----Distributed under the MIT License----


import json
import requests
from collections import OrderedDict


#--------------------------------------------------
#-------------helper functions and classes---------
#--------------------------------------------------
def to_dero(value):
    """Convert number in smallest unit to number in dero"""
    return value/10**12

def from_dero(value_in_dero):
    """Convert number in dero to smallest unit"""
    return int(value_in_dero*10**12)


class _Function:
    """This class is used in Contract to create methods, should not be used on its own"""
    def __init__(self,contract,function_name,args):
        self.args=args
        self.contract=contract
        self.function_name = function_name

    def __call__(self,*args,mixin=5,):
        if len(args)!=len(self.args):
            raise TypeError('Function '+self.function_name+' requires '+str(len(self.args))+' arguments, '+str(len(args))+' provided')

        if self.contract.connection:
            if self.contract.scid:

                payload={"jsonrpc":"2.0","id":"0","method":"transfer_split"}

                params_={"mixin":mixin,"get_tx_key":True,"sc_tx":{"entrypoint":self.function_name,"scid":self.contract.scid}}
                
                function_params={}
                value_=None

                for arg,arg_name in zip(args,self.args.keys()):
                    if arg_name=='value':
                        value_=arg
                    else:
                        if _check_type(arg,self.args[arg_name]):
                            function_params[arg_name]=str(arg)

                params_['sc_tx']['params']=function_params
                if value_:
                    params_['sc_tx']['value']=value_
                payload['params']=params_

                response = self.contract.connection.rpc_wallet(payload)
                return response.json()
            else:
                raise Exception("Contract does not have scid")
        else:
            raise Exception("Contract does not have a connection")



def _validate_abi(abi):
    """function that validates if an abi dictionary has the correct format"""
    if type(abi) not in (dict,OrderedDict):
        raise TypeError('ABI must be a dictionary')
    for fun in abi.keys():
        if type(fun)!=str:
            raise TypeError("Keys of the ABI dictionary must be of type 'str'")
        if type(abi[fun]) not in (dict,OrderedDict):
            raise TypeError("The value of function '"+fun+"' in ABI dictionary is not a dictionary")
        for par in abi[fun].keys():
            if type(par)!=str:
                raise TypeError("Parameter names must be of type 'str'")
            if ((abi[fun][par]!='Uint64')and(abi[fun][par]!='String')):
                raise TypeError("Parameter type must be either 'Uint64' or 'String'")
    return True


def _check_type(par,par_type):
    """function for checking if python parameter 'par' and DBASIC type 'par_type' are compatible"""
    if par_type=='String':
        if type(par)==str:
            return True
        else:
            raise TypeError("Parameter of DBASIC type 'String' must be of python type 'str'")
    elif par_type=='Uint64':
        if type(par)==int:
            if par>=0:
                return True
            else:
                raise TypeError("Parameter of DBASIC type 'Uint64' can not be negative")
        else:
            raise TypeError("Parameter of DBASIC type 'Uint64' must be of python type 'int'")
    else:
        raise TypeError("Parameter DBASIC type should be 'Uint64' or 'String'")

#--------------------------------------------------
#---------------main classes-----------------------
#--------------------------------------------------

class Connection:
    """This class handles JSON RPC calls to a DERO daemon and DERO cli-wallet (running with the --rpc-server flag enabled)."""

    def __init__(self,access_point_wallet="http://127.0.0.1:30309",access_point_daemon="http://127.0.0.1:30306"):
        self.access_point_wallet=access_point_wallet
        self.access_point_daemon=access_point_daemon
        self.headers = {'Content-Type':'application/json'}


    def rpc_wallet(self,data,mode='/json_rpc'):
        """For sending rpc request to the wallet"""
        """Function for sending JSON RPC data to the DERO cli-wallet"""
        if self.access_point_wallet is None:
            raise Exception("No access point provided for wallet rpc")
        return requests.post(self.access_point_wallet+mode,headers=self.headers,json=data)


    def rpc_daemon(self,data,mode='/gettransactions'):
        """For sending rpc request to the daemon"""
        """Function for sending JSON RPC data to the DERO daemon"""
        if self.access_point_daemon is None:
            raise Exception("No access point provided for daemon rpc")
        return requests.post(self.access_point_daemon+mode,headers=self.headers,json=data)




    def get_balance(self,full_response=False):
        """Get balance of the wallet"""
        response = self.rpc_wallet({'jsonrpc':'2.0','id':'0','method':'getbalance'})
        if full_response:
            return response
        else:
            return response.json()['result']['balance'],response.json()['result']['unlocked_balance']


    def get_address(self,full_response=False):
        """Get address of the wallet"""
        response = self.rpc_wallet({'jsonrpc':'2.0','id':'0','method':'getaddress'})
        if full_response:
            return response
        else:
            return response.json()['result']['address']


    def get_wallet_height(self,full_response=False):
        """Get current height in the wallet"""
        response = self.rpc_wallet({'jsonrpc':'2.0','id':'0','method':'getheight'})
        if full_response:
            return response
        else:
            return response.json()['result']['height']


    def get_block_count(self,full_response=False):
        """Get current height in the daemon"""
        response = self.rpc_daemon({'jsonrpc':'2.0','id':'0','method':'getblockcount'},mode='/json_rpc')
        if full_response:
            return response
        else:
            return response.json()['result']['count']


    def get_info(self,full_response=False):
        """Returns various info about the daemon"""
        response = self.rpc_daemon({'jsonrpc':'2.0','id':'0','method':'get_info'},mode='/json_rpc')
        if full_response:
            return response
        else:
            return response.json()['result']


    def get_last_block_header(self,full_response=False):
        """The header of the last block"""
        response = self.rpc_daemon({'jsonrpc':'2.0','id':'0','method':'getlastblockheader'},mode='/json_rpc')
        if full_response:
            return response
        else:
            return response.json()['result']['block_header']


    def get_block_header_by_hash(self,block_hash,full_response=False):
        """The header of a block with a given hash"""
        response = self.rpc_daemon({'jsonrpc':'2.0','id':'0','method':'getblockheaderbyhash','params':{'hash':block_hash}},mode='/json_rpc')
        if full_response:
            return response
        else:
            return response.json()['result']['block_header']


    def get_block_header_by_height(self,height,full_response=False):
        """The header of a block with a given height"""
        response = self.rpc_daemon({'jsonrpc':'2.0','id':'0','method':'getblockheaderbyheight','params':{'hash':height}},mode='/json_rpc')
        if full_response:
            return response
        else:
            return response.json()['result']['block_header']


    def transfer(self,destinations,mixin=5,unlock_time=0,payment_id=0,get_tx_key=False,get_tx_hex=False,full_response=False,unit='dero'):
        """Transfer dero"""
        if type(destinations)!=list:
            raise ValueError("destinations must be of the form [(amount_1,address_1),...,(amount_n,address_n)]")
        for i,dest in enumerate(destinations):

            if type(dest) not in (list,tuple,dict):
                raise ValueError("destinations must be of the form [(amount_1,address_1),...,(amount_n,address_n)]")

            if len(dest)!=2:
                raise ValueError("destinations must be of the form [(amount_1,address_1),...,(amount_n,address_n)]")

            if type(dest) in (list,tuple):
                if (unit=='dero'):
                    destinations[i]={'amount':dest[0]*10**12,'address':dest[1]}
                else:
                    destinations[i]={'amount':dest[0],'address':dest[1]}

            if 'amount' not in destinations[i].keys():
                raise ValueError
            if 'address' not in destinations[i].keys():
                raise ValueError

        response = requests.post(self.access_point_wallet+'/json_rpc',headers=self.headers,json={'jsonrpc':'2.0','id':'0','method':'transfer','params':{"destinations":destinations,'mixin':mixin,"unlock_time":unlock_time,"payment_id":0,"get_tx_key":get_tx_key,"get_tx_hex":get_tx_hex}})
        if full_response:
            return response
        else:
            return response.json()['result']


class Contract:
    """A class representing a smart contract on the DERO block-dag. __init__ takes three arguments:
                abi: The ABI of the contract, should be a dictionary format {'Function1':{'Parameter1':parameter_type1,'Parameter2':parameter_type2,...},'Function2':...}, parameter_type can be either 'String' or 'Uint64'
                connection: Should be an instance of the Connection class, optional argument but must be set in order to interact with the contract on the DERO blockdag
                scid: The scid of the contract, optional argument but must be set in order to interact with the contract on the DERO blockdag
"""

    def __init__(self,abi=None,connection=None,scid=None):
        self.connection=connection
        if type(scid)!=str:
            raise TypeError("scid must be of type 'str'")
        self.scid=scid

        if abi!=None:
            if _validate_abi(abi):
                self.abi = abi
                for function_name in abi.keys():
                    
                    setattr(self,function_name,_Function(self,function_name,abi[function_name]))

    def get_attribute(self,variables,as_dict=False):
        """Retrieves the value of any stored variables in the contract. variables should be a list of stored variable names"""
        one_variable=False
        if type(variables)==str:
            one_variable=True
        if type(variables) not in (list,tuple):
            variables=[variables]
        for var in variables:
            if type(var)!=str:
                raise TypeError("Keys must be of type 'str'")
        data = {"txs_hashes":[self.scid],"sc_keys":variables}
        response = self.connection.rpc_daemon(data)
        try:
            keys=response.json()['txs'][0]['sc_keys']

            if as_dict:
                return keys
            else:
                if one_variable:
                    return keys[variables[0]]
                else:
                    return [keys[var] for var in variables]
        except Exception as e:
            raise e


    def get_balance(self,in_dero=False):
        """Retrieves smart contract balance"""
        response = self.connection.rpc_daemon({"txs_hashes":[self.scid]})
        if in_dero:
            return to_dero(response.json()['txs'][0]['sc_balance'])
        else:
            return response.json()['txs'][0]['sc_balance']
    


    def get_abi_from_db(self):
        """Extracts the abi from the dero dag using the scid"""
        if self.scid==None:
            raise Exception("scid is not set")
        if self.connection==None:
            raise Exception("connection is not set")
        data = {"txs_hashes":[self.scid]}
        response = self.connection.rpc_daemon(data).json()
        if response['txs']==None:
            raise Exception("Smart contract not found")
        functions = response['txs'][0]['sc']['F']
        abi = {}
        for f in functions.keys():
            abi[f]=OrderedDict()
            function=functions[f]
            if 'P' in function.keys():
                parameters=functions[f]['P']
                for par in parameters:
                    if par['T']==1:
                        abi[f][par['N']]='Uint64'
                    if par['T']==2:
                        abi[f][par['N']]='String'
    
        return abi

    def set_abi_from_db(self):
        """Sets the contracts abi from the dero dag using the scid"""
        self.abi=self.get_abi_from_db()
        if _validate_abi(self.abi):
            for function_name in self.abi.keys():                    
                setattr(self,function_name,_Function(self,function_name,self.abi[function_name]))

if __name__=='__main__':
    connection = Connection()
    print(connection.get_balance())
    print(connection.get_address())
    

