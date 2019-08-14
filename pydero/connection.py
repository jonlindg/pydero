
import requests

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
        return requests.post(self.access_point_wallet+mode,headers=self.headers,json=data)


    def rpc_daemon(self,data,mode='/gettransactions'):
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

