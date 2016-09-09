import os, sys
from datetime import datetime
sys.path.append('/data/gwac/gwac_dbgen')
sys.path.append('/data/gwac/gwac_pipeline')

from simulator_pipeline import *

os.system("sudo sysctl -w vm.swappiness=70")

for i in range(1, 24, 23):
    n1=i
    n2=i+23
    stargenparams['n1cata']=n1
    stargenparams['n2cata']=n2
    os.chdir('/data/gwac/gwac_dbgen')
    pipeline(ifsimcat=True, ifcomb=False, ifconv=False, ifload=False, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #pipeline(ifsimcat=False, ifcomb=False, ifconv=True, ifload=False, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #startTime = datetime.now()
    #pipeline(ifsimcat=False, ifcomb=False, ifconv=False, ifload=True, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #print datetime.now() - startTime
    #os.chdir('/data/gwac/gwac_pipeline/')
    #cmd="./5_gwac_uniquecatalog.sh %d %d" %(n1,n2)
    #os.system(cmd)

os.system("sudo sysctl -w vm.swappiness=0")
