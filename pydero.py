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



#--------------------------------------------------
#-------------helper functions and classes---------
#--------------------------------------------------


#This class is used in Contract to create methods, should not be used on its own
class _Function:
    def __init__(self,contract,function_name,args):
        self.args=args
        self.contract=contract
        self.function_name = function_name

    def __call__(self,*args):
        if len(args)!=len(self.args):
            raise TypeError('Function '+self.function_name+' requires '+str(len(self.args))+' arguments, '+str(len(args))+' provided')

        if self.contract.connection:
            if self.contract.scid:

                data = '{"jsonrpc":"2.0","id":"0","method":"transfer_split","params":{"mixin":5,"get_tx_key": true , "sc_tx":{"entrypoint":"'+self.function_name+'","scid":"'+self.contract.scid+'", '

                params = '"params":{'
                value=''
                first=True
                for arg,arg_name in zip(args,self.args.keys()):
                    if arg_name=='value':
                        value='"value":'+str(arg)+', '
                    else:
                        if first==False:
                            params=params+","
                        first=False
                        if _check_type(arg,self.args[arg_name]):
                            params=params+'"'+arg_name+'":"'+str(arg)+'"'
                data=data+value+params+'}}}}'
#                print("Data: "+data)

                response = self.contract.connection.rpc_wallet(data)
                return response.json()
            else:
                raise Exception("Contract does not have scid")
        else:
            raise Exception("Contract does not have a connection")

#function that validates if an abi dictionary has the correct format
def _validate_abi(abi):
    if type(abi)!=dict:
        raise TypeError('ABI must be a dictionary')
    for fun in abi.keys():
        if type(fun)!=str:
            raise TypeError("Keys of the ABI dictionary must be of type 'str'")
        if type(abi[fun])!=dict:
            raise TypeError("The value of function '"+fun+"' in ABI dictionary is not a dictionary")
        for par in abi[fun].keys():
            if type(par)!=str:
                raise TypeError("Parameter names must be of type 'str'")
            if ((abi[fun][par]!='Uint64')and(abi[fun][par]!='String')):
                raise TypeError("Parameter type must be either 'Uint64' or 'String'")
    return True

#function for checking if python parameter 'par' and DBASIC type 'par_type' are compatible
def _check_type(par,par_type):
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
        """Function for sending JSON RPC data to the DERO cli-wallet"""
        if self.access_point_wallet is None:
            raise Exception("No access point provided for wallet rpc")
        return requests.post(self.access_point_wallet+mode,headers=self.headers,data=data)

    def rpc_daemon(self,data,mode='/gettransactions'):
        """Function for sending JSON RPC data to the DERO daemon"""
        if self.access_point_daemon is None:
            raise Exception("No access point provided for daemon rpc")
        return requests.post(self.access_point_daemon+mode,headers=self.headers,data=data)

    def get_balance(self):
        response = requests.post(self.access_point_wallet+'/json_rpc',headers=self.headers,json={'jsonrpc':'2.0','id':'0','method':'getbalance'})
        return response.json()['result']

    def get_address(self):
        response = requests.post(self.access_point_wallet+'/json_rpc',headers=self.headers,json={'jsonrpc':'2.0','id':'0','method':'getaddress'})
        return response.json()['result']




class Contract:
    """A class representing a smart contract on the DERO block-dag. __init__ takes three arguments:
                abi: The ABI of the contract, should be a dictionary format {'Function1':{'Parameter1':parameter_type1,'Parameter2':parameter_type2,...},'Function2':...}, parameter_type can be either 'String' or 'Uint64'
                connection: Should be an instance of the Connection class, optional argument but must be set in order to interact with the contract on the DERO blockdag
                scid: The scid of the contract, optional argument but must be set in order to interact with the contract on the DERO blockdag
"""

    connection = None
    scid = None

    def __init__(self,abi,connection=None,scid=None):
        self.connection=connection
        if type(scid)!=str:
            raise TypeError("scid must be of type 'str'")
        self.scid=scid

        if _validate_abi(abi):
            for function_name in abi.keys():
                setattr(self,function_name,_Function(self,function_name,abi[function_name]))


    def get_attribute(self,variable):
        """Retrieves the value of any stored variable in the contract"""
        if type(variable)!=str:
            raise TypeError("Argument must be of type 'str'")
        data = '{"txs_hashes":["'+self.scid+'"], "sc_keys":["'+variable+'"]}'
        response = self.connection.rpc_daemon(data)
        try:
            return response.json()['txs'][0]['sc_keys'][variable]
        except Exception as e:
            raise Exception("Failed retrieving value for variable "+variable)


if __name__=='__main__':
    connection = Connection()
    print(connection.get_balance())
    print(connection.get_address())
    

