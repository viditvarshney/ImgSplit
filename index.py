''' 
 High-Dimensional Medical Imaging Code Challenge
@author: Vidit Varshney

'''

#importing the required modules

import tornado.web
import tornado.ioloop
from PIL import Image
import numpy as np
import imageio
import matplotlib.pyplot as plt
import os
import glob2


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
        self.write("The Link of your Original Image →")
        self.write(f"'http://localhost:8090/img/{f.filename}'")

        # Taking the latest image modified in the image folder.

        ts = 0
        found = None
        for file_name in glob2.glob('./img/*'):
            fts = os.path.getmtime(file_name)
            if fts > ts:
                ts = fts
                found = file_name

        print(found)

        img = imageio.imread(found)

        # Split in three channels i.e., RGB
        red = img[:, :, 0]
        green = img[:, :, 1]
        blue = img[:, :, 2]

        # Plot
        fig, axs = plt.subplots(2,2)
        fig.canvas.set_window_title("Splits the given image into RGB")

        cax_00 = axs[0,0].imshow(img)
        cax_01 = axs[0,1].imshow(red, cmap='Reds')
        cax_10 = axs[1,0].imshow(green, cmap='Greens')
        cax_11 = axs[1,1].imshow(blue, cmap='Blues')

        plt.show()

        # Developing the Matrix for every channel i.e RGB
        r_arr = np.asarray(red)
        g_arr = np.asarray(green)
        b_arr = np.asarray(blue)

        # setting mode to NONE, and merging the image
        imr=Image.fromarray(r_arr,mode=None)
        imb=Image.fromarray(g_arr,mode=None)
        img=Image.fromarray(b_arr,mode=None)

        #merge
        merged=Image.merge("RGB",(imr,imb,img))
        merged.show(title = "Original Image")

        # Delete the file automatically after displaying the image
        os.remove(found)             


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
