pipeline {
    agent any
    environment {
        IMAGE_NAME = 'sentiment-ai'
        REGISTRY = 'ghcr.io/VOTRE_PSEUDO' // Remplacez par votre pseudo
        IMAGE_TAG = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }
    stages {
        stage ('Checkout') {
            steps {
                checkout scm
            }
        }
        stage ('Lint') {
            steps {
                sh """
                docker run --rm \
                -v ${WORKSPACE}:${WORKSPACE} \
                -w ${WORKSPACE} \
                python:3.12-slim \
                sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100 --ignore=W292"
                """
            }
        }
        stage ('IaC Validate') {
            steps {
                dir('infra') {
                    sh 'terraform init -backend=false -input=false'
                    sh 'terraform fmt -check'
                    sh 'terraform validate'
                }
            }
        }
        stage ('Build & Test') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                docker rm -f test-runner 2>/dev/null || true
                docker run -e CI=true --name test-runner \
                ${IMAGE_NAME}:${IMAGE_TAG} \
                pytest tests/ -v --cov=src \
                --cov-report=xml:/tmp/coverage.xml \
                --cov-fail-under=70
                """
                script {
                    sh "docker cp test-runner:/tmp/coverage.xml ./coverage.xml 2>/dev/null || true"
                    sh "docker rm -f test-runner 2>/dev/null || true"
                }
            }
        }
        stage ('SonarQube Analysis') {
            environment { SONARQUBE_TOKEN = credentials('sonar-token') }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    docker run --rm --network cicd-network -v ${WORKSPACE}:${WORKSPACE} \
                    -w "${WORKSPACE}" \
                    -e SONAR_HOST_URL="${SONAR_HOST_URL}" \
                    -e SONAR_TOKEN="${SONARQUBE_TOKEN}" \
                    sonarsource/sonar-scanner-cli:latest \
                    sonar-scanner -Dsonar.projectKey=sentiment-ai \
                    -Dsonar.sources=src \
                    -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }
        stage ('Quality Gate') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage ('Push') {
            when { branch 'main' }
            steps {
                withCredentials ([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'REGISTRY_USER',
                    passwordVariable: 'REGISTRY_PASS'
                )]) {
                    sh "echo $REGISTRY_PASS | docker login ghcr.io -u $REGISTRY_USER --password-stdin"
                    sh "docker push $REGISTRY/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
        stage ('IaC Apply') {
            when { branch 'main' }
            steps {
                dir('infra') {
                    sh 'terraform init -input=false'
                    sh "terraform apply -auto-approve -var='image_tag=${IMAGE_TAG}'"
                }
            }
        }
        stage ('Deploy Staging') {
            when { branch 'main' }
            steps {
                sh 'curl -f http://localhost:8001/health || exit 1'
            }
        }
        stage ('Notification') {
            steps {
                echo "Pipeline OK, ${IMAGE_TAG} déployé"
            }
        }
    }
    post {
        always { sh 'docker compose down -v 2>/dev/null || true' }
        failure { echo 'Pipeline KO' }
    }
}