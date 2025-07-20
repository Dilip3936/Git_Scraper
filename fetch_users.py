import requests
import time 

def get_pull_request_usernames(owner, repo, access_token=None,DELAY=1):
    usernames = set()
    page = 1
    per_page = 100
    headers = {"Accept": "application/vnd.github.v3+json"}
    if access_token:
        headers["Authorization"] = f"token {access_token}"

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        params = {"state": "all", "per_page": per_page, "page": page}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            pull_requests = response.json()

            if not pull_requests:
                break

            for pr in pull_requests:
                if pr.get("user"):
                    usernames.add(pr["user"]["login"])
            
            page += 1

            time.sleep(DELAY)

        except requests.exceptions.HTTPError as e:
            # If a 403 Forbidden error occurs, it might be a secondary rate limit.
            if e.response.status_code == 403:
                print("Rate limit likely exceeded. Waiting for 60 seconds before retrying...")
                time.sleep(60)
                continue # Retry the current page request
            else:
                raise # Re-raise other HTTP errors

    return list(usernames)
