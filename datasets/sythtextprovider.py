## an initial version
## Transform the tfrecord to slim data provider format

import numpy 
import tensorflow as tf
import os
slim = tf.contrib.slim




ITEMS_TO_DESCRIPTIONS = {
    'image': 'slim.tfexample_decoder.Image',
    'shape': 'shape',
    'height': 'height',
    'width': 'width',
    'object/bbox': 'box',
    'object/label': 'label'
}
SPLITS_TO_SIZES = {
    'train': 858750,
}
NUM_CLASSES = 2



def get_datasets(data_dir,file_pattern = '*.tfrecord'):
    file_patterns = os.path.join(data_dir, file_pattern)
    print 'file_path: {}'.format(file_patterns)
    reader = tf.TFRecordReader
    keys_to_features = {
        'image/height': tf.FixedLenFeature([1], tf.int64),
        'image/width': tf.FixedLenFeature([1], tf.int64),
        'image/channels': tf.FixedLenFeature([1], tf.int64),
        'image/shape': tf.FixedLenFeature([3], tf.int64),
        'image/object/bbox/label': tf.VarLenFeature(dtype=tf.int64),
        'image/object/bbox/x0': tf.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/x1': tf.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/x2': tf.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/x3': tf.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/y0': tf.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/y1': tf.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/y2': tf.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/y3': tf.VarLenFeature(dtype=tf.float32),
        'image/format': tf.FixedLenFeature([], tf.string, default_value='jpeg'),
        'image/encoded': tf.FixedLenFeature([], tf.string, default_value=''),
        'image/name': tf.VarLenFeature(dtype = tf.string),
    }

    items_to_handlers = {
        'image': slim.tfexample_decoder.Image('image/encoded', 'image/format'),
        #'image': slim.tfexample_decoder.Tensor('image/encoded'),
        'shape': slim.tfexample_decoder.Tensor('image/shape'),
        'height': slim.tfexample_decoder.Tensor('image/height'),
        'width': slim.tfexample_decoder.Tensor('image/width'),
        'object/corx': slim.tfexample_decoder.BoundingBox(
                ['x0', 'x1', 'x2', 'x3'], 'image/object/bbox/'),
        'object/cory': slim.tfexample_decoder.BoundingBox(
                ['y0', 'y1', 'y2', 'y3'], 'image/object/bbox/'),
        'object/label': slim.tfexample_decoder.Tensor('image/object/bbox/label'),
        #'imaname': slim.tfexample_decoder.Tensor('image/name'),
        #'objext/txt': slim.tfexample_decoder.Tensor('image/object/bbox/label_text'),
      }

    decoder = slim.tfexample_decoder.TFExampleDecoder(
        keys_to_features, items_to_handlers)

    labels_to_names = None


    return slim.dataset.Dataset(
        data_sources=file_patterns,
        reader=reader,
        decoder=decoder,
        num_samples=SPLITS_TO_SIZES['train'],
        items_to_descriptions=ITEMS_TO_DESCRIPTIONS,
        num_classes=NUM_CLASSES,
        labels_to_names=labels_to_names)