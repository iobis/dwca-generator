from generator import ArchiveGenerator
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("db.conf")
password = config.get("db", "password")

ids = [480,2893,2287,56,208,86,2408,482,582,2342,568,583,2316,1522,571,479,2420,151,2931,569,481,572,91,1516,585,2285,2411,2315,2407,584,2932,1525,1517,207,1520,2410,2286,2288,105,1514,2314,1455,90]

for id in ids:
    ArchiveGenerator(dataset_id=id, db_password=password, eml_path="./eml/OBIS_no-node_IMIS2EML_2017-12-19/").generate()