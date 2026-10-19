from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json,time,logging,threading
from service.model import predict

logging.basicConfig(level=logging.INFO,format='%(message)s')
STATS={'requests':0,'errors':0,'total_latency_seconds':0.0}
LOCK=threading.Lock()

class Handler(BaseHTTPRequestHandler):
    def respond(self,status,data,content_type='application/json'):
        body=(json.dumps(data) if not isinstance(data,str) else data).encode()
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path=='/health':
            return self.respond(200,{'status':'ok'})
        if self.path=='/metrics':
            with LOCK:
                s=STATS.copy()
            output='\n'.join([
                f'sensor_requests_total {s["requests"]}',
                f'sensor_errors_total {s["errors"]}',
                f'sensor_request_duration_seconds_sum {s["total_latency_seconds"]:.6f}'
            ])+'\n'
            return self.respond(200,output,'text/plain; version=0.0.4')
        self.respond(404,{'error':'not found'})

    def do_POST(self):
        if self.path!='/predict':
            return self.respond(404,{'error':'not found'})
        start=time.perf_counter()
        error=False
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size>8192 or size<=0:
                raise ValueError('invalid request size')
            payload=json.loads(self.rfile.read(size))
            if not isinstance(payload,dict):
                raise ValueError('JSON object required')
            result=predict(payload)
            self.respond(200,result)
        except (ValueError,json.JSONDecodeError) as exc:
            error=True
            self.respond(400,{'error':str(exc)})
        finally:
            duration=time.perf_counter()-start
            with LOCK:
                STATS['requests']+=1
                STATS['errors']+=int(error)
                STATS['total_latency_seconds']+=duration
            logging.info(json.dumps({'event':'inference_request','error':error,
                'duration_ms':round(duration*1000,3)}))

if __name__=='__main__':
    print('Listening on port 8001')
    ThreadingHTTPServer(('0.0.0.0',8001),Handler).serve_forever()
