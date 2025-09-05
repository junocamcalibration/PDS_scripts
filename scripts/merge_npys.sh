#!/bin/bash

for PJ in {20..31}; do
    BGR_folder=../calibrated_dataset_v1/segments/RGB/junocam*PJ${PJ}
    if [ ! -d $BGR_folder ]; then
        BGR_folder=../calibrated_dataset_v1/segments/RGB/junocam*PJ${PJ}*_fixBug
    fi
    UVM_folder=../calibrated_dataset_v1/segments/UVM/junocam*PJ${PJ}

    echo ${BGR_folder} ${UVM_folder}

    mkdir merged_npys/PJ${PJ}

    echo $PJ

    python3 ../JunoCam_calibration_utils/postprocess/merge_npys.py --bgr_files $BGR_folder/test_40/npys/fake_5/ --uvm_files $UVM_folder/test_latest/npys/fake_5/ --save_dir merged_npys/PJ${PJ}
done
