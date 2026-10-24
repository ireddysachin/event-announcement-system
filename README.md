## 🚀 Event Announcement System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Tests-10_Passing-brightgreen?logo=pytest" alt="Tests">
  <img src="https://img.shields.io/badge/Terraform-Infrastructure-7B42BC?logo=terraform&logoColor=white" alt="Terraform">
  <img src="https://img.shields.io/badge/Floci-Local_Cloud_Emulation-blue" alt="Floci">
</p>

<p align="center">
  <strong>A full-stack event announcement application with local cloud-service integration and Infrastructure as Code.</strong>
  <br>
  Create events, upload banners, and publish event announcements using Flask, SQLite, Terraform, and Floci.
</p>

---

## 🌟 About the Project

The **Event Announcement System** is a Python web application for managing technical events and displaying announcements through a browser-based interface.

The project combines application development with DevOps practices. Flask handles the web application and API routes, SQLite stores event and subscriber data, and Floci provides a local environment for experimenting with supported AWS-compatible services.

Terraform manages the local S3 and SNS infrastructure, allowing infrastructure changes to be described as code without intentionally deploying resources to real AWS.

## ✨ Key Features

| Feature | Description |
|---|---|
| 📅 Event management | Display upcoming events with dates, locations, and descriptions |
| ➕ Event creation | Create events through the web interface and REST API |
| 🖼️ Banner uploads | Upload event banner images to local Floci S3 |
| 🗄️ Database persistence | Store event details and subscriber records in SQLite |
| 📧 Subscription | Accept subscriptions and handle duplicate subscriptions |
| 🔔 Event announcements | Publish event notifications through a local SNS topic |
| 🧪 Automated testing | Test application behaviour with pytest |
| 🏗️ Infrastructure as Code | Manage local S3 and SNS resources with Terraform |
| 🔒 Safer local development | Ignore Terraform state, plan files, the local database, and environment files in Git |

## 🏛️ Architecture

```text
                 ┌─────────────────────────┐
                 │      Web Browser        │
                 │     HTML / CSS / JS     │
                 └────────────┬────────────┘
                              │ HTTP
                 ┌────────────▼────────────┐
                 │       Flask App         │
                 │ Pages and REST APIs     │
                 └──────┬──────────┬───────┘
                        │          │
              ┌─────────▼───┐  ┌───▼────────────────┐
              │   SQLite    │  │   Floci S3 / SNS   │
              │ Events and  │  │ Banner storage and │
              │ Subscribers │  │ event notifications│
              └─────────────┘  └────────────────────┘
                                       ▲
                              ┌────────┴────────┐
                              │    Terraform    │
                              │ Infrastructure  │
                              │       as Code   │
                              └─────────────────┘
```

### Request flow

1. A user opens the event website.
2. Flask retrieves event information from SQLite and renders the page.
3. An administrator submits an event and may upload a banner image.
4. The banner is uploaded to the local S3-compatible service.
5. The event details and banner URI are saved in SQLite.
6. The application attempts to publish an event announcement through the local SNS topic.
7. Pytest verifies important application behaviours, including event creation and the notification call.

**Note:** The SNS automated test uses a mocked publisher. It verifies that event creation invokes the notification function; it does not prove that an external subscriber received a message.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application and REST API |
| SQLite | Persistent local data storage |
| HTML, CSS, JavaScript | Frontend interface |
| Boto3 | Python client for S3-compatible and SNS services |
| Floci | Local cloud-service emulation |
| Terraform | Infrastructure as Code |
| Docker | Runs the local Floci environment |
| Pytest | Automated application testing |
| Git and GitHub | Version control and source-code hosting |

## 📂 Project Structure

