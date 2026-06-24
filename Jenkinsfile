pipeline {
    agent any
    environment {
        IMAGE_NAME = 'sentiment-ai'
        IMAGE_TAG = 'latest'
        SONARQUBE_TOKEN = credentials('sonar-token')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Lint') {
            steps {
                sh 'flake8 src/'
            }
        }
        stage('Build & Test') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                docker rm -f test-runner 2>/dev/null || true
                set +e
                docker run \\
                    -e CI=true \\
                    --name test-runner \\
                    ${IMAGE_NAME}:${IMAGE_TAG} \\
                    pytest tests/ -v \\
                    --cov=src \\
                    --cov-report=xml:/tmp/coverage.xml \\
                    --cov-report=term-missing \\
                    --cov-fail-under=70
                TEST_EXIT_CODE=\$?
                set -e
                docker cp test-runner:/tmp/coverage.xml ./coverage.xml 2>/dev/null || true
                docker rm -f test-runner 2>/dev/null || true
                exit \$TEST_EXIT_CODE
                """
            }
            post {
                failure { echo 'Tests échoués ou coverage insuffisant (< 70%)' }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    docker run --rm \\
                        --network cicd-network \\
                        --volumes-from jenkins \\
                        -w "\$WORKSPACE" \\
                        -e SONAR_HOST_URL="\$SONAR_HOST_URL" \\
                        -e SONAR_TOKEN="\$SONARQUBE_TOKEN" \\
                        sonarsource/sonar-scanner-cli:latest \\
                        sonar-scanner \\
                        -Dsonar.projectKey=sentiment-ai \\
                        -Dsonar.projectName=SentimentAI \\
                        -Dsonar.projectBaseDir="\$WORKSPACE" \\
                        -Dsonar.sources=src \\
                        -Dsonar.python.version=3.11 \\
                        -Dsonar.python.coverage.reportPaths=coverage.xml \\
                        -Dsonar.sourceEncoding=UTF-8 \\
                        -Dsonar.scanner.metadataFilePath=\$WORKSPACE/report-task.txt
                    """
                }
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Security Scan') {
            steps {
                sh """
                docker run --rm \\
                    -v /var/run/docker.sock:/var/run/docker.sock \\
                    -v trivy-cache:/root/.cache/trivy \\
                    aquasec/trivy:latest image \\
                    --severity HIGH,CRITICAL \\
                    --exit-code 1 \\
                    --format table \\
                    "${IMAGE_NAME}:${IMAGE_TAG}"
                """
            }
        }
        stage('Push') {
            when { branch 'main' }
            steps {
                echo "Push de l'image vers le registre..."
            }
        }
        stage('Deploy Staging') {
            when { branch 'main' }
            steps {
                sh """
                docker compose -f docker-compose.yml -p staging down 2>/dev/null || true
                docker compose -f docker-compose.yml -p staging up -d
                """
                echo "Staging disponible sur http://localhost:8001"
            }
        }
    }
}