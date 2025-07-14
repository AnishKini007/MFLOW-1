pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = "rich-operand-465008-m0"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin/"
    }
    stages {
        stage('Git Checkout') {
            steps {
                script {
                    echo 'Checking out code...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/AnishKini007/MFLOW-1.git']])
                }
                
            }
        }
        stage('Setup Virtual Environment and Install Dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment...'
                    sh'''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
        stage('Building and pushing docker Image to GCR') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        script {
                            echo 'Building and pushing Docker image to GCR...'
                            sh '''
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet
                            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                            docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                            '''
                        }
                    }
                }
            }
        }
    }
}