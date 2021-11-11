from datetime import datetime
from io import StringIO
import csv

from flask import Blueprint, make_response
from flask import request
from typing import Dict, List

from gateway.libs.database.mongo_connection import get_mongo_connection

report_bp = Blueprint('report', __name__, url_prefix='/')


def get_csv_stream(final_list: List) -> StringIO:
    fieldnames = [
        'process_id',
        'timestamp',
        'destination',
        'call_id',
        'start',
        'end',
        'answer',
        'total_seconds',
        'bill_seconds',
        'hangup_cause'
    ]
    si = StringIO()
    cw = csv.DictWriter(si, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    cw.writeheader()

    for call_processor in final_list:
        for call_detail in call_processor['calls']:
            row = {
                'process_id': call_processor['process_id'],
                'timestamp': call_processor['timestamp'],
                'destination': call_detail['destination'],
                'call_id': call_detail['call_id'],
                'start': call_detail['start'],
                'end': call_detail['end'],
                'answer': call_detail['answer'],
                'total_seconds': call_detail['total_seconds'],
                'bill_seconds': call_detail['bill_seconds'],
                'hangup_cause': call_detail['hangup_cause']
            }
            cw.writerow(row)

    return si


@report_bp.route('/report', methods=['GET'])
def get_report():
    """Endpoint - Método HTTP para realizar discagens automáticas

    Returns:
        Dict: Dicionário contendo o sucesso da execução
    """

    query_string = request.args

    init_date = datetime.strptime(query_string['init_date'], '%Y-%m-%dT%H:%M:%S')
    finn_date = datetime.strptime(query_string['finn_date'], '%Y-%m-%dT%H:%M:%S')
    export_type = query_string.get('export_type', 'json')

    calls_processor_db = get_mongo_connection('dialer', 'calls_processor')
    calls_details_db = get_mongo_connection('dialer', 'calls_details')

    final_list = []

    list_calls_processor = calls_processor_db.find({'timestamp': {'$gte': init_date, '$lte': finn_date}})
    for call_processor in list_calls_processor:
        data = {
            'process_id': call_processor['process_id'],
            'timestamp': call_processor['timestamp'].strftime('%d/%m/%Y %H:%M:%S'),
            'calls': []
        }

        list_calls_details = calls_details_db.find({'process_id': call_processor['process_id']})
        for call_details in list_calls_details:
            data['calls'].append({
                'destination': call_details['destination'],
                'call_id': call_details['call_id'],
                'start': call_details['start'].strftime('%d/%m/%Y %H:%M:%S'),
                'end': call_details['end'].strftime('%d/%m/%Y %H:%M:%S'),
                'answer': call_details['answer'].strftime('%d/%m/%Y %H:%M:%S') if call_details['answer'] else '',
                'total_seconds': call_details['total_seconds'],
                'bill_seconds': call_details['bill_seconds'],
                'hangup_cause': call_details['hangup_cause']
            })

        final_list.append(data)
    if export_type == 'csv':
        file_name = f'export_calls_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.csv'
        output = make_response(get_csv_stream(final_list).getvalue())
        output.headers["Content-Disposition"] = f'attachment; filename={file_name}'
        output.headers["Content-type"] = "text/csv"
        return output
    else:
        return {'list': final_list}
