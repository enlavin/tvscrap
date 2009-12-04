from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class GzipHelperHandler(webapp.RequestHandler):
    def get(self):
        import urllib, urllib2, gzip, StringIO
        url = urllib.unquote(self.request.path[len("/gzhelper/"):])
        req = urllib2.Request(url)
        req.add_header('Accept-encoding', 'gzip')
        opener = urllib2.build_opener()
        f = opener.open(req)
        #cdata = f.read()
        #sio = StringIO.StringIO(cdata)
        #gz = gzip.GzipFile(fileobj=sio)
        #uncompressed = gz.read()
        uncompressed = f.read()
        self.response.headers["Content-type"] = "application/x-bittorrent"
        self.response.headers["Content-length"] = len(uncompressed)
        self.response.headers["Content-disposition"] = "attachment; %s" % self.request.uri
        self.response.out.write(uncompressed)

def main():
  application = webapp.WSGIApplication([
      ('/gzhelper.*', GzipHelperHandler), 
    ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()

