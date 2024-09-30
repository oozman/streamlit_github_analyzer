import streamlit as st
from github import Github
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

from entities.analyze_github_repo import AnalyzeGithubRepo, AnalyzeGithubRepoResult

# Load environment variables
load_dotenv()

st.set_page_config(initial_sidebar_state="collapsed")

st.subheader("Repo Analyzer")
st.text("This analyze lines and commits made in a specific github repo.")

st.divider()

# Input fields
repo_owner = st.text_input("Repository Owner", "netfone")
repo_name = st.text_input("Repository Name", "terrain_web")
branch_name = st.text_input("Branch Name", "develop")
start_date = st.date_input("Start Date", datetime.now().replace(day=1))
end_date = st.date_input("End Date", datetime.now())

# Use environment variable for access token, with an option to override
default_token = os.getenv("GITHUB_ACCESS_TOKEN", "")
#access_token = st.text_input("GitHub Access Token (optional)", value=default_token, type="password")
#access_token = access_token or default_token  # Use input if provided, otherwise use env var

access_token = default_token

if st.button("Analyze"):
    if repo_owner and repo_name and access_token and start_date <= end_date:
        try:

            # Initialize the Github instance
            analyzer = AnalyzeGithubRepo(repo_owner, repo_name, branch_name, start_date, end_date, access_token)

            result = analyzer.analyze()

            # Display results
            st.success("Analysis completed successfully!")
            st.write(f"Analysis for {repo_owner}/{repo_name} on branch '{branch_name}'")
            st.write(f"Period: {start_date} to {end_date}")
            st.write(f"Total lines of code added: {result.lines}")
            st.write(f"Total number of commits: {result.commits}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill in all fields and ensure the start date is before or equal to the end date.")

st.sidebar.markdown("""
## How to use:
1. Enter the repository owner's username.
2. Enter the repository name.
3. Enter the branch name (default is 'develop').
4. Select the start and end dates for analysis.
5. (Optional) Enter your GitHub access token if not set in .env file.
6. Click 'Analyze' to see the results.

Note: You can set your GitHub access token in a .env file to avoid entering it each time.
""")
