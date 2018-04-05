#!/usr/bin/env python3

import os
import re
import csv
import json
import shutil
import hashlib
import logging
import optparse

class Deduper():

    def __init__(self):
        self.db = {}

    def read(self, in_dir, extensions=[]):
        self.db = {}
        extensions = [e.lower().strip('.') for e in extensions]
        for dirpath, dirnames, filenames in os.walk(in_dir):
            for filename in filenames:
                path = os.path.join(dirpath, filename)

                if filename.startswith('.'):
                    logging.info('ignoring dot file', path)
                    continue

                name, ext = os.path.splitext(path)
                if extensions and ext.lower().strip('.') not in extensions:
                    logging.info('ignoring %s', path)
                    continue

                self.add(path)

    def write(self, out_dir):
        if not os.path.isdir(out_dir):
            logging.info('creating output directory %s', out_dir)
            os.makedirs(out_dir)

        id = 0
        num_digits = len(str(len(self.db.keys())))
        path_format = r'%0' + str(num_digits) + 'i'

        for sha256, meta in self.items():
            id += 1
            src = meta['paths'][0]
            filename, ext = os.path.splitext(src)
            ext = ext.lower()
           
            # if it doesn't look like an extension don't use it
            if not re.match('^\.[a-z0-9]+$', ext):
                ext = ''

            dst = os.path.join(out_dir, path_format % id + ext)
            shutil.copyfile(src, dst)
            meta['path'] = dst.replace(out_dir + os.sep, '')
            logging.info('copied %s to %s', src, dst)

        self.write_json(out_dir)
        self.write_csv(out_dir)

    def add(self, path):
        sha256 = get_sha256(path)
        if sha256 in self.db:
            logging.warn('found duplicate %s', path)
            self.db[sha256]['paths'].append(path)
        else:
            self.db[sha256] = {'paths': [path], 'sha256': sha256}

    def items(self):
        keys = sorted(self.db.keys())
        for key in keys:
            yield key, self.db[key]

    def write_json(self, out_dir):
        data = {'items': []}
        for sha256, meta in self.items():
            data['items'].append({
                'path': meta['path'],
                'sha256': meta['sha256'],
                'original_paths': meta['paths'],
            })
        json.dump(data, open(os.path.join(out_dir, 'data.json'), 'w'), indent=2)

    def write_csv(self, out_dir):
        fieldnames = ['path', 'original_paths', 'sha256']
        fh = open(os.path.join(out_dir, 'data.csv'), 'w')
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for sha256, meta in self.items():
            if len(meta['paths']) == 1:
                original_paths = meta['paths'][0]
            else:
                original_paths = ','.join(['"%s"' % p for p in meta['paths']])
            writer.writerow({
                'path': meta['path'],
                'sha256': meta['sha256'],
                'original_paths': original_paths
            })

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        buff = None
        while buff != b'':
            buff = fh.read(1024)
            h.update(buff)
    sha256 = h.hexdigest()
    logging.info('sha256 %s %s', path, sha256)
    return sha256

def split_option(option, opt_str, value, parser):
    parser.values.extensions = value.split(',')

def main():
    prog = optparse.OptionParser('dedoop input_dir output_dir')
    prog.add_option('-e', '--extensions', action='callback', type='string', 
                    default=[], callback=split_option,
                    help='comma separated list of file extensions to process')
    prog.add_option('-l', '--log')
    prog.add_option('-v', '--verbose', action='store_true')

    (opts, args) = prog.parse_args()

    if len(args) != 2:
        prog.error('you must supply input and output directories')

    level = logging.INFO if opts.verbose else logging.WARN
    if opts.log:
        logging.basicConfig(filename=opts.log, level=level)
    else:
        logging.basicConfig(level=level)

    input_dir, output_dir = args

    db = Deduper()
    db.read(input_dir, extensions=opts.extensions)
    db.write(output_dir)

if __name__ == "__main__":
    main()
