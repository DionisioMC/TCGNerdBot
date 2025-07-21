import csv
import os


def add_owner_column():
    """Add Owner column to final_collection.csv and fill with 'XorVitor'"""

    input_file = 'Collections/final_collection.csv'
    output_file = 'Collections/final_collection_updated.csv'

    # Read the original CSV
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Owner']  # Add Owner column

        # Write to new CSV with Owner column
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                row['Owner'] = 'XorVitor'  # Add owner value
                writer.writerow(row)

    # Replace original file with updated file
    os.replace(output_file, input_file)
    print("Successfully added 'Owner' column and filled with 'XorVitor'")
    print(f"Updated {input_file}")


if __name__ == "__main__":
    add_owner_column()
