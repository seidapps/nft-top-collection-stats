import csv
import json

class Utils:

    def export_to_csv_file(self, filename, header=None, rows=None):

        with open(filename, 'a') as f:
            
            write = csv.writer(f)  
            if header:
                write.writerow(header)

            for row in rows:      
                write.writerow(row)

    def import_json_file(self, filename):

        with open(filename) as f:
            data = json.load(f)
            return data