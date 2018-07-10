from generator import ArchiveGenerator
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("db.conf")
password = config.get("db", "password")

ids = [12,]

for id in ids:
    ArchiveGenerator(dataset_id=id, db_password=password, eml_path="./eml/OBIS_no-node_IMIS2EML_2017-12-19/").generate()