import json

from lxml import etree

FILTER_NAMES = ['F275W', 'F395N', 'F502N', 'F631N', 'FQ889N']

# contains the start and end times for each PJ
# this is compiled from the list of images used to generate the mosaic
# it is not the true start/end time of the perijove pass
with open('PJ_times.json', 'r') as infile:
    PJ_times = json.load(infile)

for PJ in range(13, 37):
    et = etree.parse('FITS_template.xml')
    root = et.getroot()

    modification_history = root.xpath("//*[local-name() = 'Modification_History']")[0]
    modification_history[0].xpath("//*[local-name() = 'modification_date']")[
        0
    ].text = '2025-07-29'
    identification_area = root.xpath("//*[local-name() = 'Identification_Area']")[0]
    file_area = root.xpath("//*[local-name() = 'File_Area_Observational']")[0]
    observation_area = root.xpath("//*[local-name() = 'Observation_Area']")[0]
    time_coordinates = observation_area.xpath("//*[local-name() = 'Time_Coordinates']")[
        0
    ]

    identification_area.xpath("//*[local-name() = 'title']")[0].text = f"PJ {PJ} mosaic"

    time_coordinates.xpath("//*[local-name() = 'start_date_time']")[0].text = PJ_times[
        f"{PJ}"
    ]["start"]
    time_coordinates.xpath("//*[local-name() = 'stop_date_time']")[0].text = PJ_times[
        str(PJ)
    ]["end"]

    counter = 0
    for child in file_area:
        if "File" in child.tag:
            for child1 in child:
                if "file_name" in child1.tag:
                    child1.text = f"junocam_calibration_PJ{PJ}.fits"

        if "Array_2D_Image" in child.tag:
            for child1 in child:
                if "description" in child1.tag:
                    child1.text = f"Global map, filter {FILTER_NAMES[counter]}"

            counter += 1

    et.write(
        f"data_mosaics/PJ{PJ}/junocam_calibration_PJ{PJ}.xml",
        xml_declaration=True,
        encoding='UTF-8',
    )
