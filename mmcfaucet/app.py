from flask import Flask
from flask import request
from flask import render_template

import random
import time

from decimal import Decimal
from connection import database

import bitcoinrpc
import bitcoinrpc.config
from bitcoinrpc.exceptions import *

from connection import database

app = Flask(__name__)
app.config.from_pyfile('settings.py')

from forms import MyForm
from connection import bitcoind


def add_transaction_to_database(address, amount, ip, transaction):
    database.faucet.insert({
        'address': address,
        'ip': ip,
        'amount': amount,
        'transaction': transaction,
        'created_at': int(time.time())
    })


def send_to_address(address):
    list1, list2, list3, list4 = random.uniform(0.01, 0.5), random.uniform(0.01, 0.1), random.uniform(0.01, 0.5), random.uniform(0.01, 0.2)
    all_ = [list1, list2, list3, list4]
    random.shuffle(all_)

    amount = Decimal(str(all_[0])[0:7])
    result = bitcoind.sendfrom('faucet', address, float(amount))

    return result, amount


@app.route('/', methods=['POST', 'GET'])
def index():

    balance = bitcoind.getbalance('faucet')
    if balance < Decimal('0.10000000'):
        return render_template("base.html", balance=False)

    if request.method == 'GET':
        form = MyForm()

    elif request.method == 'POST':

        form = MyForm(request.form)
        if form.validate():
            result, amount = send_to_address(form.data.get("address"))
            add_transaction_to_database(form.data.get("address"), float(amount), request.remote_addr, result)
            return render_template('success.html', result=result, amount=amount)

    template_data = {
        "form": form,
        "balance": True,
    }

    return render_template("base.html", **template_data)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

