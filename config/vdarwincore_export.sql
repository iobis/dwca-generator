drop view if exists obis.vdarwincore_export;

CREATE OR REPLACE VIEW obis.vdarwincore_export AS 
    SELECT
        dxs.resource_id AS "OBIS_Resource_Id",
        s.sname AS "scientificName",
        s.sauthor AS "scientificNameAuthorship",
        dxs.sex,
        dxs.lifestage AS "lifeStage",
        CASE
            WHEN t.worms_id is not null THEN 'urn:lsid:marinespecies.org:taxname:' || t.worms_id
            ELSE null
        END as "scientificNameID",
        dxs.longitude AS "decimalLongitude",
        dxs.latitude AS "decimalLatitude",
        dxs.coordinateprecision AS "coordinatePrecision",
        dxs.ocean AS "waterBody",
        dxs.country,
        dxs.state AS "stateProvince",
        dxs.county,
        dxs.locality,
        dxs.minimumdepth AS "minimumDepthInMeters",
        dxs.maximumdepth AS "maximumDepthInMeters",
        dxs.depthrange AS "verbatimDepth",
        dxs.institutioncode AS "institutionCode",
        dxs.collectioncode AS "collectionCode",
        dxs.catalognumber AS "catalogNumber",
        dxs.previouscatalognumber AS "otherCatalogNumbers",
        dxs.identifiedby AS "identifiedBy", 
        CASE
            WHEN dxs.yearidentified IS NOT NULL AND dxs.monthidentified IS NOT NULL AND dxs.dayidentified IS NOT NULL THEN (((dxs.yearidentified::text || '-'::text) || lpad(dxs.monthidentified::text, 2, '0'::text)) || '-'::text) || lpad(dxs.dayidentified::text, 2, '0'::text)
            ELSE NULL::text
        END::character varying(10) AS "dateIdentified",
        dxs.typestatus AS "typeStatus",
        dxs.collectornumber AS "recordNumber",
        dxs.fieldnumber AS "fieldNumber",
        dxs.collector AS "recordedBy",
        dxs.datelastmodified AS modified,
        dxs.sourceofrecord AS "associatedReferences",
        dxs.citation AS "bibliographicCitation",
        dxs.recordurl AS "references",
        dxs.basisofrecord AS "basisOfRecord",
        dxs.preparationtype AS preparations,
        dxs.notes AS "occurrenceRemarks",
        dxs.yearcollected AS year,
        dxs.monthcollected AS month,
        dxs.daycollected AS day, ((
        CASE
            WHEN dxs.observedweight IS NULL THEN ''::text
            ELSE ('observedweight='::text || dxs.observedweight) || ';'::text
        END || 
        CASE
            WHEN dxs.samplesize IS NULL THEN ''::text
            ELSE ('samplesize='::text || dxs.samplesize::text) || ';'::text
        END) || 
        CASE
            WHEN dxs.temperature IS NULL THEN ''::text
            ELSE ('temperature='::text || dxs.temperature) || ';'::text
        END) || 
        CASE
            WHEN dxs.observedindividualcount IS NULL THEN ''::text
            ELSE ('observedindividualcount='::text || dxs.observedindividualcount) || ';'::text
        END AS "dynamicProperties",
        dxs.relationshiptype AS "RelationshipType",
        dxs.relatedcatalogitem AS "RelatedCatalogItem",
        dxs.individualcount,
        to_char(drs.datecollected, 'YYYY-MM-DD"T"HH24:MI:SS"Z"'::text) AS "eventDate",
        'present'::text as "occurrenceStatus"
   FROM obis.dxs
   join obis.drs on dxs.dr_id = drs.id
   JOIN obis.snames s ON dxs.sname_id = s.id
   JOIN obis.tnames t ON t.id = s.tname_id;

ALTER TABLE obis.vdarwincore_export
  OWNER TO postgres;
GRANT ALL ON TABLE obis.vdarwincore_export TO postgres;
GRANT SELECT ON TABLE obis.vdarwincore_export TO obisreaders;