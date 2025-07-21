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
    list_colections = glob.glob(r'Colections\*\*.csv')
    print(list_colections)
    # create a csv colection with the final data
    final_colection = []
    for file_path in list_colections:
        owner = file_path.split("\\")[1]
        csv_dict = read_csv_to_dict(file_path, owner)
        final_colection.append(csv_dict)

    list_colections = glob.glob(r'Colections\*\*.txt')
    # write the final colection to a csv file
    with open('Colections\\final_colection.csv', mode='w', newline='') as file:
        csv_writer = csv.DictWriter(
            file, fieldnames=final_colection[0][0].keys())
        csv_writer.writeheader()
        for colection in final_colection:
            csv_writer.writerows(colection)
