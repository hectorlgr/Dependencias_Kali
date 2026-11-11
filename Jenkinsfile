pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        PIPENV_VENV_IN_PROJECT = '1'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Preparando proyecto Flask'
                sh 'python3 -m compileall -q app.py'
            }
        }

        stage('Dependency Management') {
            steps {
                echo 'Verificando dependencias'
                sh 'pipenv verify'
                sh 'pipenv sync --dev'
                sh 'pipenv graph'
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas unitarias'
                sh 'pipenv run python -m pytest -q'
            }
        }

        stage('Analyze') {
            steps {
                echo 'Analizando codigo y dependencias'
                sh 'pipenv run bandit -q app.py'
                sh 'pipenv requirements > auditoria-requirements.txt'
                sh 'pipenv run pip-audit -r auditoria-requirements.txt'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy simulado correctamente'
            }
        }
    }

    post {
        always {
            archiveArtifacts(
                artifacts: 'auditoria-requirements.txt',
                allowEmptyArchive: true
            )
        }

        failure {
            echo 'ALERTA: revisar errores del pipeline'
        }

        success {
            echo 'Pipeline finalizado correctamente'
        }
    }
}
