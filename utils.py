import csv

class Utils:

    def export_to_csv_file(self, filename=None, header=None, rows=None):

        with open(filename, 'w') as f:
            
            write = csv.writer(f)  
            if header:
                write.writerow(header)

            for row in rows:      
                write.writerow(row)