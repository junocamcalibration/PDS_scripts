#!/bin/bash

for PJ in {13..36}; do
    geotiff_folder=geotiffs/PJ${PJ}

    echo $PJ
    mkdir data_segments/PJ${PJ}

    for file in $geotiff_folder/*.tif; do
        fname=${file##*/}
        fname=${fname%.*}
        xml_file=data_segments/PJ${PJ}/${fname}.xml
        echo ${fname}
        # gdal_translate -of "PDS4" -co CREATE_LABEL_ONLY=YES $file data_segments/PJ${PJ}/${fname}.xml
        gdal_translate\
            -of "PDS4"\
            -co "CREATE_LABEL_ONLY=YES"\
            -co "IMAGE_FILENAME=${fname}"\
            -co TEMPLATE=segment_template.xml\
            $file $xml_file

        sed -i 's/filename/'$fname'/' $xml_file
        cp $file data_segments/PJ${PJ}/${fname}.tif
        # gdal_translate -of "PDS4" ${file}
    done

done


