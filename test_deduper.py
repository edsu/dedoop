import os
import pytest
import deduper
import logging
import shutil

logging.basicConfig(filename='test.log', level=logging.DEBUG)

input_dir = 'test-data'
output_dir = 'test-data-deduped'

def setup():
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

def test_hash():
    assert deduper.get_digest(os.path.join(input_dir, 'a.jpg')) == 'b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953'

def test_read():
    m = deduper.Deduper()
    m.read(input_dir)
    assert len(list(m.items())) == 3

def test_write():
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    m = deduper.Deduper()
    m.read(input_dir)
    m.write(output_dir)

    files = os.listdir(output_dir)
    files.sort()
    assert len(files) == 3
    assert files[0] == '1.png'
    assert files[1] == '2.jpg'
    assert files[2] == '3.jpg'


def test_extensions():
    m = deduper.Deduper()
    m.read(input_dir, extensions=['jpg'])
    assert len(list(m.items())) == 2 

def test_json():
    m = deduper.Deduper()

def test_csv():
    pass


