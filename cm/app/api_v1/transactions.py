import json
import os
import socket

import requests
from flask import request, jsonify, send_from_directory

from cm.app import CalculationModuleRpcClient  # Assuming CalculationModuleRpcClient is defined
from cm.app import constant
from . import api
from .calculation_module import filter_data  # filter_data function is defined in calculation_module.py
from ..constant import SIGNATURE,CM_NAME

UPLOAD_DIRECTORY = './uploads'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@api.route('/files/<string:filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True)


@api.route('/register/', methods=['POST'])
def register():
    print('CM will begin registration')
    ip = socket.gethostbyname(socket.gethostname())
    base_url = 'http://' + str(ip) + ':' + str(constant.PORT) + '/'
    signature_final = SIGNATURE

    calculation_module_rpc = CalculationModuleRpcClient()
    signature_final["cm_url"] = base_url
    payload = json.dumps(signature_final)
    response = calculation_module_rpc.call(payload)
    return response


def save_file(filename, url):
    print('CM is computing and will download files with URL:', url)
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            path = os.path.join(UPLOAD_DIRECTORY, filename)
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print('File saved successfully')
            return path
        else:
            print('API unable to download file:', r.status_code)
            return None
    except Exception as e:
        print('Error downloading file:', e)
        return None


@api.route('/compute/', methods=['POST'])
def compute():
    print('CM will Compute ')
    data = request.get_json()

    filtered_data = filter_data(data)

    output_directory = UPLOAD_DIRECTORY
    result = filtered_data.to_json()

    response = {'result': result}

    response = jsonify(response)
    return response