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
        echo 'Construyendo imagen Docker...'

        sh 'docker build -t proyecto-flask-lab:latest .'

        echo 'Desplegando aplicacion Flask...'

        sh '''
            docker rm -f proyecto-flask-lab \
                >/dev/null 2>&1 || true

            docker run -d \
                --name proyecto-flask-lab \
                --restart unless-stopped \
                -p 127.0.0.1:5001:5000 \
                proyecto-flask-lab:latest
        '''

        echo 'Verificando que Flask responda...'

        sh '''
            for i in 1 2 3 4 5 6 7 8 9 10; do
                if docker exec proyecto-flask-lab python -c \
                    "import urllib.request; r=urllib.request.urlopen('http://127.0.0.1:5000/', timeout=3); assert r.status == 200"; then
                    echo 'Aplicacion desplegada correctamente: HTTP 200'
                    exit 0
                fi
                sleep 2
            done

            docker logs proyecto-flask-lab
            exit 1
        '''
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
