import csv
import os
import sys

start_dir = ""
output = ""

if __name__ == "__main__":

    empty_files = []
    not_empty_files = []

    start_dir = sys.argv[1]
    output = sys.argv[2]

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".chck.cex"):
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
