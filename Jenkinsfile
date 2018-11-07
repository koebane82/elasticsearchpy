def gitRepo = "https://github.com/koebane82/elasticsearchpy.git"
def buildEnv = env.BRANCH_NAME
node("python"){
  stage("checkout"){
      dir("files"){
          checkout(
            [
              $class: 'GitSCM', 
              branches: [[name: buildEnv]
            ], 
            doGenerateSubmoduleConfigurations: false, 
            userRemoteConfigs: [
              [url: gitRepo]
            ]]
          )
      }
  }

  stage("Unit Test"){
    dir("files"){
      sh "pytest -pep8"
    }
  }

  stage("Build Package"){
    dir("files"){
      sh "cat '${env.BUILD_ID}'' > BUILD_NUMBER"
      sh "python3 setup.py sdist bdist_wheel"
    }
  }

  stage("Archive"){
    dir("files/dist"){
      archiveArtifacts 'elasticsearchpy-*.tar.gz'
    }
  }
  
  if (buildEnv == "master"){
    stage("Upload to PiP"){

    }
  }
}