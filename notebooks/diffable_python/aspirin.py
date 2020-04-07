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

# The following notebook identifies SnoMed/[NHS Dictionary of Medicines and Devices](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) codes for low dose aspirin. First we will identify products in "antiplatet section" in BNF codes.

from ebmdatalab import bq
import pandas as pd
import os

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '0209000A0%' #bnf section antiplatelet - aspirin
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

aspirin_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','aspirin_codelist.csv'))
pd.set_option('display.max_rows', None)
aspirin_codelist
# -

# There are certain low dose liquids that we cannot be certain people are using for antiplatelet effect but propose exclude 

# ## Aspirin in Analgesia Section

# There is a seperate section for [Aspirin when used for analgesia](https://openprescribing.net/analyse/#org=CCG&numIds=0407010B0&denomIds=4.7.1&selectedTab=summary) with approximately 65k prescritpions per year. Let's investigate this.

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '0407010B0%' #bnf section antiplatelet - aspirin
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

aspirin_analgesia_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','aspirin_analgesia_codelist.csv'))
pd.set_option('display.max_rows', None)
aspirin_analgesia_codelist
# -

# These look suspiciously like products use to treat atrial fibrillation which was a previously recommended but not a current recommendation. Lets investigate.

# +
## here we extract data for modelling
sql = '''
SELECT
  quantity_per_item,
  sum(items) as items
FROM
 ebmdatalab.hscic.raw_prescribing_normalised AS presc
INNER JOIN
  ebmdatalab.hscic.practices AS prac
ON
  presc.practice = prac.code
WHERE
bnf_code LIKE "0407010B0%" 
AND
(bnf_name LIKE '%tablet%' OR
bnf_name LIKE '% tab %' OR
bnf_name LIKE '% tab' OR
bnf_name LIKE '% tabs %' OR
bnf_name LIKE '% tabs' OR
bnf_name LIKE '%capsule%' OR
bnf_name LIKE '% caps %' OR
bnf_name LIKE '% caps' OR
bnf_name LIKE '%caplet%' OR
bnf_name LIKE '%Chewtab%') ##this restricts to tablets or capsules
AND
setting = 4
AND (month BETWEEN '2019-01-01'
    AND '2019-12-01') ##this restricts to one year 2019 
GROUP BY
  quantity_per_item
ORDER BY
quantity_per_item
    '''

df_asp_qty = bq.cached_read(sql, csv_path=os.path.join('..','data','df_asp_qty.csv'))

# -

import plotly.express as px
fig = px.bar(df_asp_qty, x='quantity_per_item', y='items')
fig.show()


# A quantity of 28 is most frequently prescribed with 7 and 56 also above 5k items. Propose we exclude as suggestive of once daily prescribing which is suggestive of [prevention of CVD complications (BNF link)](https://bnf.nice.org.uk/drug/aspirin.html)
