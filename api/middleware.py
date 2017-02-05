class AddResponseHeader:
    def process_response(self, req, resp, resource):
        resp.set_header('Access-Control-Allow-Origin', 'http://localhost:8000')

components = [AddResponseHeader()]
