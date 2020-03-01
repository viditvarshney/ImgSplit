''' 
 High-Dimensional Medical Imaging Code Challenge
@author: Vidit Varshney

'''

#importing the required modules

import tornado.web
import tornado.ioloop

'''
make a class which handles the images
uploaded by the user and save to the ' img' folder 
'''

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    # post function: takes request for the image

    def post(self):
        files = self.request.files["Pictures"]
        for f in files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()

        self.write(f"http://localhost:8090/img/{f.filename}")

# main function: give acces to the client to acces the img folder


if (__name__ == "__main__"):
    app = tornado.web.Application([

        ("/", uploadHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"})   #saves the image in the img folder
    ])

    # listen a specific port 

    app.listen(8090)
    print("Listening on port 8090")

    tornado.ioloop.IOLoop.instance().start()