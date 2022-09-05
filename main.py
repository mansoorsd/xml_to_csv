import csv
import json
import xmltodict as xmltodict








def flatten_json(nested_json):
    """ function to flatten nested dict """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


def xml_to_dict(xml_file, csv_file_name):
    """Converts markupEntityCollection in XML to CSV """

    with open(xml_file, 'r', encoding="utf-8") as file:
        filedata = file.read()

    # Converting XML to dict
    text_dict = xmltodict.parse(filedata)
    text_dict = json.dumps(text_dict)

    # Cleaning data
    text_dict = text_dict.replace("@", "").replace("xsi:", "")
    text_dict = json.loads(text_dict)

    # Declaring required data dict
    req_data = text_dict["ImageAnnotationCollection"]["imageAnnotations"]["ImageAnnotation"]["markupEntityCollection"]

    # Flattening nested dict
    flattened_data = flatten_json(req_data)

    # Saving to CSV file
    with open(csv_file_name, 'w', newline="\n") as f:
        w = csv.DictWriter(f, flattened_data.keys())
        w.writeheader()
        w.writerow(flattened_data)


if __name__ == "__main__":
    xml_to_dict("sample.xml", "csv_out_file.csv")
