pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
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
    }
}
                
            }
        }
    }
}