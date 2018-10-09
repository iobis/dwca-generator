# dwca-generator

Generation of Darwin Core Archives from OBIS data

## How to
### Install

Install Python 2.7 and the following dependencies:

- psycopg2-binary

Create `db.conf` with the following content (replace `*****` with actual password):

```
[db]
password=*****
```

### Run

Enter the appropriate dataset IDs in `script.py` and run:

```python
python script.py
```

The output should look like this:

```
INFO:root:Processing dataset: SOC
INFO:root:Reading EML from ./eml/obis_no-node_imis2eml_2017-12-19/soc/eml.xml
INFO:root:Fetched 92851 records from the OBIS database
INFO:root:Creating output directory ../dwca-generator/output
INFO:root:Writing metadata
INFO:root:Writing data
INFO:root:Creating ZIP file: ./output/soc.zip
INFO:root:Processing dataset: INVEMAR_OBIS
INFO:root:Reading EML from ./eml/obis_no-node_imis2eml_2017-12-19/invemar_obis/eml.xml
INFO:root:Fetched 34733 records from the OBIS database
INFO:root:Writing metadata
INFO:root:Writing data
INFO:root:Creating ZIP file: ./output/invemar_obis.zip
```