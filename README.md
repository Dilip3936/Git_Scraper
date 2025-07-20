# GitHub User Data Scraper 

A modular Python tool to collect and enrich data for GitHub users. You can either scrape users who have submitted pull requests to a specific repository or provide a custom list of usernames from a CSV file.

## Features

- **Two Data Sources**:
    - Fetch usernames from a repository's pull requests.
    - Enrich a pre-existing list of usernames from a local CSV file.
- **Configurable Data**: Choose exactly which user profile details you want to fetch (name, company, location, followers, etc.).
- **Email Discovery**: Attempts to find public email addresses from user commit history.
- **Modular Design**: Easily enable or disable features in the main script.
- **CSV Export**: Saves all collected data into a clean CSV file.

## Setup

1. **Clone the repository:**
    
   ```
    git clone https://github.com/Dilip3936/Git_Scraper.git cd Git_Scraper
    ```

2. **Create a virtual environment:**

```shell
python -m venv venv
```

2. **Activate it:**

- **Windows:**

```shell
myenv\Scripts\activate
```

- **macOS & Linux:**

```shell
source venv/bin/activate
```

3. **Install the required libraries:**

```shell
pip install -r requirements.txt
```
   
4. **Create your configuration file:**
    - Create a file named `config.py`.
    - Adding your token in compulsory for all the actions but it is recommended.
    - Get your PAT token from [GitHub](https://github.com/settings/tokens)
    - Add your GitHub Personal Access Token to it:
        
        ``` python
        # config.py 
        GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```
        
5. **IMPORTANT: Secure your token:**
    - Dont ever share your token with any one.      

## A Note on API Rate Limits

Using a **Personal Access Token is highly recommended** as the GitHub API limits requests. This script can exceed these limits on large projects.

- **Primary Limits**: This is a limit on requests per hour.
    - **Without a Token**: Limited to **60** requests per hour (by IP address).
    - **With a Token**: Increased to **5,000** requests per hour (by account).
- **Secondary Limits:** There are also some secondary limits that prevent sending multiple requests in a short duration
- For more information you can refer [Quickstart for GitHub REST API - GitHub Docs](https://docs.github.com/en/rest/quickstart)
- I tried to avoid the secondary rate limits by introducing a delay that can be configured.
## How to Use

All configuration is done by editing the flags at the top of the `main.py` file.

1. **Choose your data source:**
    - **To scrape a repository**: Set `FETCH_FROM_REPO = True` and specify the `REPOSITORY_OWNER` and `REPOSITORY_NAME`.
    - **To read from a file**: Set `FETCH_FROM_REPO = False` and ensure `INPUT_CSV_FILE` points to your CSV file. The script will look for a "Username" column.
2. **Select the data you want:**
    - Enable or disable features with `FETCH_DETAILS` and `FETCH_EMAILS`.
    - Customize the data you want to collect by editing the `USER_DETAILS_FIELDS` list.
3. **Run the script:**
    ``` bash
    python main.py
    ```

The output will be saved to `github_users_export.csv` (or the filename you specify in `OUTPUT_FILE`).