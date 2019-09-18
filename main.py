from http.server import HTTPServer, BaseHTTPRequestHandler
import db_init

q_funcs = {'/chats/add': db_init.add_chat,
           '/users/add': db_init.add_user,
           '/chats/get': db_init.get_chat,
           '/messages/get': db_init.get_messages,
           '/messages/add': db_init.add_message}


class MyHandler(BaseHTTPRequestHandler):

    def respond(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        try:

            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len).decode()
            query_func = q_funcs[self.path]
            response = query_func(post_body)
            self.respond(str(response).encode())

        except Exception as e:
            self.send_response(400)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 9000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
