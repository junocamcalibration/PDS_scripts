import glob
import json
import os
import re
import subprocess

mapping = {
    "C25_PJ15": [13, 14, 15, 16],
    "C26_PJ18": [17, 18, 19],
    "C26_PJ20": [20, 21, 22, 23, 24],
    "C27_PJ27": [25, 26, 27, 28, 29, 30],
    "C28_PJ33": [31, 32, 33, 34, 35, 36],
}

pj_map = {}

for PJ in range(13, 37):
    # loop through the perijoves and figure out which
    # Hubble cycle it was trained on
    # this will essentially invert the `mapping` dictionary
    map_key = None
    for key, val in mapping.items():
        if PJ in val:
            map_key = key
            break
    map_items = re.findall(r'C(\d{2})_PJ(\d{2})', map_key)[0]
    pj_map[PJ] = map_items

for PJ in range(13, 37):
    print(PJ)
    BGR_folder = glob.glob(f'../calibrated_dataset_v1/mosaics/RGB/junocam*PJ{PJ}/')

    # get the right folder -- sometimes the folders have slightly different names
    if len(BGR_folder) == 0:
        BGR_folder = glob.glob(
            f'../calibrated_dataset_v1/mosaics/RGB/junocam*PJ{PJ}*_fixBug'
        )[0]
    else:
        BGR_folder = BGR_folder[0]

    UVM_folder = glob.glob(f'../calibrated_dataset_v1/mosaics/UVM/junocam*PJ{PJ}')[0]

    cycle, pj_train = pj_map[PJ]

    with open('metadata.json', 'w') as metafile:
        json.dump(
            {
                "ckpt": f"junocam_calibration_C{cycle}_PJ{pj_train}",
                "modelep": 50,
                "junopj": PJ,
                "HSTcyc": cycle,
            },
            metafile,
        )
    if not os.path.exists(f"FITS/PJ{PJ}"):
       os.makedirs(f'FITS/PJ{PJ}')
    subprocess.run(
        [
            'python3',
            '../JunoCam_calibration_utils/postprocess/create_FITS_export.py',
            '-bgr_path',
            os.path.join(BGR_folder, 'mosaic.npy'),
            '-uv_path',
            os.path.join(UVM_folder, 'mosaic_UV.npy'),
            '-methane_path',
            os.path.join(UVM_folder, 'mosaic_M.npy'),
            '-metadata',
            'metadata.json',
            '-output',
            f'FITS/PJ{PJ}/junocam_calibration_PJ{PJ}',
            '-overwrite',
        ]
    )
