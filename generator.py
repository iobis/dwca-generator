import psycopg2
import csv
import zipfile
from collections import OrderedDict
from StringIO import StringIO
import ConfigParser
import os

class ArchiveGenerator:

	def __init__(self, dataset_id, db_password, eml_path="./eml", output_path="./output", mapping_path="./mapping.csv", db_host="obisdb-stage.vliz.be", db_user="obisreader", db_name="obis"):
		self.dataset_id = dataset_id
		self.eml_path = eml_path
		self.output_path = output_path
		self.mapping_path = mapping_path
		self.db_host = db_host
		self.db_user = db_user
		self.db_password = db_password
		self.db_name = db_name

		self.connect_db()
		self.fetch_name()
		self.fetch_eml()
		self.fetch_mapping()
		self.fetch_data()

	def connect_db(self):
		self.conn = psycopg2.connect("host='%s' user='%s' password='%s' dbname='%s'" % (self.db_host, self.db_user, self.db_password, self.db_name))

	def fetch_name(self):
		cur = self.conn.cursor()
		cur.execute("select digirname from obis.resources where id = %s" % (self.dataset_id))
		res = cur.fetchone()
		if res is None:
			raise Exception("Dataset name not found")
		self.dataset_name = res[0]
		print "Dataset name: %s" % (self.dataset_name)

	def fetch_eml(self):
		path = ("%s/%s/eml.xml" % (self.eml_path, self.dataset_name)).lower()
		print "Reading %s" % (path)
		with open(path, "r") as eml_file:
			self.eml = eml_file.read()

	def fetch_mapping(self):
		with open(self.mapping_path, "rb") as csvfile:
			r = csv.reader(csvfile, delimiter=";")
			self.mapping = OrderedDict((rows[0], rows[1]) for rows in r)
			self.fields = OrderedDict((k, v) for k, v in self.mapping.items() if len(v) > 0)
			self.bor_index = self.fields.keys().index("basisOfRecord")

	def fetch_data(self):
		fields = ", ".join(("\"" + f + "\"" for f in self.fields.keys()))
		cur = self.conn.cursor()
		cur.execute("select %s from obis.vdarwincore where \"OBIS_Resource_Id\" = %s" % (fields, self.dataset_id))
		res = cur.fetchall()
		if res is None:
			raise Exception("No data found")
		self.data = res
		print "Fetched %s records" % (len(self.data))

	def write_meta(self):
		out = StringIO()
		out.write("<archive xmlns=\"http://rs.tdwg.org/dwc/text/\" metadata=\"eml.xml\">\n")
		out.write("  <core encoding=\"UTF-8\" fieldsTerminatedBy=\"\\t\" linesTerminatedBy=\"\\n\" fieldsEnclosedBy=\"\" ignoreHeaderLines=\"1\" rowType=\"http://rs.tdwg.org/dwc/terms/Occurrence\">\n")
		out.write("    <files>\n")
		out.write("      <location>occurrence.txt</location>\n")
		out.write("    </files>\n")
		out.write("    <id index=\"0\" />\n")
		for i in range(len(self.fields)):
			out.write("    <field index=\"%s\" term=\"%s\"/>\n" % (i + 1, self.fields.items()[i][1]))
		out.write("  </core>\n")
		out.write("</archive>")
		return out.getvalue()

	def process_value(self, value):
		if value is None:
			return ""
		elif isinstance(value, basestring):
			return value.replace("\t", " ")
		else:
			return str(value)

	def write_data(self):
		out = StringIO()
		out.write("id\t" + "\t".join(self.fields.keys()) + "\n")
		for r in range(len(self.data)):
			row = list(self.data[r])

			basis_of_record = row[self.bor_index]
			if basis_of_record == "L":
				row[self.bor_index] = "LivingSpecimen"
			elif basis_of_record == "S":
				row[self.bor_index] = "PreservedSpecimen"
			else:
				row[self.bor_index] = "HumanObservation"

			line = str(r + 1) + "\t" + "\t".join((self.process_value(value) for value in row))
			out.write(line + "\n")
		return out.getvalue()

	def generate(self):
		if not os.path.exists(self.output_path):
			print "Creating output directory %s" % (os.path.abspath(self.output_path))
			os.makedirs(self.output_path)
		mf = StringIO()
		with zipfile.ZipFile(mf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
			zf.writestr("%s/meta.xml" % (self.dataset_name.lower()), self.write_meta())
			zf.writestr("%s/eml.xml" % (self.dataset_name.lower()), self.eml)
			zf.writestr("%s/occurrence.txt" % (self.dataset_name.lower()), self.write_data())
		with open("%s/%s.zip" % (self.output_path, self.dataset_name.lower()), "wb") as f:
			f.write(mf.getvalue())

config = ConfigParser.RawConfigParser()
config.read("db.conf")

with open("arcod.csv", "rb") as csvfile:
	res = csv.reader(csvfile, delimiter=",")
	res.next()
	for row in res:
		ArchiveGenerator(row[0], config.get("db", "password")).generate()
