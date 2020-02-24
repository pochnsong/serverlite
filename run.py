# coding:utf--8

"""
简易的静态服务器
use: python3 run.py [port=8000] [site_dir='app']
"""
import sys
if sys.version_info[0] == 2:
    print('use Python3 start server')
    exit()

from wsgiref.simple_server import make_server
import mimetypes
import os


class WSGIHandler(object):
    def get_response(self, path):
        fpath = os.path.abspath(os.path.join(self.root, path))
        if os.path.isfile(fpath):
            content_type, encoding = mimetypes.guess_type(str(fpath))
            content_type = content_type or 'application/octet-stream'
            header = [('Content-Type', content_type)]
            if encoding:
                header.append(("Content-Encoding", encoding))

            with open(fpath, 'rb') as rf:
                content = rf.read()
                return '200 OK', header, [content]
        else:
            return '404 Not Found', [('Content-Type', 'text/html;charset=utf-8')], ['<h1>404 File Not Found</h1>'.encode('utf-8')]

    def __init__(self,  root=None):
        if not root:
            root = os.path.join(os.path.dirname(__file__), 'website')
        self.root = os.path.abspath(root)

        print('load site path', self.root)

    def __call__(self, environ, start_response):
        url = environ.get('PATH_INFO', '/')
        # print(environ['REQUEST_METHOD'], url)
        status_code, header, response = self.get_response(url.lstrip('/'))
        start_response(status_code, header)
        return response


if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    site_path = sys.argv[2] if len(sys.argv) > 2 else 'app'
    httpd = make_server('', int(port), WSGIHandler(site_path))
    print("Start server at http://0.0.0.0:{}".format(httpd.server_port))
    # 开始监听HTTP请求:
    httpd.serve_forever()
