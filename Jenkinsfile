pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'dn070017/cicd_practice'
        GIT_HASH = "${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            when {
                anyOf {
                    changeRequest()
                    triggeredBy 'UserIdCause'
                }
            }
            steps {
                script {
                    echo "Starting build for PR with Git Hash: ${GIT_HASH}"

                    // 1. Build the image using the develop environment arg
                    sh "docker build --build-arg BUILD_ENV=develop -t ${DOCKERHUB_REPO}:${GIT_HASH} ."

                    // 2. Run tests (poetry run tox) inside the container
                    // Note: Using the same tag created in the build step
                    sh "docker run --rm ${DOCKERHUB_REPO}:${GIT_HASH} poetry run tox"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up local images...'
            sh "docker rmi ${DOCKERHUB_REPO}:${GIT_HASH} || true"
        }
        failure {
            echo 'Pipeline failed. Please check the Tox logs for multi-omics or imaging component errors.'
        }
    }
}
