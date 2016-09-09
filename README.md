# gwac_dbgen
Tools to generate GWAC simulation data, combine, convert to binary, load into MonetDB.

Configuration
create directory: gwac, gwac/gwac_dbgen, gwac/gwac_pipeline
pipeline.py
   add the absolute path of above dirctories to your python path: eg, 
   sys.path.append('/data/gwac/gwac_dbgen')
   sys.path.append('/data/gwac/gwac_pipeline')
   
1. generate simulated catalogs for one night (2400 catalogs).
