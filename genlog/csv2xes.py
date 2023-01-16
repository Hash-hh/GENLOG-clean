import datetime
import os

def csv2xes(log_csv_file_name):
    """
    Convert splitted CSV files to XES files.
    Parameters:
        log_csv_file_name (str): The name of the CSV file in the data/logs folder.
    """

    print("Converting splitted csv files to splitted xes files...")

    split_csv_path = f'data/csvs/{log_csv_file_name}/csv_splits'

    split_xes_path = f'data/csvs/{log_csv_file_name}/xes_splits'
    if not os.path.exists(split_xes_path):
        os.makedirs(split_xes_path)

    for split_csv in os.listdir(split_csv_path):

        with open(f"{split_xes_path}/{split_csv.split('.')[0]}.xes", "w") as x:  # dump xes file here
            x.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
            x.write("<log xes.version=\"1.0\" xes.features=\"nested-attributes\" openxes.version=\"1.0RC7\">\n\t<extension name=\"Concept\" prefix=\"concept\" uri=\"http://www.xes-standard.org/concept.xesext\"/>\n\t<global scope=\"event\">\n\t\t<string key=\"concept:name\" value=\"__INVALID__\"/>\n\t</global>\n\t<classifier name=\"Event Name\" keys=\"concept:name\"/>")
            x.write("\t<trace>\n")

            with open(f'{split_csv_path}/{split_csv}', 'r') as f:  # csv file

                # while "\n" in data: data.remove("\n")  # removes empty lines if exist
                # f = [lst for lst in f if lst != ['\n']]  # removes empty elements

                for l in f:
                    data = l.split(',')

                    dt = data[0]  # 01/01/2018 20:00

                    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M'):
                        try:
                            d = datetime.datetime.strptime(dt, fmt)
                        except ValueError:
                            pass

                    # d = datetime.datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
                    d.strftime('%Y-%m-%dT%H:%M:%S.000+00:00')  #  2017-02-10T13:55:00.615+01:00


                    x.write("\t\t<event>\n" +
                            f"\t\t\t<date key=\"time:timestamp\" value=\"{d}\"/>\n" +
                            f"\t\t\t<string key=\"netvol\" value=\"{data[1]}\"/>\n" +
                            f"\t\t\t<string key=\"rundensi\" value=\"{data[2]}\"/>\n" +
                            f"\t\t\t<string key=\"absunc\" value=\"{data[3]}\"/>\n" +
                            f"\t\t\t<string key=\"asunc\" value=\"{data[4]}\"/>\n" +
                            f"\t\t\t<string key=\"bsunc\" value=\"{data[5]}\"/>\n" +
                            f"\t\t\t<string key=\"acurrent\" value=\"{data[6]}\"/>\n" +
                            f"\t\t\t<string key=\"bcurrent\" value=\"{data[7]}\"/>\n" +
                            f"\t\t\t<string key=\"abdisch\" value=\"{data[8]}\"/>\n" +
                            f"\t\t\t<string key=\"abminf\" value=\"{data[9]}\"/>\n" +
                            f"\t\t\t<string key=\"abtotdisch\" value=\"{data[10]}\"/>\n" +
                            f"\t\t\t<string key=\"abmanifold\" value=\"{data[11]}\"/>\n" +
                            f"\t\t\t<string key=\"abpumpdis\" value=\"{data[12]}\"/>\n" +
                            "\t\t</event>\n")

            x.write("\t</trace>\n")
            x.write("</log>")