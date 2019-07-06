# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
import os
import urllib
DISK = "/mnt/d/website/"
# import pdb

# Website
def application(environ, start_response):
    path = environ['PATH_INFO'].encode('iso-8859-1').decode('utf8')
    #path = urllib.parse.unquote(environ['PATH_INFO'].encode('iso-8859-1').decode('utf8'))
    dir = path[1:] # otherwise the os.path.join won't work
    htext = '<ol>'
    p = os.path.join(DISK,dir)
    if not os.path.exists(p):
        start_response('404 Not Found', [('Content-Type', 'text/html; charset=utf-8')])
        return [('%s Not Exists!' % path).encode('utf-8')]
    if os.path.isdir(p):
        directories = os.listdir(p)
        for d in directories:
            # pdb.set_trace()
            htext += '<li><a href="%s/%s">%s</a></li>' % ('/' + dir if dir else dir,d,d)
        htext += '</ol>'
        backText = '<h4 style="text-align: center"><a href="../"><b>BACK</b></a></h4>' if dir else ''
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        body = '<h1 style="text-align: center">肖恩·饼 的 网站</h1><h3 style="text-align: center">-----宋乔依是最可爱的人🐖</h3><h3 style="text-align: center">-----来帮忙的盒子也是🐖</h3><h4>开车了，嘟嘟嘟:</h4>%s%s<h6 style="text-align: center">您使用的浏览器/系统: %s</h6>' % (htext,backText,environ['HTTP_USER_AGENT'])
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
port = 8888
httpd = make_server('', port, application)
print('Serving HTTP on port %s...' % port)
# 开始监听HTTP请求:
httpd.serve_forever()
