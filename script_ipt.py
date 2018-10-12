from lib import ArchiveGenerator
import ConfigParser
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
import psycopg2

config = ConfigParser.RawConfigParser()
config.read("config/db.conf")
password = config.get("db", "password")

def fetch_ids():
    conn = psycopg2.connect("host='%s' user='%s' password='%s' dbname='%s'" % ("obisdb-stage.vliz.be", "obisreader", password, "obis"))
    cur = conn.cursor()
    q = "select id from obis.resources where not digirurl ilike '%resource?r=%'"
    cur.execute(q)
    ids = cur.fetchall()
    return [item for sublist in ids for item in sublist]

ids = fetch_ids()

for i, id in enumerate(ids):
    logging.info(i)

    try:
        archive = ArchiveGenerator(dataset_id=id, db_password=password, eml_path="./eml/imis_20181010")
        directory = "./ipt-docker/data/resources/" + archive.dataset_name.lower()

        # dwca

        filename = "dwca-1.0.zip"
        archive.generate(directory, filename=filename)

        # eml

        archive.save_eml(directory + "/eml-1.0.xml")
        archive.save_eml(directory + "/eml.xml")

        # xml

        archive.save_resource_xml(directory + "/resource.xml")

    except Exception as e:
        logging.error("Error generating dataset directory for dataset %s" % (id))
        logging.error(e)