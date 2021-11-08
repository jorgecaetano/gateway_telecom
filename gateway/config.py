import os
from base64 import b64encode

FS_BASE_INTERFACE = os.environ.get('FS_BASE_INTERFACE', 'txtapi')
FS_REQUEST_PROTOCOL = os.environ.get('FS_PROTOCOL', 'http')
FS_HOST = os.environ.get('FS_HOST', '127.0.0.1')
FS_PORT = os.environ.get('FS_PORT', '8080')
FS_USER = os.environ.get('FS_USER', 'freeswitch')
FS_PASSWORD = os.environ.get('FS_PASSWORD', 'works')

FS_BASE_URL = f'{FS_REQUEST_PROTOCOL}://{FS_HOST}:{FS_PORT}/{FS_BASE_INTERFACE}'
FS_BASE_PASSWORD = b64encode(f'{FS_USER}:{FS_PASSWORD}'.encode()).decode()
FS_PASS_ALGORITMH = 'Basic'
FS_AUTHORIZATION = f'{FS_PASS_ALGORITMH} {FS_BASE_PASSWORD}'
