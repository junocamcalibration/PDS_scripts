#!/bin/bash

for PJ in {20..31}; do
    npy_folder=merged_npys/PJ${PJ}/

    mkdir geotiffs/PJ${PJ}

    echo $PJ

    python3 ../JunoCam_calibration_utils/postprocess/create_geotiff_exports.py\
        --input_metadata ../calibrated_dataset_v1/A_metadata.csv\
        --path-to-images ${npy_folder}\
        --path-to-output geotiffs/PJ${PJ}
done

