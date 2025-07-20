import requests
import time # Import the time module

def get_user_emails(users_data, access_token=None,DELAY=1):
    #Attempts to find user emails by checking their public events,

    headers = {"Accept": "application/vnd.github.v3+json"}
    if access_token:
        headers["Authorization"] = f"token {access_token}"

    total_users = len(users_data)
    i = 0
    while i < total_users:
        user = users_data[i]
        username = user["username"]
        user['email'] = 'N/A'
        
        print(f"  ({i + 1}/{total_users}) Searching for email for {username}")

        events_url = f"https://api.github.com/users/{username}/events/public"
        try:
            events_response = requests.get(events_url, headers=headers, params={'per_page': 100})
            events_response.raise_for_status()
            events = events_response.json()
            
            for event in events:
                if event.get("type") == "PushEvent":
                    commits = event.get("payload", {}).get("commits", [])
                    for commit in commits:
                        author = commit.get("author", {})
                        commit_email = author.get("email")
                        commit_name = author.get("name")
                        
                        if commit_email and commit_name == username and 'noreply.github.com' not in commit_email:
                            user["email"] = commit_email
                            break
                if user["email"] != "N/A":
                    break
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("      -> Rate limit likely exceeded. Waiting for 60 seconds before retrying...")
                time.sleep(60)
                continue
            else:
                print(f"      -> Warning: Could not fetch events for user '{username}'. HTTP Error: {e}")

        except requests.exceptions.RequestException as e:
            print(f"      -> Warning: Could not fetch events for user '{username}'. Network Error: {e}")
        
        i += 1
        
        if i < total_users:
            time.sleep(DELAY)

    return users_data
