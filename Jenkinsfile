config = [
  teamsConnectorName: 'EdTech-Kids-and-Teens-QA',
  teamsConnectorUrl:  'https://outlook.office.com/webhook/a7f32c1d-faf5-4e70-9b87-c1553ce93d97@f0d1c6fd-dff0-486a-8e91-cfefefc7d98d/IncomingWebhook/badf7ebacd1e4fd8b120694383da1b1f/6034223b-343c-4dc8-8cd6-f71f41659b6c'
]

pipeline {
  options {
    disableConcurrentBuilds()
    timeout(time: 5, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '20'))
    office365ConnectorWebhooks([[
      name: config.teamsConnectorName, url: config.teamsConnectorUrl,
      notifySuccess: true, notifyFailure: true, notifyRepeatedFailure: true, notifyUnstable: true, notifyBackToNormal: true
    ]])
  }
  agent none
  triggers {
    cron('H/30 * * * *')
  }
  stages {
    stage('Verify') {
      agent {
        docker {
          label 'CN_Kids_QA_CI'
          image 'apipython3:latest'
        }
      }
      steps {
        script {
          sh 'ptest3  -t E1_API_Automation.Test.GP'
        }
      }
    }
  }
}