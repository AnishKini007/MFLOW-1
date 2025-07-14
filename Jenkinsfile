pipeline {
    agent any
    stages {
        stage('Git Checkout') {
            steps {
                script {
                    echo 'Checking out code...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/AnishKini007/MFLOW-1.git']])
                }
                
            }
        }
    }
}