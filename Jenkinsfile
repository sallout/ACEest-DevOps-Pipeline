pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aceest-fitness-app:latest"
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
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Lint Code') {
            steps {
                sh 'flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
            }
        }

        stage('Test') {
            steps {
                // Run pytest to validate internal logic
                sh 'pytest test_app.py -v'
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