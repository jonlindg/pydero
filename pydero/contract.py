
from collections import OrderedDict
from pydero.utils import from_dero,to_dero

class _Function:
    """This class is used in Contract to create methods, should not be used on its own.

        Arguments are passed in as normal non-keyword arguments, read in the order of the 'args' attribute. 

        Note that an argument with name 'value' corresponds to amount of dero sent in the transaction. For security reasons, if a non-zero 'value' parameter is used, the payable keyword argument must be set to True for the transaction to go through"""

    def __init__(self,contract,function_name,args):
        self.args=args
        self.contract=contract
        self.function_name = function_name


    
    def __call__(self,*args,mixin=5,payable=False,value_in_dero=False):
        if len(args)!=len(self.args):
            raise TypeError('Function '+self.function_name+' requires '+str(len(self.args))+' arguments, '+str(len(args))+' provided')

        if self.contract.connection:
            if self.contract.scid:

                payload={"jsonrpc":"2.0","id":"0","method":"transfer_split"}

                params={"mixin":mixin,"get_tx_key":True,"sc_tx":{"entrypoint":self.function_name,"scid":self.contract.scid}}
                
                function_params={}
                value=None

                for arg,arg_name in zip(args,self.args.keys()):
                    if arg_name=='value':
                        if value_in_dero:
                            value=from_dero(arg)
                        else:
                            value=arg
                    else:
                        if _check_type(arg,self.args[arg_name]):
                            function_params[arg_name]=str(arg)

                params['sc_tx']['params']=function_params
                if value:
                    if payable:
                        params['sc_tx']['value']=value
                    else:
                        raise Exception("For transferring dero in a function call, set payable=True")
                payload['params']=params

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

class Contract:
    """A class representing a smart contract on the DERO block-dag. __init__ takes three arguments:
                abi: The ABI of the contract, should be a dictionary with format {'Function1':OrderedDict({'Parameter1':parameter_type1,'Parameter2':parameter_type2,...}),'Function2':...}, parameter_type can be either 'String' or 'Uint64'
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

    def get_variable(self,variables,as_dict=False):
        """Retrieves the value of any variable in the contract that has been stored with the STORE function."""

        if self.scid==None:
            raise Exception("scid is not set")
        if self.connection==None:
            raise Exception("connection is not set")

        one_variable=False
        if type(variables)==str:
            one_variable=True
        if type(variables) not in (list,tuple):
            variables=[variables]
        if type(variables)==tuple:
            variables=list(variables)
        for var in variables:
            if type(var)!=str:
                raise TypeError("Variable names must be of type 'str'")

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

        if self.scid==None:
            raise Exception("scid is not set")
        if self.connection==None:
            raise Exception("connection is not set")

        response = self.connection.rpc_daemon({"txs_hashes":[self.scid]})

        if in_dero:
            return to_dero(response.json()['txs'][0]['sc_balance'])
        else:
            return response.json()['txs'][0]['sc_balance']
    

#    def get(self):
#        data = {"txs_hashes":[self.scid]}
#        response = self.connection.rpc_daemon(data).json()
#        print(response['txs'][0]['sc']['F']['DepositAndChangeValue'])

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

