import csv
import os
import sys
import pprint

from operator import itemgetter

start_dir = ""
output = ""



if __name__ == "__main__":

    empty_files = []
    not_empty_files = []

    start_dir = sys.argv[1]
    output = sys.argv[2]
    table = None
    if len(sys.argv) == 4:
        table = sys.argv[3]

    output_table_dict = {}

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".chck.cex") and ".bak" not in file:
                if os.stat(os.path.join(root, file)).st_size == 0:
                    empty_files.append(file)
                else:
                    not_empty_files.append(file)


    with open(output, "wb") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["file", "passes_check"])

        for file in empty_files:
            writer.writerow([file, "yes"])

        for file in not_empty_files:
            writer.writerow([file, "no"])

    empty_files_keys = [x[0:5] for x in empty_files]
    not_empty_file_keys = [x[0:5] for x in not_empty_files]

    if table:
        fieldnames = ["subject", "06", "07", "08",
                      "09", "10", "11", "12", "13",
                      "14", "15", "16", "17", "18"]

        table_with_checks_name = table.replace(".csv", "_with_checks.csv")

        with open(table, "rU") as table_input:
            with open(table_with_checks_name, "wb") as table_output:

                reader = csv.DictReader(table_input)
                writer = csv.writer(table_output)

                for line in reader:
                    pprint.pprint(line)

                    output_table_dict[line["subject"]] = {key: value for key, value in line.iteritems()}

                for subject in output_table_dict:
                    for visit in output_table_dict[subject]:
                        old_value = output_table_dict[subject][visit]
                        if "{}_{}".format(subject, visit) in empty_files_keys:
                            output_table_dict[subject][visit] = old_value+"-[passes-check]"

                pprint.pprint(output_table_dict)

                writer.writerow(fieldnames)
                for subject in output_table_dict:
                    visit_range = [None]*(len(output_table_dict[subject])-1)
                    for visit in output_table_dict[subject]:
                        if visit != "subject":
                            visit_range[int(visit)-6] = output_table_dict[subject][visit]

                    writer.writerow([subject]+visit_range)

        table_with_checks = []
        with open(table_with_checks_name, "rU") as checked_table:
            reader = csv.reader(checked_table)
            reader.next()
            for line in reader:
                table_with_checks.append(line)

        with open(table_with_checks_name, "wb") as sorted_check_table:
            writer = csv.writer(sorted_check_table)

            sorted_table = sorted(table_with_checks, key=itemgetter(0))

            writer.writerow(fieldnames)
            writer.writerows(sorted_table)






