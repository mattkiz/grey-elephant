import csv
import  pickle
subcategory_ids = {}
with open("catalog.csv") as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=",")
    for row in csv_reader:
        if (len(row)<2) : continue
        try:
            subcategory = (row[1].strip()).split(">")[1].strip()
            ID = int(row[0].strip())
            if subcategory not in subcategory_ids.keys():
                subcategory_ids[subcategory] = []
            if ID not in subcategory_ids[subcategory]: subcategory_ids[subcategory].append(ID)
        except:
            pass

pickle.dump(subcategory_ids,open("subcategoryIDs.pkl","wb"))
