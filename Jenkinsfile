// Jenkinsfile - Pipeline CI/CD SentimentAI
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'sentiment-ai'
        REGISTRY   = 'ghcr.io/ElodieCecile2022' 
        IMAGE_TAG  = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log --oneline -5'
            }
        }
        stage('Lint') {
            steps {
                sh '''
                    docker run --rm \
                    --volumes-from jenkins \
                    -w $WORKSPACE \
                    python:3.12-slim \
                    sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100 || true"
                '''
            }
        }

        stage('Build & Test') {
            steps {
                sh 'docker compose build'
                sh 'docker compose run --rm app pytest'
            }
            post {
                failure {
                    echo 'Tests échoués ou coverage insuffisant.'
                }
            }
        }

        stage('Push') {
            when { branch 'main' }
            steps {
                echo "Construction et envoi de l'image..."
                sh 'docker build -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}'
            }
        }
    } // <-- Ajoutée ici pour fermer le bloc stages

    post {
        always {
            sh 'docker compose down -v 2>/dev/null || true'
        }
        success {
            echo "Pipeline réussi ! Image : ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline échoué. Consultez les logs ci-dessus.'
        }
    }
}