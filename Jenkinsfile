config = [
  teamsConnectorName: 'EdTech-QA-Team',
  teamsConnectorUrl:  'https://outlook.office.com/webhook/36e05938-50a0-40ed-9657-5483b2c4ec34@f0d1c6fd-dff0-486a-8e91-cfefefc7d98d/JenkinsCI/bc600ad16b3f4985be4749929e7d547c/85e457eb-b12b-44d6-bf27-0d23de69a378']

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
          image '10.128.42.216:5000/apipython3:latest'
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