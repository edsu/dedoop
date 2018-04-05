import os
import csv
import json
import pytest
import dedoop
import logging
import shutil

logging.basicConfig(filename='test.log', level=logging.DEBUG)

input_dir = 'test-data'
output_dir = 'test-data-deduped'

def setup():
    if os.path.isdir(output_dir):
        pass # shutil.rmtree(output_dir)

def test_sha256():
    assert dedoop.get_sha256(os.path.join(input_dir, 'a.jpg')) == 'b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953'

def test_read():
    m = dedoop.Deduper()
    m.read(input_dir)
    assert len(list(m.items())) == 3

def test_write():
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    m = dedoop.Deduper()
    m.read(input_dir)
    m.write(output_dir)

    files = os.listdir(output_dir)
    files.sort()
    assert len(files) == 5
    assert files[0] == '1.png'
    assert files[1] == '2.jpg'
    assert files[2] == '3.jpg'
    assert files[3] == 'data.csv'
    assert files[4] == 'data.json'

def test_extensions():
    m = dedoop.Deduper()
    m.read(input_dir, extensions=['jpg'])
    assert len(list(m.items())) == 2 

def test_json():
    m = dedoop.Deduper()
    m.read(input_dir)
    m.write(output_dir)
    data = json.load(open(os.path.join(output_dir, 'data.json')))
    assert len(data['items']) == 3

    assert data['items'][0]['path'] == '1.png'
    assert data['items'][0]['sha256'] == '1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341'
    assert data['items'][0]['original_paths'] == ['test-data/a.png']

    assert data['items'][1]['path'] == '2.jpg'
    assert data['items'][1]['sha256'] == '45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4'
    assert data['items'][1]['original_paths'] == ['test-data/b.jpg', 'test-data/c/b.jpg']

def test_csv():
    reader = csv.DictReader(open(os.path.join(output_dir, 'data.csv')))

    row = next(reader)
    assert row['path'] == '1.png'
    assert row['sha256'] == '1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341'
    assert row['original_paths'] == 'test-data/a.png'

    row = next(reader)
    assert row['path'] == '2.jpg'
    assert row['sha256'] == '45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4'
    assert row['original_paths'] == '"test-data/b.jpg","test-data/c/b.jpg"'
