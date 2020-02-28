import tornado.web
import tornado.ioloop

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        files = self.request.files["Pictures"]
        for f in files:
            fh = open(f"imguploader/img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()

        self.write(f"http://localhost:8090/img/{f.filename}")


if (__name__ == "__main__"):
    app = tornado.web.Application([

        ("/", uploadHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"})
    ])


    app.listen(8090)
    print("Listening on port 8090")

    tornado.ioloop.IOLoop.instance().start()