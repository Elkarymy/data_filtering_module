#!/usr/bin/env python
import logging
import os
from cm.app import create_app, log
from cm.app.constant import PORT, TRANFER_PROTOCOLE
import requests
import threading
import time
import socket

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

application = create_app(os.environ.get('FLASK_CONFIG', 'development'))

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            LOGGER.info('In start loop')
            try:
                # Get the external IP
                ip = socket.gethostbyname(socket.gethostname())
                # The CM will run its register request
                LOGGER.info('ip ', ip)
                base_url = f"{TRANFER_PROTOCOLE}{ip}:{PORT}/"
                headers = {'Content-Type': 'application/json'}
                r = requests.post(f"{base_url}computation-module/register/", headers=headers)
                print(r.status_code)
                LOGGER.info('r.status_code ', r.status_code)
                if r.status_code == 200:
                    print('Server started, quitting start_loop')
                    LOGGER.info('Server started, quitting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                LOGGER.info('Server not yet started')
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    LOGGER.info('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()

log.info(application)

if __name__ == '__main__':
    # start_runner()
    application.run(host='0.0.0.0', port=PORT)
