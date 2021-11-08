from uuid import uuid4

from flask import Blueprint
from flask import request
from typing import Dict

from gateway.rest_resources.dialer.funcs import send_cti_command

dialer_bp = Blueprint('dialer', __name__, url_prefix='/')


@dialer_bp.route('/calls', methods=['POST'])
def make_calls():
    """Endpoint - Método HTTP para realizar discagens automáticas

    Returns:
        Dict: Dicionário contendo o sucesso da execução
    """

    data = request.get_json()

    amount = data['amount']
    trunk = data['trunk']
    destination = list(set(data['destination'])) if isinstance(data['destination'], list) else [data['destination']]

    if amount < len(destination):
        return {'message': 'Quantidade de destinos únicos é maior do que a quantidade de chamadas'}, 400

    timeout = data['timeout']

    per_destination = int(amount / len(destination))
    rest = int(amount % len(destination))

    map_destination = {each: per_destination for each in destination}
    if rest:
        map_destination[destination[0]] = map_destination[destination[0]] + rest

    process_id = str(uuid4())

    for key, value in map_destination.items():
        dial_string = f'{trunk}/{key}'
        res = send_cti_command('python', [
            'fs_scripts.make_call',
            dial_string,
            key,
            process_id,
            str(timeout),
            str(value)
        ])
        print(res)

    return {'success': True}
