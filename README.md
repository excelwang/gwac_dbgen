# gwac_dbgen
Tools to generate GWAC simulation data, combine, convert to binary, load into MonetDB.

Configuration
create directory: gwac, gwac/gwac_dbgen, gwac/gwac_pipeline
pipeline.py
   add the absolute path of above dirctories to your python path: eg, 
      sys.path.append('/data/gwac/gwac_dbgen')
   sys.path.append('/data/gwac/gwac_pipeline')
   
1. Generate simulated catalogs for one night (2400 catalogs/day).
   you can change this number in the for loop of pipeline.py
   pipeline.py will call functions from simulator_pipeline.py to do the real genaration work.
   it will create the directory containing simulated catalogs under the top gwac directory: catalog.csv.

2. Combine multiple catalog file into large ones to speed up database loading process.
   configure the combination rate parameter: cmbrate.
   pipeline.py will call functions from combineCata.py.py to do the real genaration work.
   the combined large files are also created in a cbddir directory under the top level: like combinedcsv-200in1-270M.
   a log file will also be created in gwac_dbgen dir, nameed like logcomb-20160909151931-200in1.

3. Convert the combined files from CSV format to binary column files, which will be even faster when loading into database by the bulk loading technology of MonetDB, using multiporcessing.
   compile csv2bin.c: 
      gcc array.c -c
      gcc csv2bin.c -c
      gcc array.o csv2bin.o -o csv2bin
   pipeline.py will call functions from multicsv2bin.py to do the real conversion work.
   the binary files are created in a binarydir directory under the top level: like binarycatalogs-200in1, files like RA240_DEC10_sqd225-ccd16-0001.cat-1,..., RA240_DEC10_sqd225-ccd16-0001.cat-22.

4. Load the binary column files into MonetDB.
   It needs to first install MonetDB from tarball:
   wget https://www.monetdb.org/downloads/sources/Jun2016-SP1/MonetDB-11.23.7.tar.bz2
   tar xjvf MonetDB-11.23.7.tar.bz2
   ./bootstrap
   ./configure --prefix=/data/monetdbJul2016 --enable-optimize && make -j8 && make install

   create ~/.monetdb file on the node:
   cat ~/.monetdb
      user=monetdb
      password=monetdb
      save_history=true
      width=42
      language=sql
   add monetdb to PATH: vi ~/.bashrc
      PATH=$PATH:/data/monetdbJul2016/bin
   and create a dbfarm and db named 'gwacdb':
      monetdbd create dbfarm
      monetdbd start dbfarm
      monetdb create gwacdb
      monetdb start gwacdb
