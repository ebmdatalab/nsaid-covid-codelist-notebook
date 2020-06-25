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

# The following notebook identifies [NHS dm+d codes](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) for oral ibuprofen at a AMP and VMP level. Current prescribing patterns
# - [ibuprofen prescribing volume](https://openprescribing.net/chemical/1001010J0/) on OpenPrescribing
# - [ibuprofen LYSINE prescribing volume](https://openprescribing.net/chemical/1001010AD/) on OpenPrescribing
# - [ibuprofen  SODIUM prescribing volume](https://openprescribing.net/chemical/1001010AP/) on OpenPrescribing

#import libraries
from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''
WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '1001010J0%'  OR #ibuprofen
  bnf_code LIKE '1001010AD%'  OR #ibuprofen lysine
  bnf_code LIKE '1001010AP%'     #ibuprofen sodium
  
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

oral_ibuprofen_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','oral_ibuprofen_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
oral_ibuprofen_codelist
# -


