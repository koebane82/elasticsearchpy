def gitRepo = "https://github.com/koebane82/elasticsearchpy.git"
def buildEnv = env.BRANCH_NAME

def pyPiCreds = "testPyPi"
def pyPiUrl = "https://test.pypi.org/legacy/"

properties(
  [
    buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '10')), parameters(
      [
        booleanParam(defaultValue: false, description: 'Should this build be released to production', name: 'release')
      ]
    )
  ]
)

if (buildEnv == "master"){
  if (params['release'] != true){
    println("!!!!!! Master Builds can not run without the release parameter !!!!!")
    sh 'exit 2'
  }

  pyPiCreds = "prodPyPi"
}

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
    println("################################\n#     Running Unit Tests       #\n################################")
    dir("files"){
      sh "pytest -pep8"
    }
  }

  stage("Build Package"){
    println("################################\n#      Building Package        #\n################################")

    dir("files"){
      if (buildEnv == "master"){
        sh "echo 'RELEASE' > BUILD_NUMBER"
      } else {
        sh "echo '${env.BUILD_ID}' > BUILD_NUMBER"
      }
      
      sh "python3 setup.py sdist bdist_wheel"
    }
  }
  
  stage("Upload to PiPy"){
    if (params["release"] == true){
      withCredentials([
        usernamePassword(credentialsId: pyPiCreds, passwordVariable: 'PIPYPASS', usernameVariable: 'PIPYUSER')
      ]) {
        def twine_envs = [
          "TWINE_USERNAME=${PIPYUSER}", 
          "TWINE_PASSWORD=${PIPYPASS}"
        ]
  
        if (buildEnv != "master"){
          twine_envs.add("TWINE_REPOSITORY_URL=${pyPiUrl}")
        }
        withEnv(twine_envs) {
          dir("files"){
            sh "twine upload dist/*"
          }
        }
      }
    } else {
      println("Skipping Stage")
    }
  }
}