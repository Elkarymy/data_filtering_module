# Set the Celery broker URL for Docker and local testing
CELERY_BROKER_URL_DOCKER = 'amqp://guest:guest@localhost:5672//'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'

# Choose the appropriate Celery broker URL based on the testing environment
# In this case, we're testing locally, so we'll use the local URL


# Other configuration parameters
CM_REGISTER_Q = 'rpc_queue_CM_register'
CM_NAME = 'CM - Data Filtering Module'
RPC_CM_ALIVE = 'rpc_queue_CM_ALIVE'
RPC_Q = 'rpc_queue_CM_compute'
CM_ID = 14
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80

CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
PORT = PORT_DOCKER


TRANFER_PROTOCOLE = 'http://'

# Define input parameters for the calculation module
INPUTS_CALCULATION_MODULE = {
    "field_of_intervention": {
        "name": "Field of Intervention",
        "type": "select",
        "options": ["Occupant presence", "Building insulation", "Energy consumption", "Other"]
    },
    "intervention_type": {
        "name": "Intervention Type",
        "type": "select",
        "options": ["Monetary incentives", "Regulatory measures", "Educational programs", "Other"]
    },
    "space_filter_options": {
        "name": "Space Filter Options",
        "type": "checkbox",
        "options": {
            "Residential": "Y",
            "Office": "N",
            "Educational": "N",
            "Other": "N"
        }
    }
}

# Define the SIGNATURE dictionary
SIGNATURE = {
    "category": "Data Filtering",
    "cm_name": CM_NAME,
    "wiki_url": "https://wiki.hotmaps.hevs.ch/en/Data-Filtering-Module",
    "layers_needed": [],
    "type_layer_needed": [],
    "type_vectors_needed": [],
    "cm_url": "Do not add something",
    "cm_description": "This computation module allows to filter data based on specified criteria.",
    "cm_id": CM_ID,
    "inputs_calculation_module": INPUTS_CALCULATION_MODULE,
    "authorized_scale": ["NUTS 3", "NUTS 2", "NUTS 1", "NUTS 0", "Hectare", "LAU 2"]
}

# Now you can use the above configurations in your application
