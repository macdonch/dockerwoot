podTemplate(
    name: 'jenkins-docker',
    label: 'jenkins-docker',
    containers: [
        containerTemplate(name: 'jenkins-docker', image:'leibniz9999/jenkins-docker-client-lab'),
    ],
    volumes: [
        hostPathVolume(mountPath: '/var/run/docker.sock',
        hostPath: '/var/run/docker.sock'),
    ],
    {
        //node = the pod label
        node('jenkins-docker') {
            def secrets = [
                [path: 'secret/jenkins/harbor', engineVersion: 2, secretValues: [
                [envVar: 'HARBOR_USER', vaultKey: 'user'],
                [envVar: 'HARBOR_TOKEN', vaultKey: 'password']]],
            ]
            def configuration = [vaultUrl: 'http://vault.corp.sidclab',  vaultCredentialId: 'vault-approle', engineVersion: 2]

            def app

            def registryCredential = 'leibniz9999_id'

            stage('Clone repository') {
                /* repository is defined in the Jenkins pipeline */

                checkout scm
            }

            stage('Build Docker Image') {
                //container = the container label
                container('docker') {
                    // This is where we build the Docker image

                    dir('web') {
                        app = docker.build("leibniz9999/dockerwoot")
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
                    /*
                    docker.withRegistry('', registryCredential) {
                        app.push("latest")
                    }
                    */

                    /* can't use an insecure registry, so this doesn't work  with harbor and a self-signed cert */
                    /* custom image has insecure harbor added */
                    withVault([configuration: configuration, vaultSecrets: secrets]) {
                        dir ('web') {

                            sh "docker login --username '${env.HARBOR_USER}' --password ${env.HARBOR_TOKEN} harbor.corp.sidclab && docker push harbor.corp.sidclab/hybridbuild/dockerwoot:latest"
                        }
                    }


                }
            }
        }
    }
)