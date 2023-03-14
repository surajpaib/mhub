"""
-------------------------------------------------
MedicalHub - Run Module for TotalSegmentator.
-------------------------------------------------

-------------------------------------------------
Author: Leonard Nürnberg
Email:  leonard.nuernberg@maastrichtuniversity.nl
-------------------------------------------------
"""

from mhub.mhubio.modules.runner.ModelRunner import ModelRunner
from mhub.mhubio.Config import Instance, InstanceData, DataType, FileType, SEG
from monai.bundle.scripts import run
import os, subprocess

class BundleRunner(ModelRunner):
    def runModel(self, instance: Instance) -> None:
        # data
        inp_data = instance.getData(DataType(FileType.NIFTI))

        # define model output folder
        out_dir = self.config.data.requestTempDir(label="ts-model-out")

        input_dir = os.path.dirname(inp_data.abspath)
        # Run monai bundle

        run("inference", meta_file="configs/metadata.json", \
                        config_file="configs/inference.json", \
                         logging_file="configs/logging.conf", \
                            **{"dataset_dir": input_dir, "output_dir": out_dir, "bundle_root": "/app/bundle"}
                )

        # add output data
        for out_file in os.listdir(out_dir):

            # ignore non nifti files
            if out_file[-7:] != ".nii.gz":
                self.v(f"IGNORE OUTPUT FILE {out_file}")
                continue

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