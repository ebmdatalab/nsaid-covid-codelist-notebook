# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

The following notebook identifies NHS dm+d codes for indometacin at a AMP and VMP level. T
- [indometacin prescribing volume](https://openprescribing.net/chemical/1001010K0/) on OpenPrescribing


#import libraries
from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''
WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '1001010K0%'  #bnf indometacin
)

SELECT *
FROM measures.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes) 
AND 
obj_type IN ('vmp', 'amp')
AND
form_route LIKE '%.oral%' 
ORDER BY obj_type, bnf_code, snomed_id
'''

indomet_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','cox2_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
cox2_codelist
cox2_codelist
