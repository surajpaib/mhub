"""
-------------------------------------------------
MedicalHub - run monai bundle pipeline
-------------------------------------------------

-------------------------------------------------
Author: Leonard Nürnberg, Suraj Pai
Email:  leonard.nuernberg@maastrichtuniversity.nl, bspai@bwh.harvard.edu
-------------------------------------------------
"""

import sys, os
sys.path.append('.')

from mhub.mhubio.Config import Config, DataType, FileType, CT, SEG
from mhub.mhubio.modules.importer.UnsortedDicomImporter import UnsortedInstanceImporter
from mhub.mhubio.modules.importer.DataSorter import DataSorter
from mhub.mhubio.modules.convert.NiftiConverter import NiftiConverter
from mhub.mhubio.modules.convert.DsegConverter import DsegConverter
from mhub.mhubio.modules.organizer.DataOrganizer import DataOrganizer
from mhub.monai_bundle.utils.BundleRunner import BundleRunner

# clean-up
import shutil
shutil.rmtree("/app/data/sorted", ignore_errors=True)
shutil.rmtree("/app/data/nifti", ignore_errors=True)
shutil.rmtree("/app/tmp", ignore_errors=True)
shutil.rmtree("/app/data/output_data", ignore_errors=True)

# config
config = Config('/app/mhub/monai_bundle/config/config.yml')
config.verbose = True  # TODO: define levels of verbosity and integrate consistently. 
config.debug = False

# import
UnsortedInstanceImporter(config).execute()

# sort
DataSorter(config).execute()

# convert (ct:dicom -> ct:nifti)
NiftiConverter(config).execute()

# execute model (nnunet)
runner = BundleRunner(config)
runner.input_type = DataType(FileType.NIFTI, CT)
runner.execute()

# convert (seg:nifti -> seg:dcm)
DsegConverter(config).execute()

# organize data into output folder
organizer = DataOrganizer(config, set_file_permissions=sys.platform.startswith('linux'))
organizer.setTarget(DataType(FileType.NIFTI, CT), "/app/data/output_data/image.nii.gz")
organizer.setTarget(DataType(FileType.NIFTI, SEG), f"/app/data/output_data/{organizer.c['label']}.nii.gz")
organizer.setTarget(DataType(FileType.DICOMSEG, SEG), f"/app/data/output_data/{organizer.c['label']}.seg.dcm")
organizer.execute()
