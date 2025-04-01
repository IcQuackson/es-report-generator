import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

GITLAB_URL = os.environ.get("GITLAB_URL")
PROJECT_ID = os.environ.get("PROJECT_ID")
PRIVATE_TOKEN = os.environ.get("ACCESS_TOKEN")

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

FEATURES = config["features"]
SUBGROUPS = config["subgroups"]
START_DATE = config.get("creation_date", "YYYY-MM-DD")

START_DATE_ISO = f"{START_DATE}T00:00:00Z"

HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}


def get_group_number():
    """Fetch the group number from the project name."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        project_data = response.json()
        project_name = project_data.get("name", "")
        group_number = project_name.split("-")[-1] if "-" in project_name else ""
        return group_number
    else:
        print(f"Error fetching project data: {response.status_code}")
        return None

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
    group_number = get_group_number()
    if group_number is None:
        return "Error: Unable to fetch group number."
    report = f"# ES P2 submission, Group {group_number}\n\n## Did your group use the base code provided?\n\nYes\n\n"

    for feature, label in FEATURES.items():
        # Fetch issues and MRs for the feature and date range
        issues = get_issues(label)
        merge_requests = get_merge_requests(label)

        report += f"\n## Feature {feature}\n\n### Subgroup\n"

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

generated_report = format_report()

output_file = f"P2.md"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(generated_report)

print(f"Report successfully generated: {output_file}")
