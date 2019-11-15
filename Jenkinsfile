pipeline {
  agent {
    label 'jenkins-slave'
  }
  environment {
    registryCredential = 'dockerhub'
    version = "1.3.0.1-$BUILD_NUMBER"
    buildName = String.format("derrickwalton/slackbot:%s", version)
    linuxBuild = ''
    PYTHONPATH = "${WORKSPACE}"
  }
  stages {
    stage('Setup'){
      steps {
        sh 'echo "Begin setup"'
        notifyBuild('STARTED')
        git 'https://github.com/plainenough/slackbot'
        withCredentials([
          file(credentialsId: 'k8sconfig', variable: 'kubeconfig')
        ]) {
          sh 'cp $kubeconfig ../kubeconfig'
        }
      }
    }
    stage('testing') {
      steps {
        sh "kubectl  --kubeconfig ../kubeconfig --insecure-skip-tls-verify get pods"
        sh "pytest -v --junit-xml=results.xml"
      }
    }
    stage('Build') {
      steps {
        sh 'echo "Begin build"'
        script {
            linuxBuild = docker.build(buildName, "-f ./container/Dockerfile --no-cache .")
        }
      }
    }
  }
  post {
    always {
      junit testResults: 'results.xml', healthScaleFactor: 100
    }
    failure {
      notifyBuild(currentBuild.result)
    }
    success {
      lastChanges since: 'LAST_SUCCESSFUL_BUILD', format:'SIDE',matching: 'LINE'
      script {
        docker.withRegistry( '', registryCredential ) {
          linuxBuild.push()
          linuxBuild.push('latest')
        }
      }
      sh "kubectl --kubeconfig ../kubeconfig --insecure-skip-tls-verify set image deployment/slackbot -n slackbot slackbot=derrickwalton/slackbot:\"${version}\""
      notifyBuild(currentBuild.result)
    }
  }
}

def notifyBuild(String buildStatus = 'STARTED') {
  buildStatus =  buildStatus ?: 'SUCCESS'
  
  def colorName = 'RED'
  def colorCode = '#FF0000'
  def channelName = '#jenkins_alerts' // This is where you would set your custom channel. 
  def details = """STARTED: Job ${env.JOB_NAME} ${env.BUILD_NUMBER}"""

  if (buildStatus == 'STARTED') {
    color = 'YELLOW'
    colorCode = '#FFFF00'
  } else if (buildStatus == 'SUCCESS') {
    color = 'GREEN'
    colorCode = '#2E9022'
    details = """SUCCESS (${env.BUILD_URL})"""
  } else {
    color = 'RED'
    colorCode = '#FF0000'
    details = """FAILED: Job ${env.JOB_NAME} ${env.BUILD_NUMBER}
  Check console output at ${env.BUILD_URL}${env.JOB_NAME} ${env.BUILD_NUMBER}"""
  }
  // Send notifications
  slackSend (color: colorCode, message: details, channel: channelName )
}
