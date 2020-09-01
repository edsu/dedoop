import os
import csv
import json
import pytest
import dedoop
import dotenv
import shutil
import logging
import libcloud


dotenv.load_dotenv()
logging.basicConfig(filename='test.log', level=logging.DEBUG)

input_dir = 'test-data'
output_dir = 'test-data-deduped'

def setup():
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

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
    assert len(files) == 3
    assert files[0] == '1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341.png'
    assert files[1] == '45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4.jpg'
    assert files[2] == 'b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953.jpg'

def test_extensions():
    m = dedoop.Deduper()
    m.read(input_dir, extensions=['jpg'])
    assert len(list(m.items())) == 2 

def test_dotfiles():
    m = dedoop.Deduper()
    m.read(input_dir, dotfiles=True)
    assert len(list(m.items())) == 4 


def test_json():
    m = dedoop.Deduper()
    m.read(input_dir)
    m.write(output_dir)
    data = m.json()

    assert len(data['items']) == 3

    assert data['items'][0]['path'] == '1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341.png'
    assert data['items'][0]['sha256'] == '1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341'
    assert data['items'][0]['original_paths'] == ['test-data/a.png']

    assert data['items'][1]['path'] == '45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4.jpg'
    assert data['items'][1]['sha256'] == '45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4'
    assert data['items'][1]['original_paths'] == ['test-data/b.jpg', 'test-data/c/b.jpg']

def test_write_s3():
    user = os.environ.get('DEDOOP_USER')
    assert user

    access_key = os.environ.get('DEDOOP_S3_ACCESS_KEY')
    assert access_key

    access_secret = os.environ.get('DEDOOP_S3_ACCESS_SECRET')
    assert access_secret

    m = dedoop.Deduper(access_key, access_secret)

    container_name = 's3://{}-dedoop-test'.format(user)
    container = get_test_container(m, container_name)

    m.read(input_dir)
    m.write(container_name)

    o = container.get_object('1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341')
    assert o

    o = container.get_object('45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4')
    assert o

    o = container.get_object('b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953')
    assert o

def test_write_gs():
    user = os.environ.get('DEDOOP_USER')
    assert user

    access_key = os.environ.get('DEDOOP_GS_ACCESS_KEY')
    assert access_key

    access_secret = os.environ.get('DEDOOP_GS_ACCESS_SECRET')
    assert access_secret

    m = dedoop.Deduper(access_key, access_secret)

    container_name = 'gs://{}-dedoop-test'.format(user)
    container = get_test_container(m, container_name)

    m.read(input_dir)
    m.write(container_name)

    o = container.get_object('1e89b90b5973baad2e6c3294ffe648ff53ab0b9d75188e9fbb8b38deb9ba3341')
    assert o

    o = container.get_object('45d257c93e59ec35187c6a34c8e62e72c3e9cfbb548984d6f6e8deb84bac41f4')
    assert o

    o = container.get_object('b6df8058fa818acfd91759edffa27e473f2308d5a6fca1e07a79189b95879953')
    assert o


def get_test_container(deduper, container_name):
    container = deduper.get_container(container_name)

    # if the test container isn't empty remove all its contents
    if len(container.list_objects()) != 0:
        storage = container.driver
        for o in container.list_objects():
            storage.delete_object(o)

    return container
