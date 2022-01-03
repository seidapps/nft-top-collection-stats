import csv

class Utils:

    def export_to_csv_file(self, filename, rows):

        with open(filename, 'w') as f:
            
            write = csv.writer(f)  
            for row in rows:      
                write.writerow(row)