```text
Event-Announcement-System/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── s3_storage.py
│   ├── sns_notifications.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
├── tests/
│   └── test_app.py
├── terraform/
│   ├── provider.tf
│   ├── s3.tf
│   ├── sns.tf
│   └── .terraform.lock.hcl
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

The SQLite database is created locally and is intentionally excluded from Git. Terraform state and plan files are also excluded.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or later
- Git
- Docker
- Terraform
- AWS CLI
- Floci running locally on port `4566`

### 1. Clone the repository

```bash
git clone https://github.com/ireddysachin/event-announcement-system.git
cd event-announcement-system
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Floci

Ensure your Floci container is running and healthy:

```bash
docker ps --filter name=floci
```

The application and Terraform configuration should use the local endpoint `http://localhost:4566` for supported services.

### 5. Initialise and validate Terraform

```bash
terraform -chdir=terraform init
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

Review the plan before applying it. These configuration files are intended for local Floci use; verify the provider endpoints before running Terraform.

To apply the local infrastructure:

```bash
terraform -chdir=terraform apply
```

Confirm the prompt only after checking that the configuration targets Floci rather than real AWS.

### 6. Run the application

From the project root:

```bash
python app/app.py
```

Open the application in your browser:

**http://127.0.0.1:5000**

If port 5000 is already occupied, reuse the running Flask server or stop the existing process before starting another.

## 🧪 Automated Testing

Run the test suite from the project root:

```bash
pytest -q
```

**Last verified result: 10 tests passed.**

The tests cover important application behaviour such as page loading, health checks, subscriptions, event creation, duplicate handling, and invocation of the SNS notification function.

The SNS publishing test uses a mock, so it does not require a real SNS account or a delivered notification.

## 🔌 API Overview

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Display the event website |
| `/health` | GET | Check application health |
| `/api/events` | GET | Retrieve event information |
| `/api/events` | POST | Create an event |
| `/api/banners` | POST | Upload an event banner |
| `/banners/<filename>` | GET | Retrieve a stored banner through Flask |

The subscription endpoint is also implemented in the application. Refer to `app/app.py` for its exact route and request format.

## 🔐 Local Development and Safety

This project is designed to practise cloud-service integration without intentionally creating billable AWS resources.

- Configure Terraform to use the local Floci endpoint.
- Use dummy credentials only for local emulation.
- Do not commit `.env` files or real cloud credentials.
- Keep Terraform state and plan files out of version control.
- Keep the local SQLite database out of version control.
- Review Terraform plans before applying changes.

**Important:** A local configuration is not automatically safe if its provider endpoints are changed. Always verify the endpoints before running Terraform.

## 🔄 CI/CD Roadmap

The current project includes application tests and Terraform configuration. GitHub Actions automation remains a future enhancement unless a workflow is added and verified.

Planned improvements:

1. Configure GitHub Actions to run pytest on pushes and pull requests.
2. Add automated Terraform formatting and validation checks.
3. Improve banner content validation and error handling.
4. Add stronger notification tests.
5. Document the complete local setup with screenshots and troubleshooting steps.

## 🎯 Interview Explanation

**Project summary:**

“I built an Event Announcement System using Python and Flask. It stores event and subscriber data in SQLite and supports event creation through a web interface and REST API. I integrated a local S3-compatible service through Boto3 to store banner images and used an SNS topic to publish event announcements. Terraform manages the local infrastructure, while Pytest checks the application's behaviour. I use Floci to practise AWS-compatible service integration locally and avoid intentionally deploying billable resources to AWS.”

### Key interview topics

- Why did you use Terraform instead of creating resources manually?
- How does the application upload and retrieve banner images?
- How does the Flask application invoke SNS?
- How do you test notifications without publishing a real message?
- How do you isolate the test database from development data?
- How do you prevent Terraform state and plan files from being committed?
- How would you implement CI/CD using GitHub Actions?

## 👨‍💻 Author

**Sachin S. Ireddy**

GitHub: [@ireddysachin](https://github.com/ireddysachin)

---

<p align="center">
  ⭐ If you find this project useful, consider giving the repository a star!
  <br>
  <strong>Built with Python • Flask • SQLite • Terraform • Floci</strong>
</p>
