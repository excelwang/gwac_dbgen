import os, sys, socket
from datetime import datetime
sys.path.append('/home/wamdm/wm/gwac/gwac_dbgen')
sys.path.append('/home/wamdm/wm/gwac/gwac_pipeline')

from simulator_pipeline import pipeline, stargenparams, machine_tableno 
#import simulator_pipeline

os.system("sudo sysctl -w vm.swappiness=70")

#2400 is the number of each day's catalogs of one CCD.
n=2400
for i in range(1, n, n-1):
    #n1=i
    #n2=i+2399
    cmbrate = 200 #2400/200=12 and 34M*200=6.6G ,*15proc=100G, plus copy-on-write = 200G, can fit in total mem 256G.
    ratiosize = {200:'270M'}
    startno=i
    endno=i+(n-1)
    stargenparams['n1cata']=startno
    stargenparams['n2cata']=endno
    tblno=machine_tableno[socket.gethostname()]
    srcdir=stargenparams['destdir']
    cbddir="/home/wamdm/wm/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate])
    binarydir="/home/wamdm/wm/gwac/binarycatalogs-%din1/" %cmbrate
    prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno'])
    suffix=".cat"
    dbname='gwacdb'
    print "\nInitial parameters:\nstartno="+str(startno)+"\nendno="+str(endno)+"\ncmbrate="+str(cmbrate)+"\nhostname:"+socket.gethostname()+"\nccdno(tblno)="+str(tblno)+"\nsrcdir="+str(srcdir)+"\ncbddir="+str(cbddir)+"\nbinarydir="+str(binarydir)+"\nprefix="+prefix+"\nsuffix="+suffix+"\nratiosize[%d]=" %cmbrate +ratiosize[cmbrate] +"\ndbname="+dbname+"\n"
    #1.Generate simulated catalog files. Uncomment the next line if this step is finished.
    #edit the prefix of cbddir, binarydir according to your machine.
    os.chdir('/home/wamdm/wm/gwac/gwac_dbgen')
    pipeline(ifsimcat=True, ifcomb=False, ifconv=False, ifload=False, startno=startno, endno=endno, ratio=cmbrate, tblno=tblno, cbddir=cbddir, srcdir=srcdir, binarydir=binarydir, prefix=prefix, suffix=suffix, dbname=dbname)
    #2.Combine multiple catalogs into one so as to speed up db loading. Uncomment the next line if this step is finished.
#    pipeline(ifsimcat=False, ifcomb=True, ifconv=False, ifload=False, startno=startno, endno=endno, ratio=cmbrate, tblno=tblno, cbddir=cbddir, srcdir=srcdir, binarydir=binarydir, prefix=prefix, suffix=suffix, dbname=dbname)
    #startTime = datetime.now()
    #3. Convert the combined files from CSV format to binary. Uncomment the next line if this step is finished.
    #pipeline(ifsimcat=False, ifcomb=False, ifconv=True, ifload=False, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/home/wamdm/wm/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/home/wamdm/wm/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #pipeline(ifsimcat=False, ifcomb=False, ifconv=True, ifload=False, startno=startno, endno=endno, ratio=cmbrate, tblno=tblno, cbddir=cbddir, srcdir=srcdir, binarydir=binarydir, prefix=prefix, suffix=suffix, dbname=dbname)
    #4. Load the binary files into MonetDB.
    #pipeline(ifsimcat=False, ifcomb=False, ifconv=False, ifload=True, startno=int(stargenparams['n1cata']), endno=int(stargenparams['n2cata']), ratio=cmbrate, tblno=machine_tableno[socket.gethostname()], cbddir="/data/gwac/combinedcsv-%din1-%s/" %(cmbrate, ratiosize[cmbrate]), srcdir=stargenparams['destdir'], binarydir="/data/gwac/binarycatalogs-%din1/" %cmbrate, prefix="RA%03d_DEC%d_sqd%d-ccd%s-" %(stargenparams['rac'], stargenparams['decc'], stargenparams['sqd'],stargenparams['ccdno']), suffix=".cat", dbname='gwacdb')
    #print datetime.now() - startTime
    #os.chdir('/data/gwac/gwac_pipeline/')
    #cmd="./5_gwac_uniquecatalog.sh %d %d" %(n1,n2)
    #os.system(cmd)

os.system("sudo sysctl -w vm.swappiness=0")
