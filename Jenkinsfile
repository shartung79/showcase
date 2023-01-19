pipeline{
    agent any
    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }
    environment{ 
        registry = "https://esp-cr.artifactory.lsyesp-app.dlh.de/harding-showcase/hello-world"
        registryCredential = 'ARTIFACTORY_ACCESS'        
    }
    stages{
        stage('Building image') {
            steps{
                script {
                    dockerImage = docker.build registry + ":0.$BUILD_NUMBER"
                }
            }
        }
        stage('Deploy Image') {
            steps{
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
    }
}