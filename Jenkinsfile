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

node("python"){
  if (buildEnv == "master"){
    if (params['release'] != true){
      println("!!!!!! Master Builds can not run without the release parameter !!!!!")
      sh 'exit 2'
    }

    pyPiCreds = "prodPyPi"
  }
  
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