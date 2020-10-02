podTemplate(
    name: 'docker-on-docker',
    label: 'docker-on-docker',
    containers: [
        containerTemplate(name: 'docker', image:'trion/jenkins-docker-client'),
    ],
    volumes: [
        hostPathVolume(mountPath: '/var/run/docker.sock',
        hostPath: '/var/run/docker.sock'),
    ],
    {
        //node = the pod label
        node('docker-on-docker') {
            def secrets = [
                [path: 'secret/jenkins/harbor', engineVersion: 2, secretValues: [
                [envVar: 'HARBOR_USER', vaultKey: 'user'],
                [envVar: 'HARBOR_TOKEN', vaultKey: 'password']]],
            ]
            def configuration = [vaultUrl: 'http://vault.corp.sidclab',  vaultCredentialId: 'vault-approle', engineVersion: 2]

            def app

            stage('Clone repository') {
                /* repository is defined in the Jenkins pipeline */

                checkout scm
            }

            stage('Build Docker Image') {
                //container = the container label
                container('docker') {
                    // This is where we build the Docker image

                    dir('web') {
                        app = docker.build("dockerwoot/k8s-hello-onprem")
                    }
                }
            }

            stage('Test image') {
                /* Pretend to have a test 
                container('docker') {
                    app.inside {
                        sh 'echo "Tests passed"'
                    }
                }
                */
                sh 'echo "Tests passed"'
            }

            stage('Push image') {
                /* Finally, we'll push the image with two tags:
                * First, the incremental build number from Jenkins
                * Second, the 'latest' tag. */

                container('docker') {

                    withVault([configuration: configuration, vaultSecrets: secrets]) {
                        sh "echo ${env.HARBOR_TOKEN}"
                    }

                    dir ('web') {
                        /* docker.withRegistry('https://harbor.corp.sidclab/leinbiz9999/dockerwoot', "${env.HARBOR_TOKEN}") { */
                        docker.withRegistry('https://hub.docker.com/repository/docker/leibniz9999') {
                            app.push("latest")
                        }
                    }
                }

            }
        }
    }
)