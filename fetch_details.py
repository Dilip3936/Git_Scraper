import requests
import time 

def get_user_details(users_data, access_token=None, fields_to_fetch=None,DELAY=1):
    if fields_to_fetch is None:
        fields_to_fetch = ['name']  # Default to only getting the name

    headers = {"Accept": "application/vnd.github.v3+json"}
    if access_token:
        headers["Authorization"] = f"token {access_token}"

    total_users = len(users_data)
    i = 0
    while i < total_users:
        user = users_data[i]
        username = user["username"]
        print(f"  ({i + 1}/{total_users}) Fetching details for {username}")

        user_url = f"https://api.github.com/users/{username}"

        try:
            user_response = requests.get(user_url, headers=headers)
            user_response.raise_for_status()  
            user_profile = user_response.json()

            for field in fields_to_fetch:
                user[field] = user_profile.get(field) or "N/A"
            
            i += 1
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("      -> Rate limit likely exceeded. Waiting for 60 seconds before retrying...")
                time.sleep(60)
                continue
            else:
                for field in fields_to_fetch:
                    user[field] = "Error"
                i += 1 
        
        except requests.exceptions.RequestException as e:
            for field in fields_to_fetch:
                user[field] = "Error"
            i += 1 
        
        if i < total_users:
            time.sleep(DELAY)

    return users_data
