import unittest
from werkzeug.exceptions import NotFound
from app import create_app
import os.path
import pandas as pd
from shutil import copyfile
from .test_client import TestClient

UPLOAD_DIRECTORY = '/var/hotmaps/cm_files_uploaded'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    os.chmod(UPLOAD_DIRECTORY, 0o777)


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = TestClient(self.app, )

    def tearDown(self):
        self.ctx.pop()

    def test_compute(self):
        raster_file_path = 'tests/data/raster_for_test.tif'
        raster_file_path2 = 'tests/data/nuts_id.tif'
        path_input_parameter = "tests/data/INPUTS_CALCULATION_MODULE.xlsx"

        # simulate copy from HTAPI to CM
        save_path = UPLOAD_DIRECTORY + "/raster_for_test.tif"
        copyfile(raster_file_path, save_path)
        save_path2 = UPLOAD_DIRECTORY + "/nuts_id.tif"
        copyfile(raster_file_path2, save_path2)

        inputs_raster_selection = {}
        inputs_parameter_selection = {}

        inputs_raster_selection["heat"] = save_path
        inputs_raster_selection["nuts_id_number"] = save_path2

        df = pd.read_excel(path_input_parameter)
        inputs_parameter_selection = df.set_index(df.input_parameter_name)["input_value"].to_dict()

        # register the calculation module a
        payload = {"inputs_raster_selection": inputs_raster_selection,
                   "inputs_parameter_selection": inputs_parameter_selection}

        rv, json = self.client.post('computation-module/compute/', data=payload)

        self.assertTrue(rv.status_code == 200)