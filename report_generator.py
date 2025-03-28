import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# GitLab Configuration
GITLAB_URL = os.environ.get("GITLAB_URL")
PROJECT_ID = os.environ.get("PROJECT_ID")
PRIVATE_TOKEN = os.environ.get("ACCESS_TOKEN")

# Load Team Configuration from JSON
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

FEATURES = config["features"]
SUBGROUPS = config["subgroups"]
START_DATE = config.get("creation_date", "YYYY-MM-DD")  # Default placeholder

# Convert START_DATE to ISO format
START_DATE_ISO = f"{START_DATE}T00:00:00Z"

# Headers for API authentication
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

# GitLab API Endpoints with Date Filtering
def get_issues(feature_label):
    """Fetch issues based on feature label and creation date."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues?labels={feature_label}&created_after={START_DATE_ISO}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def get_merge_requests(feature_label):
    """Fetch merge requests based on feature label and creation date."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/merge_requests?labels={feature_label}&created_after={START_DATE_ISO}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def format_report():
    """Generate the full report according to the provided template."""
    report = f"# ES P2 Submission - Issues & MRs Created After {START_DATE}\n\n## Did your group use the base code provided?\n\nYes / No\n\n"

    for feature, label in FEATURES.items():
        # Fetch issues and MRs for the feature and date range
        issues = get_issues(label)
        merge_requests = get_merge_requests(label)

        report += f"\n## Feature {feature} - Created After {START_DATE}\n\n### Subgroup\n"

        for member in SUBGROUPS[feature]:
            # Filter issues assigned to the user
            assigned_issues = [
                f"[#{issue['iid']}]({issue['web_url']})"
                for issue in issues if issue.get("assignee") and issue["assignee"]["username"] == member["username"]
            ]
            assigned_issues_str = ", ".join(assigned_issues) if assigned_issues else "None"

            # Member details
            report += f" - {member['name']}, {member['istID']}, [GitLab link]({GITLAB_URL}/{member['username']})\n"
            report += f"   + Issues assigned: {assigned_issues_str}\n"

        # Merge Requests Section
        report += "\n### Merge requests associated with this feature\n\n"
        if merge_requests:
            for mr in merge_requests:
                report += f" - [MR #{mr['iid']}]({mr['web_url']})\n"
        else:
            report += " - None\n"

        # Notes Section
        report += "\n### Notes\n\nAdd here any relevant information that you might want the teaching team to consider.\n\n---\n"

    return report

# Generate the report
generated_report = format_report()

# Save to a markdown file
output_file = f"P2.md"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(generated_report)

print(f"Report successfully generated: {output_file}")
