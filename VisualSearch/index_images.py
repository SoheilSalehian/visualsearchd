import logging, os
import inception
from configs import IMAGES_PATH

def index():
    """
    Index images
    """
    logging.info("Starting with images present in {} storing index in {}".format(IMAGES_PATH,INDEX_PATH))
    try:
        os.mkdir(INDEX_PATH)
    except:
        print "Could not created {}, if its on /mnt/ have you set correct permissions?".format(INDEX_PATH)
        raise ValueError
    inception.load_network()
    count = 0
    start = time.time()
    with inception.tf.Session() as sess:
        for image_data in inception.get_batch(IMAGES_PATH):
            logging.info("Batch with {} images loaded in {} seconds".format(len(image_data),time.time()-start))
            start = time.time()
            count += 1
            features,files = inception.extract_features(image_data,sess)
            logging.info("Batch with {} images processed in {} seconds".format(len(features),time.time()-start))
            start = time.time()
            inception.store_index(features,files,count,INDEX_PATH)
