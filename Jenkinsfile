// Jenkinsfile - Pipeline CI/CD SentimentAI
pipeline {
    agent any // s'exécute sur n'importe quel agent disponible

    environment {
        IMAGE_NAME = 'sentiment-ai'
        // REMPLACEZ 'VOTRE_PSEUDO' CI-DESSOUS
        REGISTRY   = 'ghcr.io/VOTRE_PSEUDO' 
        
        // Chaque build produit une image taguée de façon unique et traçable
        IMAGE_TAG  = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }

    stages {
        // Les 4 stages seront définis ici
        stage('Checkout') {
            steps {
                checkout scm
                echo "Branche : ${env.BRANCH_NAME}"
                echo "Commit  : ${env.GIT_COMMIT}"
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
                    sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"
                '''
            }
        }
        stage('Build & Test') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh """
                    docker run --rm \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    pytest tests/ -v \
                    --cov=src \
                    --cov-report=xml:coverage.xml \
                    --cov-report=term-missing \
                    --cov-fail-under=70
                """
            }
            stage('Push') {
            when { branch 'main' }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token', 
                    usernameVariable: 'REGISTRY_USER', 
                    passwordVariable: 'REGISTRY_PASS'
                )]) {
                    sh """
                        echo \$REGISTRY_PASS | docker login ghcr.io -u \$REGISTRY_USER --password-stdin
                        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:latest
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
            post {
                failure {
                    echo 'Tests échoués ou coverage insuffisant (< 70%)'
                }
            }
        }
        stage('Build') {
            steps {
                echo "Construction de l'image..."
                sh 'docker build -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }
        // Ajoutez vos autres stages (Test, Push, etc.) ici
    }

    post {
        always {
            // Nettoyer les conteneurs de test, qu'il y ait succès ou échec
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