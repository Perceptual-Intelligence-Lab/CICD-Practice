pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'dn070017/cicd_practice'
        GIT_HASH = "${env.GIT_COMMIT?.take(7) ?: 'unknown'}"
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
                    // Get commit hash at the start
                    def gitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.GIT_HASH = gitHash

                    echo "Starting build for PR with Git Hash: ${env.GIT_HASH}"

                    // 1. Build the image using the develop environment arg
                    sh """
                        docker build --build-arg BUILD_ENV=develop \
                                     --cache-from ${DOCKERHUB_REPO}:develop \
                                     -t ${DOCKERHUB_REPO}:${env.GIT_HASH} \
                                     -t ${DOCKERHUB_REPO}:develop .
                    """

                    // 2. Run tests
                    sh "docker run --rm ${DOCKERHUB_REPO}:${env.GIT_HASH} poetry run tox"
                }
            }
        }

        stage('Manual Approval') {
            when {
                anyOf {
                    changeRequest()
                    triggeredBy 'UserIdCause'
                }
            }
            steps {
                script {
                    echo "✅ Tests passed for commit ${env.GIT_HASH}"
                    echo "Docker image ready: ${DOCKERHUB_REPO}:${env.GIT_HASH}"
                    echo '⏰ You have 1 hour to approve...'

                    // Manual approval - will pause and wait for user input
                    timeout(time: 1, unit: 'HOURS') {
                        input(
                            message: 'Push image to DockerHub?',
                            ok: 'Push',
                            submitter: 'admin,dn070017'
                        )
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            when {
                anyOf {
                    changeRequest()
                    triggeredBy 'UserIdCause'
                }
            }
            steps {
                script {
                    echo 'Pushing image to DockerHub...'

                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                            docker push ${DOCKERHUB_REPO}:${env.GIT_HASH}
                            docker push ${DOCKERHUB_REPO}:develop
                            docker logout
                        """
                    }
                    echo "✅ Successfully pushed ${DOCKERHUB_REPO}:${env.GIT_HASH}"
                    echo "✅ Successfully pushed ${DOCKERHUB_REPO}:develop"
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'Cleaning up local images...'
                sh """
                    docker rmi ${DOCKERHUB_REPO}:${env.GIT_HASH} || true
                    docker rmi ${DOCKERHUB_REPO}:develop || true
                """
            }
        }
        success {
            echo "✅ Pipeline completed successfully for commit ${env.GIT_HASH}"
        }
        failure {
            echo "❌ Pipeline failed for commit ${env.GIT_HASH}"
            echo 'Please check the logs above for errors.'
        }
        aborted {
            echo '⚠️ Pipeline was aborted (push to DockerHub was cancelled)'
        }
    }
}
