# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
import os
import urllib
DISK = "D:/website/"

# Website
def application(environ, start_response):
    path = environ['PATH_INFO'].encode('iso-8859-1').decode('utf8')
    #path = urllib.parse.unquote(environ['PATH_INFO'].encode('iso-8859-1').decode('utf8'))
    dir = path[1:]
    htext = '<ol>'
    p = os.path.join(DISK,dir)
    if not os.path.exists(p):
        start_response('404 Not Found', [('Content-Type', 'text/html; charset=utf-8')])
        return [('%s Not Exists!' % path).encode('utf-8')]
    if os.path.isdir(p):
        directories = os.listdir(p)
        for d in directories:
            htext += '<li><a href="%s/%s">%s</a></li>' % (dir,d,d)
        htext += '</ol>'
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        body = '<h1>宋乔依是最可爱的人🐖</h1><a href="http://download.189cube.com/update/App/android/yueme.apk">Telecom APK</a><h2>http://192.168.1.18:1080/pac?t=20190428220025318&secret=+CsN4xParBuqHxsAw+p94ICCJGnM0nkD+KetTNfioNQ=</h2>%s<h3>您使用的浏览器/系统: %s</h3>' % (htext,environ['HTTP_USER_AGENT'])
        return [body.encode('utf-8')]
    else:
        size = os.path.getsize(p)
        start_response('200 OK',[('Content-Type', 'application/octet-stream'), ('Content-Length', str(size))])
        #with open(p,'rb') as body:
        body = open(p,'rb')
        return fbuffer(body,1048576)

# Read file in chunks
def fbuffer(f, chunk_size):
    '''Generator to buffer file chunks'''  
    while True:
        chunk = f.read(chunk_size)      
        if not chunk: break
        yield chunk

# 创建一个服务器，IP地址为空，端口是80，处理函数是application:
httpd = make_server('', 80, application)
print('Serving HTTP on port 80...')
# 开始监听HTTP请求:
httpd.serve_forever()
