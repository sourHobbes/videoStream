import cv2
import signal
from install_exit_int import signal_handler
import scipy.misc as misc
import StringIO
import time
#from gevent import monkey
#monkey.patch_all()
#monkey.patch_socket()
#from gevent.wsgi import WSGIServer

def shutdown_server():
    import sys
    sys.exit()

signal_handler(shutdown_server)

liveThreads = 0

try:
    from MyQueue import MyQueue
    q = MyQueue(2)
    pass
except Exception, e:
    print("failed to initilize q" + str(e))

class Images(object):
    def __init__(self, ignore):
        self.imglist = list()
        img = None
        for i in xrange(0, 50):
            try:
                img = misc.imread('img-{0}'.format(i) + ".jpg")
            except Exception, e:
                print e
                continue
            self.imglist.append(img)
            print("len of images is {0}".format(len(self.imglist)))
    
    def get_image(self, i):
        return self.imglist[i % 50]

class CamImages(object):
    def __init__(self, q):
        self.camera = cv2.VideoCapture(0)
        self.q = q

    def get_image(self, i):
        _, img = self.camera.read()
        self.q.add(img)
        #return img
        return self.q.get(i)

    def close(self):
        self.camera.release()


imgs_obj = CamImages(q)

def gen_images(imgs_obj, idx):
    i = int(time.time()) % 50
    #img = misc.imread('img-{0}'.format(i) + ".jpg")
    #f, img = camera.read()
    #cv2.imshow("webcam",img)
    #print type(img)
    yield imgs_obj.get_image(idx)


#while True:
#    img = gen_images().next()
#    cv2.imshow("webcam", img)
#    if (cv2.waitKey(5) != -1):
#       break

from flask import Flask, render_template, Response, request
app = Flask(__name__, template_folder="static_content")

@app.route('/')
def index():
    return render_template('index.html')


def gen(imgs_obj, idx):
    i = 0
    while True: 
        try:
            frameJpeg = StringIO.StringIO()
            frame = gen_images(imgs_obj, idx).next()
            misc.imsave(frameJpeg, frame, format="JPEG")
            #misc.imsave('img-{0}'.format(i) + ".jpg", frame)
            i+=1
        except Exception, e:
            print("My xception" + e.message)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frameJpeg.getvalue() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    global liveThreads
    liveThreads+=1
    print('got request')
    try:
        return Response(gen(imgs_obj, liveThreads),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception, e:
        imgs_obj.close()
        print("released the capture")

if __name__ == '__main__':
    print("Starting app")
    try:
        #http_server = WSGIServer(('', 5000), app)
        #http_server.serve_forever()
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except Exception, e:
        print("caught error {0}".format(str(e)))
        raise e
