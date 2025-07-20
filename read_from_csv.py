import csv

def read_usernames_from_csv(filename):
    usernames = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            
            username_col_name = None
            for header in headers:
                if header.lower() == 'username':
                    username_col_name = header
                    break
            
            if not username_col_name:
                username_col_name = headers[0]
            else:
                print(f"Reading usernames from column: '{username_col_name}'")

            for row in reader:
                if row.get(username_col_name):
                    usernames.append(row[username_col_name])

    except FileNotFoundError:
        print(f"ERROR: Input file not found at '{filename}'. Please check the INPUT_CSV_FILE path in main.py.")
        return []
    except IndexError:
        print(f"ERROR: The CSV file '{filename}' appears to be empty or invalid.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return []
        
    return usernames
