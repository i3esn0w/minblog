#encoding:utf8
import tornado.ioloop
import tornado.web
import os



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('blog.html')
        
setting = {
	"base_url": tornado.options.options.url,
	"template_path": "templates",
	"cookie_secret": "s3cr3tk3y",
	"config_filename": tornado.options.options.config,
	"compress_response": True,
	"default_handler_class": controller.base.NotFoundHandler,
	"xsrf_cookies": True,
	"static_path": "static",
	"download": "./download",
	"session": {
		"driver": "redis",
		"driver_settings": {
			"host": "localhost",
			"port": 6379,
			"db": 1
		},
		"force_persistence": False,
		"cache_driver": True,
		"cookie_config": {
			"httponly": True
		},
	},
	"thread_pool": futures.ThreadPoolExecutor(4)
}

config = {}
try:
	with open(setting["config_filename"], "r") as fin:
		config = yaml.load(fin)
	for k, v in config["global"].items():
		setting[k] = v
	if "session" in config:
		setting["session"]["driver_settings"] = config["session"]
except:
	print "cannot found config.yaml file"
	sys.exit(0)
try:
	client = motor.MotorClient(config["database"]["config"])
	database = client[config["database"]["db"]]
	setting["database"] = database
except:
	print "cannot connect mongodb, check the config.yaml"
	sys.exit(0)


if __name__ == "__main__":
	try:
		application.listen(tornado.options.options.port)
		tornado.ioloop.IOLoop.instance().start()
	except:
		import traceback
		print traceback.print_exc()
	finally:
		sys.exit(0)

application = tornado.web.Application([
	(r"^/", "IndexHandler"),
	(r"^/download/(.*)", "controller.download.DownloadHandler", {"path": "./download/"})
], **setting)

if __name__=="__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()