import os, sys
from datetime import datetime
sys.path.append('/data/gwac/gwac_dbgen')
sys.path.append('/data/gwac/gwac_pipeline')

from simulator_pipeline import *

os.system("sudo sysctl -w vm.swappiness=70")

#2400 is the number of each day's catalogs of one CCD.
for i in range(1, 2400, 2399):
    n1=i
    n2=i+2399
    stargenparams['n1cata']=n1
    stargenparams['n2cata']=n2
    os.chdir('/data/gwac/gwac_dbgen')
    #1.Generate simulated catalog files. Uncomment the next line if this step is finished.
    #edit the prefix of cbddir, binarydir according to your machine.
    #pipeline(ifsimcat=True, ifcomb=False, ifconv=False, ifload=False, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #2.Combine multiple catalogs into one so as to speed up db loading. Uncomment the next line if this step is finished.
    cmbrate = 200 #2400/200=12 and 34M*200=6.6G ,*15proc=100G, plus copy-on-write = 200G, can fit in total mem 256G.
    #pipeline(ifsimcat=False, ifcomb=True, ifconv=False, ifload=False, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #startTime = datetime.now()
    #3. Convert the combined files from CSV format to binary. Uncomment the next line if this step is finished.
    pipeline(ifsimcat=False, ifcomb=False, ifconv=True, ifload=False, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #4. Load the binary files into MonetDB.
    #pipeline(ifsimcat=False, ifcomb=False, ifconv=False, ifload=True, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #print datetime.now() - startTime
    #os.chdir('/data/gwac/gwac_pipeline/')
    #cmd="./5_gwac_uniquecatalog.sh %d %d" %(n1,n2)
    #os.system(cmd)

os.system("sudo sysctl -w vm.swappiness=0")
