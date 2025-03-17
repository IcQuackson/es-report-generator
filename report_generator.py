import requests
# use .env file
from dotenv import load_dotenv
import os

load_dotenv()

# GitLab Configuration
GITLAB_URL = os.environ.get("GITLAB_URL")
PROJECT_ID = os.environ.get("PROJECT_ID")
PRIVATE_TOKEN = os.environ.get("ACCESS_TOKEN")

print(GITLAB_URL, PROJECT_ID, PRIVATE_TOKEN)

# Headers for API authentication
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

# Feature Labels in GitLab
FEATURES = {
    "CA": "Suggest Activity",
    "SP": "Volunteer Profile",
    "AI": "Institution Profile"
}

# Subgroups with names, istID, and GitLab usernames
SUBGROUPS = {
    "CA": [
        {"name": "Pedro Gonçalves", "istID": "ist187559", "username": "ist187559"},
        {"name": "Martim Garcia dos Anjos", "istID": "ist1103704", "username": "ist1103704"}
    ],
    "SP": [
        {"name": "Xavier Augusto", "istID": "ist1106997", "username": "ist1106997"},
        {"name": "Luísa Folques Cardoso", "istID": "ist1106871", "username": "ist1106871"}
    ],
    "AI": [
        {"name": "Tomás de Sousa Santos", "istID": "ist1104111", "username": "ist1104111"},
        {"name": "Diogo Pinto", "istID": "ist1103976", "username": "ist1103976"}
    ]
}

# GitLab API Endpoints
def get_issues(feature_label):
    """Fetch issues based on the feature label."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues?labels={feature_label}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def get_merge_requests(feature_label):
    """Fetch merge requests based on the feature label."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/merge_requests?labels={feature_label}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def format_report():
    """Generate the full report according to the provided template."""
    report = "# ES P2 submission, Group NN\n\n## Did your group use the base code provided?\n\nYes / No\n\n"

    for feature, label in FEATURES.items():
        # Fetch issues and MRs for the feature
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

# Generate the report
generated_report = format_report()

# Save to a markdown file
with open("GitLab_Project_Report.md", "w", encoding="utf-8") as file:
    file.write(generated_report)

print("Report successfully generated: GitLab_Project_Report.md")
