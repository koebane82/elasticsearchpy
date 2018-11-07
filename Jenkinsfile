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
    println("################################")
    println("#     Running Unit Tests       #")
    println("################################")

    dir("files"){
      sh "pytest -pep8"
    }
  }

  stage("Build Package"){
    println("################################")
    println("#      Building Package        #")
    println("################################")

    dir("files"){
      sh "echo '${env.BUILD_ID}' > BUILD_NUMBER"
      sh "python3 setup.py sdist bdist_wheel"
    }
  }

  stage("Archive"){
    println("################################")
    println("#        Archiving Tar         #")
    println("################################")
    dir("files/dist"){
      archiveArtifacts 'elasticsearchpy-*.tar.gz'
    }
  }
  
  if (buildEnv == "master"){
    stage("Upload to PiP"){

    }
  }
}