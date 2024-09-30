from datetime import datetime

import pytz
from dotenv import load_dotenv
from github import Github
from pydantic import BaseModel

# Load environment variables
load_dotenv()


class AnalyzeGithubRepoResult(BaseModel):
    lines: int
    commits: int


class AnalyzeGithubRepo:
    def __init__(self, repo_owner, repo_name, branch_name, start_date, end_date, access_token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.start_date = start_date
        self.end_date = end_date
        self.access_token = access_token

    def analyze(self):
        # Initialize the Github instance
        g = Github(self.access_token)

        # Get the repository
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")

        # Convert dates to datetime with UTC timezone
        start_datetime = datetime.combine(self.start_date, datetime.min.time()).replace(tzinfo=pytz.UTC)
        end_datetime = datetime.combine(self.end_date, datetime.max.time()).replace(tzinfo=pytz.UTC)

        # Get all commits within the date range for the specified branch
        commits = repo.get_commits(sha=self.branch_name, since=start_datetime, until=end_datetime)

        # Initialize counters
        total_lines_added = 0
        total_commits = 0

        # Iterate through all commits
        for commit in commits:
            # Get the stats for the commit
            stats = commit.stats

            # Add the number of additions to the total
            total_lines_added += stats.additions

            # Increment the commit counter
            total_commits += 1

        result = {'lines': total_lines_added, 'commits': total_commits}

        return AnalyzeGithubRepoResult(**result)
