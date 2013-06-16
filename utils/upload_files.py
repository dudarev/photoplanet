"""
Uploads files to Amazon S3 bucket.

Parameters for the bucket are in ``config.py``.
"""

import os
import datetime

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import config


# connection to bucket

conn = S3Connection(
    config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY)

bucket = conn.create_bucket(config.BUCKET_NAME)
bucket.set_acl('public-read')


# upload files

print datetime.datetime.now()

for root, dirs, files in os.walk('.'):
    relpath = os.path.relpath(root, '.')

    for f in files:
        if relpath == '.':
            keyname = f
        else:
            keyname = os.path.join(relpath, f)
        filename = os.path.join(root, f)

        # for now this is just for a single file
        # remove if to upload all
        if f == 'out.jpg':
            k = Key(bucket)
            k.key = keyname
            print 'uploading: {}'.format(keyname)
            k.set_contents_from_filename(filename, replace=False)
            k.set_acl('public-read')
