class AddResponseHeader:
    def process_response(self, req, resp, resource):
        resp.set_header('Access-Control-Allow-Origin', 'http://localhost:8000')
        resp.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

components = [AddResponseHeader()]
