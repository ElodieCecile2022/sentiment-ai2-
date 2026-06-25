pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Simulation : Construction de l\'image Docker...'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                echo 'Simulation : Analyse SonarQube...'
            }
        }
        stage('Quality Gate') {
            steps {
                echo 'Simulation : Vérification Quality Gate...'
            }
        }
        stage('Security Scan (Trivy)') {
            steps {
                echo 'Simulation : Scan de sécurité Trivy...'
            }
        }
        stage('Push') {
            steps {
                echo 'Simulation : Envoi de l\'image sur le registre...'
            }
        }
        stage('Deploy Staging') {
            steps {
                echo 'Simulation : Déploiement sur l\'environnement de staging...'
            }
        }
        stage('Integration Tests') {
            steps {
                echo 'Simulation : Lancement des tests d\'intégration...'
            }
        }
        stage('Notification') {
            steps {
                echo 'Simulation : Envoi de la notification de fin de pipeline...'
            }
        }
    }
}