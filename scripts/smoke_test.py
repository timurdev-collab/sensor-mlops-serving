"""Run after starting python -m service.api locally."""
import json
from urllib.request import Request,urlopen

with urlopen('http://127.0.0.1:8001/health',timeout=5) as r:
    assert json.load(r)['status']=='ok'
body=json.dumps({'pressure_bar':2.1,'flow_lpm':60,'temperature_c':25}).encode()
req=Request('http://127.0.0.1:8001/predict',data=body,headers={'Content-Type':'application/json'})
with urlopen(req,timeout=5) as r:
    result=json.load(r)
assert result['anomaly'] is True
print('Local HTTP smoke test passed:',result)
