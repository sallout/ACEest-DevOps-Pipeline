# ACEest Fitness & Gym - Automated Deployment Pipeline

## Project Overview

As part of the DevOps transition, the standalone legacy Python application has been modularized into a RESTful Flask API. The source code is version-controlled, tested via Pytest, containerized using Docker, and integrated into automated pipelines.

---

## Repository Contents

* **app.py**: Core Flask web application
* **requirements.txt**: Python package dependencies
* **test_app.py**: Unit tests validating application logic
* **Dockerfile**: Instructions for containerizing the application
* **.github/workflows/main.yml**: GitHub Actions pipeline configuration
* **Jenkinsfile**: Jenkins declarative pipeline configuration
* **screenshots/**: Proof of successful local Jenkins pipeline execution

---

## 1. Local Setup and Execution Instructions

### Prerequisites

* Python 3.9+ installed
* Docker installed
* Git installed

### Running the App Locally

**Clone the repository:**

```bash
git clone https://github.com/sallout/ACEest-DevOps-Pipeline.git
cd ACEest-DevOps-Pipeline
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run the Flask application:**

```bash
python app.py
```

The application will start on:
http://127.0.0.1:5000/

---

## Running via Docker

**Build the Docker image:**

```bash
docker build -t aceest-fitness-app .
```

**Run the Docker container:**

```bash
docker run -p 5000:5000 aceest-fitness-app
```

---

## 2. Running Tests Manually

We use **pytest** for validating application integrity.

Ensure dependencies are installed, then run:

```bash
pytest test_app.py -v
```

This will automatically execute:

* Database setup
* Endpoint tests
* Data validation
* Logic tests (calorie calculations)

Results will be printed in the terminal.

---

## 3. High-Level CI/CD Integration Logic

Our continuous integration and continuous delivery (CI/CD) pipelines serve as quality gates.

### GitHub Actions

The pipeline is defined in `.github/workflows/main.yml`.
It is triggered automatically on every **push** or **pull_request** to the `main` branch.

**Stages:**

1. **Build & Lint**

   * Sets up Python
   * Installs dependencies
   * Runs `flake8` for syntax checking

2. **Automated Testing**

   * Executes `pytest`
   * Ensures no regressions

3. **Docker Assembly**

   * Builds Docker image
   * Verifies container portability

---

### Jenkins Pipeline

Jenkins acts as the primary **build and quality gate server**.

Defined in the `Jenkinsfile`:

**Stages:**

1. **Checkout**

   * Pulls latest code from repository

2. **Dependencies & Linting**

   * Installs dependencies
   * Validates code quality in a Python virtual environment

3. **Test**

   * Runs `pytest`

4. **Docker Image Build**

   * Builds production-ready Docker image

---

## 4. Proof of Execution (Jenkins)

The following screenshots demonstrate successful execution of the Jenkins pipeline in a local environment.

* Pipeline Overview
* Console Output (Docker Build Success)
