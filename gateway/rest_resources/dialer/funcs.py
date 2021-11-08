import requests

from gateway.config import FS_BASE_URL, FS_AUTHORIZATION


def send_cti_command(command: str, args: list):
    """
    Função para acionamento da API de integração do FreeSwitch

    :param command: Comando a ser executado na API
    :param args: Argumentos do comandos em questão
    :return: Tupla contendo o texto do retorno e o status http do retorno
    """

    url = f'{FS_BASE_URL}/{command}?{" ".join(args)}'

    headers = {
        'Authorization': FS_AUTHORIZATION
    }

    res = requests.get(url, headers=headers)
    return res.text, res.status_code
