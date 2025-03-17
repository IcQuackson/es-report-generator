# GitLab Project Report Generator

## Overview
This script automates the generation of a project report by fetching issues and merge requests from GitLab. It categorizes them based on predefined labels and assigns them to the respective team members.

## Features
- Fetches issues and merge requests from GitLab.
- Categorizes tasks based on feature labels.
- Assigns issues and MRs to the correct subgroup members.
- Generates a structured markdown report.
- Supports multiple teams with configurable settings.
- Filters issues and merge requests based on creation date.

---

## Setup Instructions

### 1. Clone or Download the Repository
```sh
git clone https://github.com/IcQuackson/es-report-generator.git
cd es-report-generator
```

### 2. Install Dependencies
Ensure you have Python installed, then run:
```sh
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Rename the example environment file and update it with your credentials:
```sh
cp .env.example .env
```

Edit `.env` and provide your GitLab details:
```ini
GITLAB_URL=https://gitlab.rnl.tecnico.ulisboa.pt
PROJECT_ID=YOUR_PROJECT_ID
ACCESS_TOKEN=YOUR_ACCESS_TOKEN
```

### 4. Set the Creation Date Filter
The script filters issues and merge requests **created after a specific date**. To configure this:
1. Open `config.json`.
2. Add or modify the `creation_date` field:
```json
"creation_date": "YYYY-MM-DD"
```
3. Replace `YYYY-MM-DD` with the desired start date for filtering issues and merge requests.

### 5. Generate a GitLab API Key
To authenticate with GitLab, you need a **Personal Access Token**.

#### Steps to Create an API Key:
- [GitLab API Key Creation](https://screenful.com/guide/how-to/gitlab-apikey)
1. Go to **GitLab Profile Settings**.
2. Click on **"Access Tokens"**.
3. Create a new token with the **`read_api`** permission.
4. Copy the token and paste it into your `.env` file as `ACCESS_TOKEN`.

### 6. Get Your Project ID
To retrieve your **Project ID**:
1. Go to your **GitLab Project Page**.
![alt text](<Screenshot 2025-03-17 035058.png>)
4. Copy the ID and paste it into `.env` under `PROJECT_ID`.

### 7. Customize Team Settings
Edit `config.json` to define subgroup members and feature labels:
```json
{
    "features": {
        "CA": "Suggest Activity",
        "SP": "Volunteer Profile",
        "AI": "Institution Profile"
    },
    "subgroups": {
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
    },
    "creation_date": "YYYY-MM-DD"
}
```

### 8. Run the Script
Execute the script to generate the report:
```sh
python report_generator.py
```

### 9. Output
The script generates a markdown file named based on the configured date:
```
P2.md
```
This file contains the structured project report based on your GitLab repository.

---

## Troubleshooting
### Common Issues
#### 1. Authentication Error
- Ensure your GitLab token has the correct permissions (`read_api`).
- Check that `.env` is correctly configured.

#### 2. No Issues or MRs Retrieved
- Verify that your GitLab labels match the labels in `config.json`.
- Ensure issues and merge requests are correctly labeled in GitLab.
- Ensure the `creation_date` is set correctly in `config.json`.

#### 3. Dependencies Not Found
Run:
```sh
pip install -r requirements.txt
```

---

## Contributing
- Fork the repository and submit pull requests.
- Report issues and suggest features in the GitLab issue tracker.

## License
MIT License

