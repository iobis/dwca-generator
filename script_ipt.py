from lib import ArchiveGenerator
import ConfigParser
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

config = ConfigParser.RawConfigParser()
config.read("config/db.conf")
password = config.get("db", "password")

ids = [12, 1502]

for id in ids:
    archive = ArchiveGenerator(dataset_id=id, db_password=password, eml_path="./eml/OBIS_no-node_IMIS2EML_2017-12-19")
    directory = "./ipt-docker/data/resources/" + archive.dataset_name.lower()

    # dwca

    filename = "dwca-1.0.zip"
    archive.generate(directory, filename=filename)

    # eml

    archive.save_eml(directory + "/eml-1.0.xml")
    archive.save_eml(directory + "/eml.xml")

    # xml

    archive.save_resource_xml(directory + "/resource.xml")
