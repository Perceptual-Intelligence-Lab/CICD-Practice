pipeline {
    agent {
        docker {
            image 'docker:27-cli'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    options {
        retry(3)
    }
    environment {
        DOCKERHUB_REPO = 'dn070017/cicd_practice'
        GIT_HASH = "${env.GIT_COMMIT?.take(7) ?: 'unknown'}"
        DOCKER_TAG = "${env.BRANCH_NAME == 'main' ? 'latest' : env.BRANCH_NAME}"
    }
    stages {
        stage('Continuous Integration') {
            stages {
                stage('Checkout') {
                    steps {
                        checkout scm
                    }
                }
                stage('Build') {
                    steps {
                        script {
                            echo "🚀 Building on node: ${env.NODE_NAME}"
                            echo "📦 Branch: ${env.BRANCH_NAME}, Commit: ${env.GIT_HASH}"
                            sh """
                                docker build \
                                    --build-arg BUILD_ENV=${env.BRANCH_NAME?.startsWith('PR-') ? 'develop' : (env.BRANCH_NAME == 'main' ? 'production' : 'develop')} \
                                    --cache-from ${DOCKERHUB_REPO}:${DOCKER_TAG} \
                                    -t ${DOCKERHUB_REPO}:${env.GIT_HASH} \
                                    -t ${DOCKERHUB_REPO}:${DOCKER_TAG} \
                                    .
                            """
                        }
                    }
                }
                stage('Test') {
                    steps {
                        script {
                            echo '🧪 Running tests...'
                            sh "docker run --rm ${DOCKERHUB_REPO}:${env.GIT_HASH} poetry run tox"
                        }
                    }
                }
            }
        }
        stage('Continuous Deployment') {
            when {
                allOf {
                    expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
                    anyOf {
                        branch 'main'
                        branch 'develop'
                    }
                }
            }
            stages {
                stage('Manual Approval') {
                    steps {
                        script {
                            timeout(time: 1, unit: 'HOURS') {
                                input(
                                    message: "✅ CI passed for ${env.GIT_HASH} on '${env.BRANCH_NAME}'. Deploy to DockerHub as '${DOCKER_TAG}'?",
                                    ok: 'Deploy'
                                )
                            }
                        }
                    }
                }
                stage('Push to DockerHub') {
                    steps {
                        script {
                            echo '🐳 Pushing to DockerHub...'
                            withCredentials([usernamePassword(
                                credentialsId: 'dockerhub-credentials',
                                usernameVariable: 'DOCKER_USER',
                                passwordVariable: 'DOCKER_PASS'
                            )]) {
                                sh """
                                    echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                                    docker push ${DOCKERHUB_REPO}:${env.GIT_HASH}
                                    docker push ${DOCKERHUB_REPO}:${DOCKER_TAG}
                                """
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            script {
                if (env.BRANCH_NAME?.startsWith('PR-')) {
                    echo "✅ CI passed for PR ${env.BRANCH_NAME} — ready for review and merge."
                }
            }
        }
        failure {
            script {
                if (env.BRANCH_NAME?.startsWith('PR-')) {
                    echo "❌ CI failed for PR ${env.BRANCH_NAME} — merge blocked."
                }
            }
        }
        always {
            sh 'docker logout || true'
        }
    }
}
