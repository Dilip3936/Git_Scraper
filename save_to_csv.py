import csv

def save_users_to_csv(users_data, filename="github_users_export.csv"):
    if not users_data:
        print("No data to save.")
        return

    headers = list(users_data[0].keys())
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(users_data)
