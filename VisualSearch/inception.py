import logging, glob, os
from tensorflow.python.platform import gfile
import tensorflow as tf
import numpy as np
from scipy import spatial
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from configs import INDEX_PATH, BUCKET_NAME


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='worker.log',
                    filemode='a')


DIMENSIONS = 2048
PROJECTIONBITS = 16
ENGINE = Engine(DIMENSIONS, lshashes=[RandomBinaryProjections('rbp', PROJECTIONBITS,rand_seed=2611),
                                      RandomBinaryProjections('rbp', PROJECTIONBITS,rand_seed=261),
                                      RandomBinaryProjections('rbp', PROJECTIONBITS,rand_seed=26)])



def load_network(png=False):
    ''' Load the network definitions and graph'''
    # Protobuf format for the newtwork here is binary
    with gfile.FastGFile('./model/network.pb', 'rb') as f:
        # Instantiate the Graph definition
        graph_def = tf.GraphDef()
        # Parse the definition
        graph_def.ParseFromString(f.read())
        # Flag if a single file is being put through the network
        if png:
            png_data = tf.placeholder(tf.string, shape=[])
            decoded_png = tf.image.decode_image(png_data, channels=3)
            # Actual importation of the graph definition with remappings
            _ = tf.import_graph_def(graph_def, name='incept',input_map={'DecodeJpeg': decoded_png})
            return png_data
        else:
            # Actual importation of the graph definition without remappings from png
            _ = tf.import_graph_def(graph_def, name='incept')


def load_index():
    ''' Load the index of the model that was trained prior '''
    index,files,findex = [],{},0
    print "Using index path : {}".format(INDEX_PATH+"*.npy")
    logging.info("Using index path : {}".format(INDEX_PATH+"*.npy"))
    for fname in glob.glob(INDEX_PATH+"*.npy"):
        logging.info("Starting {}".format(fname))
        try:
            t = np.load(fname)
            if max(t.shape) > 0:
                index.append(t)
            else:
                raise ValueError
        except:
            logging.error("Could not load {}".format(fname))
            pass
        else:
            for i,f in enumerate(file(fname.replace(".feats_pool3.npy",".files")).readlines()):
                files[findex] = f.strip()
                ENGINE.store_vector(index[-1][i,:],"{}".format(findex))
                findex += 1
            logging.info("Loaded {}".format(fname))
    index = np.concatenate(index)
    return index,files


def nearest(query_vector, index, files, n=20):
    ''' Nearest neighbour with more through computation for better accuracy '''
    query_vector= query_vector[np.newaxis, :]
    temp = []
    dist = []
    logging.info("started query")
    for k in xrange(index.shape[0]):
        temp.append(index[k])
        if (k+1) % 50000 == 0:
            temp = np.transpose(np.dstack(temp)[0])
            dist.append(spatial.distance.cdist(query_vector, temp))
            temp = []
    if temp:
        temp = np.transpose(np.dstack(temp)[0])
        dist.append(spatial.distance.cdist(query_vector, temp))
    dist = np.hstack(dist)
    ranked = np.squeeze(dist.argsort())
    logging.info("query finished")
    return [files[k] for i,k in enumerate(ranked[:n])]


def nearest_fast(query_vector, index, files, n=20):
    ''' Nearest neighbour with better performance at the cost of accuracy '''
    return [files[int(k)] for v,k,d in ENGINE.neighbours(query_vector)[:n]]


def store_index(features,files,count,index_dir):
    ''' Store index once features have been extracted '''
    feat_fname = "{}/{}.feats_pool3.npy".format(index_dir,count)
    files_fname = "{}/{}.files".format(index_dir,count)
    logging.info("storing in {}".format(index_dir))
    with open(feat_fname,'w') as feats:
        np.save(feats,np.array(features))
    with open(files_fname,'w') as filelist:
        filelist.write("\n".join(files))

def extract_features(image_data,sess):
    ''' Extract the features from the image data for the inception model '''
    pool3 = sess.graph.get_tensor_by_name('incept/pool_3:0')
    features = []
    files = []
    for fname,data in image_data.iteritems():
        try:
            pool3_features = sess.run(pool3,{'incept/DecodeJpeg/contents:0': data})
            features.append(np.squeeze(pool3_features))
            files.append(fname)
        except:
            logging.error("error while processing fname {}".format(fname))
    return features,files
