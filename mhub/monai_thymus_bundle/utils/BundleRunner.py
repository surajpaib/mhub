"""
-------------------------------------------------
MedicalHub - Run Module for TotalSegmentator.
-------------------------------------------------

-------------------------------------------------
Author: Leonard Nürnberg, Suraj Pai
Email:  leonard.nuernberg@maastrichtuniversity.nl, bspai@bwh.harvard.edu
-------------------------------------------------
"""

from mhub.mhubio.modules.runner.ModelRunner import ModelRunner
from mhub.mhubio.Config import Instance, InstanceData, DataType, FileType, SEG
from monai.bundle.scripts import run
import os, subprocess
from pathlib import Path

class BundleRunner(ModelRunner):
    def runModel(self, instance: Instance) -> None:
        # data
        inp_data = instance.getData(DataType(FileType.NIFTI))

        # define model output folder
        out_dir = self.config.data.requestTempDir(label="ts-model-out")

        # Run monai bundle
        self.v(f"Running monai bundle with key: {self.c['run_key']}")


        # TODO: This runs it individually for each image, this is highly inefficient,
        # needs to be updated to run in batch mode.
        run(self.c['run_key'], meta_file="/app/bundle/configs/metadata.json", \
                        config_file="/app/bundle/configs/inference.yaml", \
                         logging_file="/app/bundle/configs/logging.conf", \
                            **{"datalist": [inp_data.abspath], "output_dir": out_dir, "bundle_root": "/app/bundle/"}
                )

        # add output data
        for out_file in Path(out_dir).rglob("*.nii.gz"):
            out_file = str(out_file)
            print(out_file)
            # meta
            meta = {
                "model": "MonaiBundle"
            }

            # create output data
            seg_data_type = DataType(FileType.NIFTI, SEG + meta)           
            seg_path = os.path.join(out_dir, out_file)
            seg_data = InstanceData(seg_path, type=seg_data_type)
            seg_data.base = "" # required since path is external (will be fixed soon)
            instance.addData(seg_data)