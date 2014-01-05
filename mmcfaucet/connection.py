
from pymongo import Connection

import bitcoinrpc
import bitcoinrpc.config
import os

connection = Connection()
database = connection['memorycoin']


def patch_config(filename=None):
    filename = os.path.expanduser("~/.memorycoin/memorycoin.conf")
    if not os.path.exists(filename):
        filename = '/.memorycoin/memorycoin.conf'
    return bitcoinrpc.config.read_config_file(filename)

bitcoinrpc.config.read_default_config = patch_config


bitcoind = bitcoinrpc.connect_to_local()
