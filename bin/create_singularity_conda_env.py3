#!/usr/bin/python3

import re
import os, sys, stat
from datetime import datetime
import getopt  



def write_singularity_file(dirname, app, ver, ts):
  f = open("%s/Singularity" % dirname,"w+")
  f.write(singularity_template.format( APP = app,VER = ver, TS = ts))
  f.close()


if __name__ == '__main__':

  args=sys.argv[1:]

  app = ''
  version = ''
  loc = '.'
  micromamba = False
 
  try:
     opts, args = getopt.getopt(args,"hua:v:l:",["app=","version=","location="])
  except getopt.GetoptError:
     print ('test.py -l <location> -a <app> -v <version>')
     sys.exit(2)
 
  for opt, arg in opts:
     if opt == '-h':
        print ('args.py -a <app> -v <version>')
        sys.exit()
     elif opt == '-u':
        micromamba = True
     elif opt in ("-a", "--app"):
        app = arg
     elif opt in ("-l", "--location"):
        loc = arg
     elif opt in ("-v", "--version"):
        version = arg
 
  print ('Application is ', app)
  print ('Version is ',     version)
  print ('Location is ',    loc)
  if micromamba:
    singularity_template = """
Bootstrap: docker
From: mambaorg/micromamba:focal
# based on debian bullseye
# created {TS}

%files

%setup

%environment
    unset PYTHONPATH
    export PYTHONPATH=/opt/conda/envs/{APP}_{VER}_singularity/lib
    export PYTHONNOUSERSITE=True
    export PYTHONWARNINGS=ignore

%post
    micromamba create --yes --quiet --name {APP}_{VER}_singularity -c base -c conda-forge -c bioconda {APP}={VER}
    micromamba clean -afy

%runscript
    exec "$@"
"""
  else:
    singularity_template = """
Bootstrap: docker
From: continuumio/miniconda3
# based on debian bullseye
# created {TS}

%files

%setup

%environment
    unset PYTHONPATH
    export PYTHONPATH=/opt/conda/envs/{APP}_{VER}_singularity/lib
    export PYTHONNOUSERSITE=True

%post
    apt update && apt install -y man-db

    conda install -c conda-forge mamba
    mamba create  --quiet --yes --name {APP}_{VER}_singularity -c base -c conda-forge -c bioconda  {APP}={VER}

    # activate the conda env and do stuff if required
#    . /opt/conda/etc/profile.d/conda.sh
#    conda activate {APP}_{VER}_singularity




    # Finally have a cleanup of conda to save space in the container
    conda clean -afy  \\
    && find /opt/conda/ -follow -type f -name '*.a' -delete \\
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \\
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete \\
    && find /opt/conda/ -follow -type f -name 'activate*64.sh' -delete

    # And set the env to auto-start when you exec a command
    mkdir -p $SINGULARITY_ROOTFS/.singularity.d/env
    echo "export LC_ALL=C.UTF-8"                    >> $SINGULARITY_ROOTFS/$SINGULARITY_ENVIRONMENT
    echo "source /opt/conda/etc/profile.d/conda.sh" >> $SINGULARITY_ROOTFS/$SINGULARITY_ENVIRONMENT
    echo "conda activate {APP}_{VER}_singularity" >> $SINGULARITY_ROOTFS/$SINGULARITY_ENVIRONMENT


%runscript
    exec "$@"



"""
    
  # current date and time
  timestamp = datetime.now().strftime("%d %B %Y, %H:%M:%S")

  write_singularity_file(loc, app, version, timestamp)


