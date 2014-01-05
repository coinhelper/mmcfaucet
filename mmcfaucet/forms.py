
from flask import request
from flask_wtf import Form, RecaptchaField
from wtforms import TextField
from wtforms.validators import DataRequired
from wtforms import ValidationError

from connection import bitcoind, database

import time


def check_tx(ip, address):
    t = int(time.time())
    ip_records = database.faucet.find({
        "ip": ip,
        "created_at": {
            "$gt": t - int(3600 * 24),
        }
    }).count()

    if ip_records == 0:
        addr_records = database.faucet.find({
            "address": address,
            "created_at": {
                "$gt": t - int(3600 * 24)
            }
        }).count()

        if addr_records == 0:
            return True

    return False


class MyForm(Form):
    address = TextField('name', validators=[DataRequired()])
    recaptcha = RecaptchaField()

    def validate_address(form, field):
        result = bitcoind.validateaddress(field.data)

        if not result.isvalid:
            raise ValidationError('invalid mmc address.')

        if not check_tx(request.remote_addr, field.data):
            raise ValidationError('try tomorrow.')
