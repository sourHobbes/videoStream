# import the necessary packages
from __future__ import print_function
import cv2
import signal

def handler(signum, frame):
    try:
        print("Caught signal " + str(signum))
        import sys
        sys.exit(0)
    except OSError as e:
        if e.errno != errno.EAGAIN:
            print('Signal handler write error')
            os._exit(1)
signal.signal(signal.SIGINT, handler)
# load the image and convert it to grayscale
image = cv2.imread("jurassic_world.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Original", image)

# initialize the AKAZE descriptor, then detect keypoints and extract
# local invariant descriptors from the image
detector = cv2.AKAZE_create()
(kps, descs) = detector.detectAndCompute(gray, None)
print("keypoints: {}, descriptors: {}".format(len(kps), descs.shape))

# draw the keypoints and show the output image
cv2.drawKeypoints(image, kps, image, (0, 255, 0))
cv2.imshow("Output", image)
while True:
    k = cv2.waitKey(1) & 0xff
    #print(k)

