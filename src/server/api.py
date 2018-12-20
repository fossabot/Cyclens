# coding: utf-8

from flask import Flask, Response, render_template, jsonify, request
import json
import numpy as np
import cv2
from matplotlib import pyplot as plt

app = Flask(__name__)

headerJSON = {'Content-Type': 'application/json'}
headerJPEG = {'Content-Type': 'image/jpeg'}

global stream


@app.route('/')
def index():
    return render_template("../../data/web/index.html")


@app.route('/test/sender', methods=['POST'])
def route_test():
    resp = Response("Test")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers = headerJSON

    return resp


@app.route('/test/receiver', methods=['GET'])
def route_test2():
    resp = Response(response="TEST", status=200, mimetype="image/jpeg")
    resp.headers["Content-Type"] = "image/jpeg; charset=utf-8"
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/test', methods=['GET'])
def route_test3():
    test = {'result': 'gender=male'}
    data = json.dumps({'data': test})

    resp = Response(response=data, status=200, mimetype="application/json")
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


# Test1: curl -i -X POST -H "Content-Type: image/jpeg" -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
# Test2: curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
# Test3: curl -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo


@app.route('/test/demo', methods=['POST'])
def demo():
    print(request.files)
    data = request.files['fileToUpload'].read()

    print('FILE')

    npimg = np.frombuffer(data, np.uint8)

    # PRE-PROCESSOR

    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    small = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)

    edges = cv2.Canny(small, 100, 200)


    #cv2.imshow('HSV image', edges)
    #cv2.waitKey(0)

    # PROCESSOR

    hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    #plt.hist(img.ravel(), 256, [0, 256])
    #plt.show()

    # ...

    # POST-PROCESSOR

    result = {'result': 'size={}x{}'.format(img.shape[1], img.shape[0])}

    response_pickled = json.dumps({'data': result}, cls=NumpyEncoder)

    resp = Response(response=response_pickled, status=200)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'

    return resp

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.144', port=5000)

