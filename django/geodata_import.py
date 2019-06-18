import os
import shutil
import tarfile
import sys

import geodata_config

try:
    # Python 2.7
    from urllib2 import urlopen
except ImportError:
    # Python 3.x
    from urllib.request import urlopen


def fetch_geodata():
    print("-- Fetching pre-selected country files from Mapzen...")
    # Use pre-selected countries.

    file_list = geodata_config.SELECTED_FILE_LIST if len(
        sys.argv) > 1 and sys.argv[1] == 'prod' else geodata_config.SELECTED_FILE_LIST_DEV

    # Recreating temporary folder for the files.
    try:
        os.mkdir(geodata_config.GEOJSON_TEMP_DIR)
    except OSError:
        shutil.rmtree(geodata_config.GEOJSON_TEMP_DIR)
        os.mkdir(geodata_config.GEOJSON_TEMP_DIR)

    # Getting the files one by one and saving to the temp folder.
    for filename in file_list:
        response = urlopen(geodata_config.MAPZEN_S3_URL + filename)

        with open(geodata_config.GEOJSON_TEMP_DIR + filename, "wb") as f:
            f.write(response.read())
        print(filename + " saved.")

        # Extracting tar files to folders.
        tfile = tarfile.open(geodata_config.GEOJSON_TEMP_DIR + filename, "r:gz")
        tfile.extractall(geodata_config.GEOJSON_TEMP_DIR)

        os.remove(geodata_config.GEOJSON_TEMP_DIR + filename)

    print("-- Fetching is done!")


def topojson():
    print("-- Transforming geodata files with Topojson...")
    for folder in os.listdir(geodata_config.GEOJSON_TEMP_DIR):
        print("==== " + folder)
        os.chdir(os.path.join(geodata_config.GEOJSON_TEMP_DIR, folder))
        for filename in geodata_config.ADMIN_LEVELS_TO_IMPORT:
            print("-- " + filename)
            os.system("geo2topo -p -o {} {}".format("topojson_" + filename, filename))
        print("{} transformed.".format(filename))

    print("-- Transforming is done!")


def import_geodata():
    os.system("docker exec -it whomaps_django_1 python manage.py import_geodata")


fetch_geodata()
topojson()
import_geodata()
