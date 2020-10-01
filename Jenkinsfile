node {
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

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        /*  dockerfile is in the web directory of the repo */

        /*
        dir ('web') {
            app = docker.build("dockerwoot/k8s-hello-onprem")
        }
        */
        app = docker.build("dockerwoot/k8s-hello-onprem")

    }

    stage('Test image') {
        /* Pretend to have a test */

        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag. */
        steps {
            withVault([configuration: configuration, vaultSecrets: secrets]) {
            sh "echo ${env.HARBOR_TOKEN}"
            }

            docker.withRegistry('https://harbor.corp.sidclab', ${env.HARBOR_TOKEN}) {
                app.push("${env.BUILD_NUMBER}")
                app.push("latest")
            }
        }
    }
}