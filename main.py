# main.py
from fetch_users import get_pull_request_usernames
from read_from_csv import read_usernames_from_csv
from fetch_details import get_user_details
from fetch_emails import get_user_emails
from save_to_csv import save_users_to_csv
import requests
from config import GITHUB_TOKEN #add your GitHub Personal Access Token to the config.py file.

if __name__ == "__main__":

    # --- Configuration ---
    REPOSITORY_OWNER = "gadepall" # add the username
    REPOSITORY_NAME = "digital-communication" # add the repo name
    FETCH_FROM_REPO = True # set true to get usernames from repo's pull history
    DELAY=0.1 #delay (in seconds) between each request to avoid secondary rate limits
    FETCH_DETAILS = True
    FETCH_EMAILS = True
    USE_TOKEN=True  #set it to false to not use your token
    USER_DETAILS_FIELDS = [
        "name",
        #"avatar_url",
        #"company",
        #"location",
        "public_repos",
        #"followers",
        #"created_at"
    ]
    INPUT_CSV_FILE = "output/github_users_details.csv"
    OUTPUT_FILE = "output/github_users_export.csv"

    # --- Security Check ---
    if USE_TOKEN :
        if not GITHUB_TOKEN or GITHUB_TOKEN == "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
            print("ERROR: Please add your GitHub Personal Access Token to the config.py file.")
    else :
        GITHUB_TOKEN=None
    # --- main code ---
    print(f"Starting scraper for repository: {REPOSITORY_OWNER}/{REPOSITORY_NAME}")

    try:
        usernames = []
        if FETCH_FROM_REPO:
            print(f"\n--- Fetching usernames from repo '{REPOSITORY_OWNER}/{REPOSITORY_NAME}' ---")
            usernames = get_pull_request_usernames(REPOSITORY_OWNER, REPOSITORY_NAME, GITHUB_TOKEN,DELAY)
        else:
            print(f"\n--- Reading usernames from file '{INPUT_CSV_FILE}' ---")
            usernames = read_usernames_from_csv(INPUT_CSV_FILE)

        if not usernames:
            print("No usernames were loaded. Exiting.")
            exit()
        
        print(f"Processing {len(usernames)} unique users.")
        
        # Initialize data structure
        users_data = [{'username': user, 'profile_link': f'https://github.com/{user}'} for user in usernames]

        if FETCH_DETAILS:
            print("\n--- Fetching user details (name, profile URL) ---")
            users_data = get_user_details(users_data, GITHUB_TOKEN, USER_DETAILS_FIELDS,DELAY)

        if FETCH_EMAILS:
            print("\n--- Fetching user emails ---")
            users_data = get_user_emails(users_data, GITHUB_TOKEN,DELAY)

        print(f"\n--- Saving data to {OUTPUT_FILE} ---")
        save_users_to_csv(users_data, OUTPUT_FILE)
        print(f"\nSuccessfully exported details for {len(users_data)} unique users to {OUTPUT_FILE}")

    except requests.exceptions.HTTPError as e:
        print(f"\nAn HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"\nA network error occurred: {e}")
