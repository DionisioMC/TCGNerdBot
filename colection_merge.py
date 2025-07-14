import csv
import glob


def read_csv_to_dict(file_path, name):
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        # change the name of the first column to 'Name'
        if csv_reader.fieldnames[0] == 'Binder Name':
            csv_reader.fieldnames[0] = 'Owner'
            data = [row for row in csv_reader]
            # add the owner name to the first row
            for row in data:
                row['Owner'] = name
        elif csv_reader.fieldnames[0] == 'Name':
            data = [row for row in csv_reader]
            # add the owner name to the first row
            for row in data:
                row['Owner'] = name
    return data


if __name__ == "__main__":
    list_collections = glob.glob(r'Collections\*\*.csv')
    print(list_collections)
    # create a csv collection with the final data
    final_collection = []
    for file_path in list_collections:
        owner = file_path.split("\\")[1]
        csv_dict = read_csv_to_dict(file_path, owner)
        final_collection.append(csv_dict)

    list_collections = glob.glob(r'Collections\*\*.txt')
    # write the final collection to a csv file
    with open('Collections\\final_collection.csv', mode='w', newline='') as file:
        csv_writer = csv.DictWriter(
            file, fieldnames=final_collection[0][0].keys())
        csv_writer.writeheader()
        for collection in final_collection:
            csv_writer.writerows(collection)
