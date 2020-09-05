#!/usr/bin/env python3

import os
import re
import csv
import json
import click
import shutil
import hashlib
import logging
import optparse

from urllib.parse import urlparse
from libcloud.storage.types import Provider, ContainerDoesNotExistError
from libcloud.storage.providers import get_driver

STORAGE_PROVIDERS = {
    's3': Provider.S3,
    'gs': Provider.GOOGLE_STORAGE
}

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
def add(input_dir, output_dir):
    input_dir, output_dir = args
    db = Deduper()
    db.read(input_dir, extensions=opts.extensions, dotfiles=opts.dotfiles)
    db.write(output_dir)


class Deduper():

    def __init__(self, key=None, secret=None):
        self.db = {}
        self.key = key
        self.secret = secret

    def read(self, in_dir, extensions=[], dotfiles=False):
        self.db = {}
        extensions = [e.lower().strip('.') for e in extensions]
        for dirpath, dirnames, filenames in os.walk(in_dir):
            for filename in filenames:
                path = os.path.join(dirpath, filename)

                if filename.startswith('.') and not dotfiles:
                    logging.info('ignoring dot file: %s', path)
                    continue

                name, ext = os.path.splitext(path)
                if extensions and ext.lower().strip('.') not in extensions:
                    logging.info('ignoring %s', path)
                    continue

                self.add(path)

    def write(self, dest):
        uri = urlparse(dest)
        if uri.scheme in STORAGE_PROVIDERS.keys():
            self.write_cloud(dest)
        else:
            self.write_fs(dest)

    def write_fs(self, out_dir):
        if not os.path.isdir(out_dir):
            logging.info('creating output directory %s', out_dir)
            os.makedirs(out_dir)

        num_digits = len(str(len(self.db.keys())))

        for sha256, meta in self.items():
            src = meta['paths'][0]
            filename, ext = os.path.splitext(src)
            ext = ext.lower()
           
            # if it doesn't look like an extension don't use it
            if not re.match(r'^[.][a-z0-9]+$', ext):
                ext = ''

            dst = os.path.join(out_dir, sha256 + ext)
            shutil.copyfile(src, dst)
            meta['path'] = dst.replace(out_dir + os.sep, '')
            logging.info('copied %s to %s', src, dst)

    def write_cloud(self, container_uri):
        container = self.get_container(container_uri)
        storage = container.driver

        for sha256, meta in self.items():
            src = meta['paths'][0]
            object_name = sha256
            storage.upload_object(src, container, object_name)
            logging.info('copied %s to %s/%s', src, container, object_name)

    def add(self, path):
        sha256 = get_sha256(path)
        if sha256 in self.db:
            logging.warning('found duplicate %s', path)
            self.db[sha256]['paths'].append(path)
        else:
            self.db[sha256] = {'paths': [path], 'sha256': sha256}

    def items(self):
        keys = sorted(self.db.keys())
        for key in keys:
            yield key, self.db[key]

    def json(self):
        data = {'items': []}
        for sha256, meta in self.items():
            data['items'].append({
                'path': meta['path'],
                'sha256': meta['sha256'],
                'original_paths': meta['paths'],
            })
        return data

    def get_container(self, container_uri):
        uri = urlparse(container_uri)
        provider = STORAGE_PROVIDERS.get(uri.scheme)
        container_name = uri.netloc

        if provider == None:
            raise Exception('unknown storage provider {}'.format(container_name))
        else:
            storage = get_driver(provider)(self.key, self.secret)

        try:
            container = storage.get_container(container_name)
        except ContainerDoesNotExistError:
            container = storage.create_container(container_name)

        return container

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

cli = click.CommandCollection(sources=[add])

if __name__ == "__main__":
    cli()
