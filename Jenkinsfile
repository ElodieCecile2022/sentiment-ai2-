pipeline {
    agent any
    
    environment {
        // Remplacez par vos propres valeurs
        IMAGE_NAME = 'sentiment-ai'
        IMAGE_TAG = 'latest'
        REGISTRY = 'votre-registre' // Modifiez selon votre registre
    }

    stages {
        stage('Build') {
            steps {
                echo 'Construction de l\'image Docker...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                waitForQualityGate abortPipeline: true
            }
        }

        stage('Security Scan (Trivy)') {
            steps {
                echo 'Analyse de sécurité avec Trivy...'
                sh """
                    docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v trivy-cache:/root/.cache/trivy \
                    aquasec/trivy:latest image \
                    --severity HIGH,CRITICAL \
                    --exit-code 1 \
                    --format table \
                    ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
            post {
                failure {
                    echo 'Vulnérabilités détectées par Trivy ! Arrêt du pipeline.'
                }
            }
        }

        stage('Push') {
            steps {
                echo 'Envoi de l\'image vers le registre...'
            }
        }

        stage('Deploy Staging') {
            when { 
                branch 'main' 
            }
            steps {
                echo "Déploiement de ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} en staging ..."
                sh """
                    # Arrêter le staging précédent proprement
                    docker compose -f docker-compose.yml -p staging down 2>/dev/null || true

                    # Démarrer la nouvelle version
                    docker compose -f docker-compose.yml -p staging up -d

                    echo "Staging disponible sur http://localhost:8001"
                """
            }
        }
    }
}