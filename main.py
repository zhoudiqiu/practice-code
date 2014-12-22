import os.path
import tornado.locale
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.options import define, options
#import pymongo
import json
import urllib
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
#from XX import XX #the os file completed by PS.

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		self.handlers=[
			(r"/", MainHandler),
			(r"/requestToServer",RequestToServerHandler),
			(r"/post",PostHandler),
		]
	settings = {
		#to be completed
		"debug":True,
		}
	
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world!")

class RequestToServerHandler(tornado.web.RequestHandler):
	def get(self):
		#Request to the server for update information about the repositories.
		query=self.get_argument('q')
		client=tornado.httpclient.HTTPClient()
		response=client.fetch("https://evernote.com/search.json?"+\
			urllib.urlencode({"q" : query, "result_type" : "recent"}))
	def on_response(self, response):
		body=json.loads(response.body)
		f=open('repository.json','w')
		f.write(self.request.body.decode('utf-8'))
		f.close()
		repository=json.loads(self.request.body.decode('utf-8'))
		resultCount=len(body['results'])
		#if body=null:
		#	self.set.status(404)
		return repository,resultCount

class PostHandler(tornado.web.RequestHandler):
	def post(self):
		f = open('temp.json', 'w')
		f.write(self.request.body.decode('utf-8'))
		f.close()
		c = S3Connection('AKIAI7MUPCCLREXSEEAQ', 'dvfHGw3IQ2f1mvNteHz+ltQMOEc3ms105G9Lsb7G')
		b = c.get_bucket('pongoboy')
		k = Key(b)
		k.key = 'f'
		k.set_contents_from_filename('temp.json')



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
    	[(r"/", MainHandler),
			(r"/requestToServer",RequestToServerHandler),
			(r"/post",PostHandler),]
			,debug=True
    	)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()