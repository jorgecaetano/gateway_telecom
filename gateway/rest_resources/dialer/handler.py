from datetime import datetime
from numbers import Number
from threading import Thread
from time import sleep
from uuid import uuid4

from flask import Blueprint
from flask import request
from typing import Dict, AnyStr

from gateway.libs.database.mongo_connection import get_mongo_connection
from gateway.rest_resources.dialer.funcs import send_cti_command

dialer_bp = Blueprint('dialer', __name__, url_prefix='/')


@dialer_bp.route('/calls', methods=['POST'])
def make_calls():
    """Endpoint - Método HTTP para realizar discagens automáticas

    Returns:
        Dict: Dicionário contendo o sucesso da execução
    """

    def _cti_make_calls(_dial_string: AnyStr, _destination: AnyStr, _cpf_cnpj: AnyStr, _process_id: AnyStr, _timeout: Number, _amount: Number, _record_call: AnyStr):
        res = send_cti_command('python', [
            'fs_scripts.make_call',
            _dial_string,
            _destination,
            _cpf_cnpj,
            _process_id,
            str(_timeout),
            str(_amount),
            record_call
        ])

    data = request.get_json()

    amount = data['amount']
    trunk = data['trunk']
    destination = list(set(data['destination'])) if isinstance(data['destination'], list) else [data['destination']]

    if amount < len(destination):
        return {'message': 'Quantidade de destinos únicos é maior do que a quantidade de chamadas'}, 400

    timeout = data['timeout']
    cpf_cnpj = data['cpf_cnpj']
    record_call = 'TRUE' if data['record_call'] else 'FALSE'

    per_destination = int(amount / len(destination))
    rest = int(amount % len(destination))

    map_destination = {each: per_destination for each in destination}
    if rest:
        map_destination[destination[0]] = map_destination[destination[0]] + rest

    process_id = str(uuid4())

    thread_list = []

    calls_processor_db = get_mongo_connection('dialer', 'calls_processor')
    calls_processor_db.insert_one({
        'process_id': process_id,
        'destination': destination,
        'timestamp': datetime.now()
    })

    for key, value in map_destination.items():
        for i in range(value):
            dial_string = f'{trunk}/{key}'
            sleep(0.05)
            _dialer_thread = Thread(target=_cti_make_calls, args=(dial_string, key, cpf_cnpj, process_id, timeout, 1, record_call))
            thread_list.append(_dialer_thread)
            _dialer_thread.start()

    for each in thread_list:
        each.join()

    return {'success': True}
