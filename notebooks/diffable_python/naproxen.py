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

# The following notebook identifies [NHS dm+d](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) codes for Naproxen at a AMP and VMP level. Naproxen is a very commonly prescribed NSAID in England ([see prescribing volume on OpenPrescribing](https://openprescribing.net/chemical/1001010P0/)). This is because Naproxen has been shwn to be one of the safer NSAIDs and on OpenPrescribing there is a [measure of Naproxen and Iburpfen usage compard to other NSAIDs](https://openprescribing.net/measure/ktt13_nsaids_ibuprofen/national/england/).
#
# - [All naproxen codes](#all)
# - [High dose naproxen](#hd)
# - [Low dose naproxen](#ld)

#import libraries
from ebmdatalab import bq
import os
import pandas as pd

# ## Total naproxen preparations <a id='all'></a>

# +
sql = '''
WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '1001010P0%' #bnf chemical naproxen

)

SELECT *
FROM measures.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes) 
AND 
obj_type IN ('vmp', 'amp')
AND
form_route LIKE '%.oral%' #gets rid of suppositories
AND
form_route NOT LIKE '%susp%' #this drops oral liquids ie suspensions
ORDER BY obj_type, bnf_code, snomed_id
'''


naproxen_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','naproxen_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
naproxen_codelist.rename(columns={'snomed_id':'id'}, inplace=True) ##rename to fit another notebook with code already written
naproxen_codelist


# +
## High dose naproxen <a id='hd'></a>
# -

naproxen_high_dose = naproxen_codelist[naproxen_codelist['bnf_name'].str.contains("500mg")]
naproxen_high_dose


# ## Low dose naproxen <a id='ld'></a>

naproxen_low_dose = naproxen_codelist[naproxen_codelist['bnf_name'].str.contains("250mg")]
naproxen_low_dose


