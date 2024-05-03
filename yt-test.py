from http.server import BaseHTTPRequestHandler, HTTPServer
from pytube import YouTube
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/download':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            link = data['link']
            result = self.download_video(link)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(result, 'utf-8'))
        else:
            self.send_error(404)

    def download_video(self, link):
        try:
            youtube_obj = YouTube(link)
            youtube_obj = youtube_obj.streams.get_highest_resolution()
            youtube_obj.download()
            return "Download completed successfully!"
        except Exception as e:
            return f"An error has occurred: {str(e)}"

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
