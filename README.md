ACEest Fitness & Gym - Automated Deployment Pipeline

This repository contains the backend Flask application for ACEest Fitness & Gym and the required CI/CD configurations for an automated deployment pipeline using Docker, GitHub Actions, and Jenkins.

Project Overview

As part of the DevOps transition, the standalone legacy Python application has been modularized into a RESTful Flask API. The source code is version-controlled, tested via Pytest, containerized using Docker, and integrated into automated pipelines.

Repository Contents

app.py: Core Flask web application.

requirements.txt: Python package dependencies.

test_app.py: Unit tests validating application logic.

Dockerfile: Instructions for containerizing the application.

.github/workflows/main.yml: GitHub Actions pipeline configuration.

Jenkinsfile: Jenkins declarative pipeline configuration.

1. Local Setup and Execution Instructions

Prerequisites

Python 3.9+ installed

Docker installed (optional for local non-containerized testing)

Git

Running the App Locally

Clone the repository:

git clone <repository-url>
cd ACEest-DevOps


Install dependencies:

pip install -r requirements.txt


Run the Flask application:

python app.py


The application will start on http://127.0.0.1:5000/.

Running via Docker

Build the Docker image:

docker build -t aceest-fitness-app .


Run the Docker container:

docker run -p 5000:5000 aceest-fitness-app


2. Running Tests Manually

We use pytest for validating application integrity.

Ensure dependencies are installed.

Run the test suite:

pytest test_app.py -v


This will automatically execute database setup, endpoint tests, data validation, and logic tests (calorie calculations), and print the success/failure outputs to the terminal.

3. High-Level CI/CD Integration Logic

Our continuous integration and continuous delivery (CI/CD) pipelines serve as quality gates.

GitHub Actions

The pipeline is defined in .github/workflows/main.yml. It is triggered automatically on every push or pull_request to the main branch.

Stage 1 (Build & Lint): Sets up Python, installs dependencies, and checks for syntax errors using flake8.

Stage 2 (Automated Testing): Executes pytest to ensure new code does not break existing logic.

Stage 3 (Docker Assembly): If tests pass, it automatically builds the Docker image to verify container portability.

Jenkins Pipeline

Jenkins acts as our primary BUILD and quality gate server. The Jenkinsfile in this repository dictates the steps:

Checkout: Pulls the latest stable code from GitHub.

Dependencies & Linting: Validates code quality on the Jenkins server.

Test: Executes pytest in the build environment.

Docker Image Build: Packages the validated code into a portable Docker image ready for staging/production deployment.