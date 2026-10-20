# 🚀 Event Announcement System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Tests-8_Passing-brightgreen?logo=pytest" alt="Tests">
  <img src="https://img.shields.io/badge/Infrastructure-Terraform-7B42BC?logo=terraform&logoColor=white" alt="Terraform">
</p>

<p align="center">
  <strong>A modern event announcement web application built with Python, Flask, and SQLite.</strong>
  <br>
  Discover events, create announcements, and subscribe for updates.
</p>

---

## 🌟 About the Project

The **Event Announcement System** is a web application that helps users discover upcoming technical events and subscribe for announcements. Administrators can create events through a simple web interface.

This project is also a hands-on learning journey into DevOps practices, automated testing, Infrastructure as Code, and CI/CD.

## ✨ Key Features

<table>
  <tr>
    <td width="50%">
      <h3>📅 Event Management</h3>
      View upcoming events with dates, locations, and descriptions.
    </td>
    <td width="50%">
      <h3>➕ Create Events</h3>
      Add new events through an administrator form.
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>📧 Email Subscription</h3>
      Allow users to subscribe and prevent duplicate subscriptions.
    </td>
    <td width="50%">
      <h3>🗄️ Persistent Storage</h3>
      Store event and subscriber information in SQLite.
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🧪 Automated Testing</h3>
      Validate application behaviour using pytest.
    </td>
    <td width="50%">
      <h3>⚙️ DevOps Learning</h3>
      Prepare for Terraform, Floci, and CI/CD integration.
    </td>
  </tr>
</table>

## 🛠️ Technology Stack

| Technology | Role |
|:---|:---|
| 🐍 **Python** | Backend programming |
| ⚡ **Flask** | Web application and REST API |
| 🗃️ **SQLite** | Local database |
| 🎨 **HTML, CSS, JavaScript** | Frontend development |
| 🧪 **pytest** | Automated testing |
| 🌿 **Git & GitHub** | Version control and collaboration |
| 🏗️ **Terraform** | Infrastructure as Code — planned integration |
| ☁️ **Floci** | Local cloud-service emulation — planned integration |
| 🔄 **GitHub Actions** | CI/CD automation — planned integration |

## 🖥️ Application Preview

The application includes an upcoming-events page, an event creation form, and an email subscription form.

> Add a screenshot of your running application here to showcase the interface on GitHub.

<!-- After adding a screenshot, replace this comment with:
<p align="center">
  <img src="docs/images/event-announcement-preview.png" width="850" alt="Event Announcement System preview">
</p>
-->

## 📂 Project Structure

```text
Event-Announcement-System/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── events.db
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
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or later
- Git
- Visual Studio Code (recommended)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/ireddysachin/event-announcement-system.git
cd event-announcement-system
```

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start the application

```bash
python app/app.py
```

Open your browser at:

**http://127.0.0.1:5000**

If port 5000 is already occupied, stop the previous Flask server before starting another instance.

## 🧪 Run the Tests

Run the automated test suite:

```bash
python -m pytest -v
```

**Current result:** 8 tests passing ✅

The tests cover application routes, event creation, event retrieval, subscription behaviour, and duplicate-event handling.

## 🔌 API Overview

| Endpoint | Purpose |
|:---|:---|
| `GET /` | Display the web application |
| `GET /health` | Check application health |
| `GET /api/events` | Retrieve events |
| `POST /api/events` | Create an event |

The subscription endpoint is implemented in the Flask application. Check `app/app.py` for its exact route and supported request method.

## 🏗️ Architecture & DevOps Roadmap

The current application uses Flask for request handling and SQLite for local persistence.

**Planned development stages:**

1. ✅ Build the web interface and Flask backend.
2. ✅ Implement event and subscriber database operations.
3. ✅ Add automated tests using pytest.
4. ✅ Initialise Git and publish the repository to GitHub.
5. 🔜 Add and validate Terraform configuration for local infrastructure.
6. 🔜 Integrate supported Floci services.
7. 🔜 Configure GitHub Actions for automated testing.
8. 🔜 Document the final architecture and deployment workflow.

*The roadmap reflects the current development status; planned integrations are not yet claimed as completed.*

## 🎯 Learning Objectives

- Develop a Python web application using Flask.
- Build and test REST API endpoints.
- Work with SQLite and database operations.
- Write automated tests with pytest.
- Manage source code using Git and GitHub.
- Learn Infrastructure as Code with Terraform.
- Explore local cloud-service emulation with Floci.
- Implement CI/CD workflows with GitHub Actions.

## 👨‍💻 Author

**Sachin S. Ireddy**

🔗 **GitHub:** [ireddysachin](https://github.com/ireddysachin)

---

<p align="center">
  ⭐ If you find this project useful, consider giving the repository a star!
  <br>
  <strong>Built with Python • Flask • SQLite • DevOps</strong>
</p>
