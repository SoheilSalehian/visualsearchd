from flask import request, jsonify, Flask
import urllib
import random
import base64
from inception import *

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    image_data = get_request()
    pool3 = sess.graph.get_tensor_by_name('incept/pool_3:0')
    pool3_features = sess.run(pool3,{png_data: image_data})
    results = [k.split('/')[-1] for k in nearest(np.squeeze(pool3_features),index,files)]
    final = []
    for fname in results:
      fname = "https://s3.amazonaws.com/" + BUCKET_NAME + "/" + fname
      final.append(fname)
    return jsonify(final=final)


@app.route('/quick', methods=['POST'])
def search_quick():
    image_data = get_request()
    pool3 = sess.graph.get_tensor_by_name('incept/pool_3:0')
    pool3_features = sess.run(pool3,{png_data: image_data})
    results = [k.split('/')[-1] for k in nearest(np.squeeze(pool3_features),index,files)]

    links = []

    for fname in results:
      fname = "https://s3.amazonaws.com/" + BUCKET_NAME + "/" + fname
      links.append(fname)
    return jsonify(links=links)


@app.route('/')
def hello_world():
    return 'Visual similarity engine.'


def get_request():
    image_url = request.get_json(force=True)
    image_url = image_url["image_url"]
    urllib.urlretrieve(image_url, "test.png")
    image_data = ''
    with open("test.png", "rb") as image_file:
      image_data = image_file.read()
    return image_data



if __name__ == '__main__':
    print "Loading inception network..."
    png_data = load_network(True)
    sess = tf.InteractiveSession()
    print "Loading index..."
    index,files = load_index()
    print "Server started :8000"
    app.run(host="0.0.0.0",port=8000,debug=False)
