import os
from flask import Flask, g
from cm.app.constant import SIGNATURE,CM_NAME
import pika
import logging
log = logging.getLogger(__name__)
class CalculationModuleRpcClient(object):
    def __init__(self):
        parameters = pika.URLParameters(constant.CELERY_BROKER_URL_LOCAL)  # Update to local broker URL
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            print(self.response)

    def call(self, data):
        self.response = None
        self.corr_id = constant.CM_REGISTER_Q
        self.channel.basic_publish(exchange='',
                                   routing_key=constant.CM_REGISTER_Q,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=constant.CM_REGISTER_Q,
                                   ),
                                   body=data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # Apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # Register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/computation-module')

    # Register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    return app

