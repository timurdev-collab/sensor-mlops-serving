import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from service.api import Handler

class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_health(self):
        with urlopen(self.base + "/health", timeout=3) as response:
            self.assertEqual(json.load(response)["status"], "ok")

    def test_prediction_response_contract(self):
        data = json.dumps({"pressure_bar": 2, "flow_lpm": 60, "temperature_c": 25}).encode()
        request = Request(self.base + "/predict", data=data, headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=3) as response:
            payload = json.load(response)
        self.assertEqual(payload["model_version"], "rules-v1")
        self.assertTrue(payload["anomaly"])
        self.assertIn("low_pressure", payload["reasons"])

    def test_malformed_request_is_400(self):
        request = Request(self.base + "/predict", data=b"not-json",
                          headers={"Content-Type": "application/json"})
        with self.assertRaises(HTTPError) as context:
            urlopen(request, timeout=3)
        self.assertEqual(context.exception.code, 400)

    def test_metrics_endpoint(self):
        with urlopen(self.base + "/metrics", timeout=3) as response:
            text = response.read().decode()
        self.assertIn("sensor_requests_total", text)
        self.assertIn("sensor_errors_total", text)

if __name__ == "__main__":
    unittest.main()
