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

# The following notebook generates [NHS Dictionary of Medicines and Devices](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) codes for oral NSAIDs. You can see [current NSAID prescribing patterns on OpenPrescribing](https://openprescribing.net/bnf/100101/)

#import libraries
from ebmdatalab import bq
import pandas as pd
import os

# +
sql = '''
WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '1001010%' #bnf section non-steroidal anti-inflammatory drugs

)

SELECT *
FROM measures.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes) 
AND 
obj_type IN ('vmp', 'amp')
AND
form_route LIKE '%.oral%' #include oral preparations only
ORDER BY obj_type, bnf_code, snomed_id'''

nsaid_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','nsaid_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
nsaid_codelist.rename(columns={'snomed_id':'id'}, inplace=True) ##rename to fit another notebook with code already written
nsaid_codelist
# -


