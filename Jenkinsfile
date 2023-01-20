pipeline {
  agent {
    kubernetes {
      yaml """
        apiVersion: v1
        kind: Pod
        metadata:
          labels:
            build: true
        spec:
          containers:
          - name: kaniko
            image: gcr.io/kaniko-project/executor:v1.8.1-debug
            command:
            - /busybox/cat
            shell:
            - /busybox/sh
            tty: true
          - name: prov-tools
            image: isb.docker.vmh-aiapd-testenv.lic.fra.dlh.de/isb/provisioning-tools:1.6
            command:
            - cat
            tty: true
          - name: grype
            image: isb.docker.vmh-aiapd-testenv.lic.fra.dlh.de/isb/grype:0.46
            command:
            - cat
            tty: true
          - name: jfrog-cli
            image: releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf:2.16.4
            tty: true
            command:
            - cat
            shell:
            - sh
        """
    }
  }

  options {
    timestamps()
    ansiColor("xterm")
  }

  environment {
    ENV = "dev"
    APPNAME = "helloworld-flask"
    REGISTRY = "esp-cr.artifactory.lsyesp.app.dlh.de"
    REGISTRY_CRED = credentials('CONTAINER_REPO')
    AUTH_FILE = credentials('CONTAINER_REPO_JSON')
    IMAGE = "${REGISTRY}/showcase-harding/${APPNAME}"
    TAG = sh(script: "git describe --tags | sed 's/\\(.*\\)-.*/\\1/'", returnStdout: true).trim()
    PROXY_CRED = credentials('PROXY_CREDENTIALS')
    PROXY = "http://${PROXY_CRED_USR}:${PROXY_CRED_PSW}@prx-fralh-v01.sec.fra.dlh.de:8080"
    http_proxy = "${PROXY}"
    https_proxy = "${PROXY}"
    NO_PROXY = "127.0.0.1,localhost,.dlh.de,.lhsystems.int"
    SC_HOME = tool "LSYESP SonarQubeScanner 4.6.2.2472"
    SC_PROJECTKEY = "ISB_PYTHON_EXAMPLE"
    SC_APIKEY = "94ecc870417cd069aa66104d712f8b896eeee009"
  }
  
  stages {
    // stage('SonarQube analysis') {
    //   steps {
    //     ws('.') {
    //       withSonarQubeEnv('LSYESP SonarQube') {
    //         sh """
    //           #!/usr/bin/env bash
    //           ${SC_HOME}/bin/sonar-scanner -X \
    //           -Dsonar.projectKey=${SC_PROJECTKEY} \
    //           -Dsonar.projectName=isb-python-example \
    //           -Dsonar.projectVersion=0.1 \
    //           -Dsonar.sources=/home/jenkins/agent/workspace/twgf/LSY/python-example/src \
    //           -Dsonar.sourceEncoding=UTF-8 \
    //           -Dsonar.login=${SC_APIKEY}
    //         """
    //         slackSend channel: "lsy-esp-cicd-poc", color: "#0DADEA", message: "SonarQube #${env.BUILD_NUMBER} of ${env.JOB_NAME}\nSourcecode has been scanned by SonarCube:\ncheck URL: https://dev.k8s.private.lsyesp.app.dlh.de/sonar/dashboard?id=${SC_PROJECTKEY}"
    //       }
    //     }
    //   }
	//   }

    // stage('Parse SonarQube result') {
    //   steps {
    //     container('prov-tools') {
    //       script {
    //         def res = sh(returnStdout: true, script: """
    //           curl -ks 'https://dev.k8s.private.lsyesp.app.dlh.de/sonar/api/project_analyses/search?project=${SC_PROJECTKEY}&category=QUALITY_GATE' -u ${SC_APIKEY}: |jq '.analyses[0].events[0].name' |cut -d \\" -f2
    //         """)
    //         if (res.contains('Failed')) {
    //           slackSend channel: "lsy-esp-cicd-poc", color: "#FF0000", message: ":exclamation: SonarQube #${env.BUILD_NUMBER} of ${env.JOB_NAME}\nYour code failed the Quality Gate of SonarQube\ncheck result: https://dev.k8s.private.lsyesp.app.dlh.de/sonar/dashboard?id=${SC_PROJECTKEY}"
    //         } else {
    //           slackSend channel: "lsy-esp-cicd-poc", color: "#18BE52", message: ":white_check_mark: SonarQube #${env.BUILD_NUMBER} of ${env.JOB_NAME}\nYour code is good according to SonarQube\ncheck result: https://dev.k8s.private.lsyesp.app.dlh.de/sonar/dashboard?id=${SC_PROJECTKEY}"
    //         }
    //       }
    //     }
    //   }
	//   }

//    stage('delete docker image tagged LATEST') {
//      steps {
//        container('jfrog-cli') {
//          script {
//            sh (
//              """jf rt del --insecure-tls \
//              --recursive=false --quiet --exclusions=*_uploads \
//              --sort-by=created --sort-order=desc --offset 0 \
//              --url=https://vmh-aiapd-testenv.lic.fra.dlh.de/artifactory \
//              --user=$REGISTRY_CRED_USR --password=$REGISTRY_CRED_PSW \
//              docker-isb-local/isb/${APPNAME}/latest"""
//            )
//          }
//        }
//      }
//    }

    stage('build image') {
      environment {
        BUILDARGS="--build-arg http_proxy=$env.PROXY --build-arg https_proxy=$env.PROXY --build-arg $env.NO_PROXY"
        DESTINATIONS="--destination=${env.IMAGE}:latest --destination=${env.IMAGE}:${env.TAG}"
      }
      steps {
        // slackSend channel: "lsy-esp-cicd-poc", color: "#0DADEA", message: "Started build #${env.BUILD_NUMBER} of ${env.JOB_NAME}\nURL: ${env.BUILD_URL}"
        container('kaniko') {
          sh """
            cat ${AUTH_FILE} >/kaniko/.docker/config.json
            /kaniko/executor --skip-tls-verify-pull ${BUILDARGS} --registry-mirror ${REGISTRY} --skip-tls-verify ${DESTINATIONS} -c `pwd`
          """
        }
      }
    }

    stage('grype scan') {
      steps {
        container('grype') {
          script {
            def res = sh(returnStdout: true, script: """
              #!/usr/bin/env bash
              mkdir -p /config
              cat ${AUTH_FILE} >/config/config.json
              export DOCKER_CONFIG=/config
              grype ${env.IMAGE}:${env.TAG}
            """).trim()
            println res
            // if (res.contains('Critical')) {
            //   slackSend channel: "lsy-esp-cicd-poc", color: "#FF0000", message: ":exclamation: Grype security scan #${env.BUILD_NUMBER} of ${env.JOB_NAME}\nLOG: ${env.BUILD_URL}consoleText\nGrype scan: Result contains criticals!"
            // } else {
            //   slackSend channel: "lsy-esp-cicd-poc", color: "#18BE52", message: ":white_check_mark: Grype security scan #${env.BUILD_NUMBER} of ${env.JOB_NAME}\nLOG: ${env.BUILD_URL}consoleText\nGrype scan: Success!"
            // }
          }
        }
      }
    }

    /*
    stage('modify target image') {
      steps {
        container('prov-tools') {
          sh """
            cd k8s/${ENV}
            kustomize edit set image ${APPNAME}=${IMAGE}:${TAG}
          """
        }
      }
    }

    stage('bump final image version back to git') {
      steps {
        sshagent(credentials: ['CODEBASE_DEV_ACCESS']) {
          sh '''
            export GIT_SSH_COMMAND="ssh -oStrictHostKeyChecking=no"
            git config --global user.name "Jenkins"
            git config --global user.email "jenkins@lhsystems.com"
            git checkout master
            git commit -am 'Jenkins: set new image version'
            git push
          '''
        }
      }
    }
    */

    // stage('delete old docker images') {
    //   steps {
    //     container('jfrog-cli') {
    //       script {
    //         def images = ["isb/${APPNAME}/*"]
    //         echo "Searching for images"
    //         images.each { image ->
    //           sh (
    //             """jf rt s --insecure-tls \
    //             --recursive=false --include-dirs --exclusions='*_uploads;*latest' \
    //             --sort-by=created --sort-order=desc --offset 0 \
    //             --url=https://vmh-aiapd-testenv.lic.fra.dlh.de/artifactory \
    //             --user=$REGISTRY_CRED_USR --password=$REGISTRY_CRED_PSW \
    //             docker-isb-local/$image"""
    //           )
    //         }
    //         echo "Images to delete"
    //         images.each { image ->
    //           sh (
    //             """jf rt del --insecure-tls \
    //             --recursive=false --quiet --exclusions='*_uploads;*latest' \
    //             --sort-by=created --sort-order=desc --offset 3 \
    //             --url=https://vmh-aiapd-testenv.lic.fra.dlh.de/artifactory \
    //             --user=$REGISTRY_CRED_USR --password=$REGISTRY_CRED_PSW \
    //             docker-isb-local/$image"""
    //           )
    //         }
    //       }
    //     }
    //   }
    // }
  }

  post {
    success {
    //   slackSend channel: "lsy-esp-cicd-poc", color: "#18BE52", message: ":white_check_mark: Build #${env.BUILD_NUMBER} of ${env.JOB_NAME}\nsuccessfully finished\nLOG: ${env.BUILD_URL}consoleText\nImage ready to be deployed: ${env.IMAGE}:${env.TAG}"
      echo "** Image: ${env.IMAGE}:${env.TAG} ready to be deployed by Argo CD **"
    }
    failure {
    //   slackSend channel: "lsy-esp-cicd-poc", color: "#FF0000", message: ":exclamation: Build #${env.BUILD_NUMBER} failed of ${env.JOB_NAME}\nLOG: ${env.BUILD_URL}consoleText\nCheck log!"
      echo "** Failure while creating image **"
    }
  }
}
