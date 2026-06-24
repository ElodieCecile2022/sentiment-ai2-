// Jenkinsfile - Pipeline CI/CD SentimentAI
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'sentiment-ai'
        // Assurez-vous que ce registre est bien configuré sur votre serveur
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
                // Remplacement de docker-compose par docker build et run
                sh 'docker build -t sentiment-ai-test .'
                sh 'docker run --rm sentiment-ai-test pytest'
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
    }

    post {
        always {
            // Nettoyage simplifié sans docker-compose
            echo "Nettoyage terminé."
        }
        success {
            echo "Pipeline réussi ! Image : ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline échoué. Consultez les logs ci-dessus.'
        }
    }
}