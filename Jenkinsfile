pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aceest-fitness-app:latest"
        // Add Homebrew and Docker paths so Jenkins can find the 'docker' command on Macs
        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls code from the GitHub repository
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // Use python3 to create a virtual environment to avoid macOS restrictions
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Lint Code') {
            steps {
                sh './venv/bin/flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
            }
        }

        stage('Test') {
            steps {
                // Run pytest to validate internal logic using the virtual environment
                sh './venv/bin/pytest test_app.py -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the image after passing tests
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo "Jenkins Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}