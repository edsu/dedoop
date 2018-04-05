#!/usr/bin/env python3

import os
import shutil
import hashlib
import logging
import optparse


def main():
    prog = optparse.OptionParser('deduper input_dir output_dir')
    prog.add_option('-c', '--csv',
                    help='where to write the csv file')
    prog.add_option('-e', '--ext', 
                   help='comma separated list of file extensions to process')
    prog.add_option('-l', '--log')
    prog.add_option('-v', '--verbose', action='store_true')

    (opts, args) = prog.parse_args()

    if len(args) != 2:
        op.error('you must supply input and output directories')
   
    level = logging.INFO if opts.verbose else logging.WARN
    if opts.log:
        logging.basicConfig(opts.log, level=level)
    else:
        logging.basicConfig(level=level)

    input_dir, output_dir = args

    db = DedupeDB()
    db.read(input_dir)
    db.write(output_dir)

class DedupeDB():

    def __init__(self):
        self.db = {}

    def add(self, path):
        digest = get_digest(path)
        if digest in self.db:
            logging.warn('found duplicate %s', path)
            self.db[digest].append(path)
        else:
            self.db[digest] = [path]

    def entries(self):
        for digest, paths in self.db:
            yield digest, paths

    def read(self, in_dir):
        for dirpath, dirnames, filenames in os.walk(in_dir):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                self.add(path)

    def write(self, out_dir, csv_path=None):

        if csv_path is None:
            csv_path = os.path.join(out_dir, 'data.csv')

        if not os.path.isdir(out_dir):
            logging.info('creating output directory %s', out_dir)
            os.makedirs(out_dir)

        id = 0
        num_digits = len(str(len(self.db.keys())))
        path_format = r'%0' + str(num_digits) + 'i%s'

        for digest, paths in self.db.items():
            id += 1
            src = paths[0]
            filename, ext = os.path.splitext(src)
            dst = os.path.join(out_dir, path_format % (id, ext))
            shutil.copyfile(src, dst)
            logging.info('copied %s to %s', src, dst)

def get_digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        buff = None
        while buff != b'':
            buff = fh.read(1024)
            h.update(buff)
    digest = h.hexdigest()
    logging.info('digest %s %s', path, digest)
    return digest

if __name__ == "__main__":
    main()
