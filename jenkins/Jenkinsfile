stage('Build Docker Image') {
    node ('kaniko') {
        withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PASSWORD')]) {
            git branch: 'main',
                url: 'https://github.com/Kubison/java-app.git'
        }
        container('kaniko') {
            stage('Build Image') {
                sh 'executor --dockerfile `pwd`/Dockerfile --context `pwd` --destination=kubison/java-app:$BUILD_NUMBER'
            }
        }
    }
}

stage('Deploy Image') {
    node('master') {
         withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PASSWORD')]) {
            git branch: 'main',
                url: 'https://github.com/Kubison/java-app.git'
        }
        withCredentials([file(credentialsId: 'kube', variable: 'KUBECONFIG_FILE')]) {
                    def kubeconfigContent = readFile(file: env.KUBECONFIG_FILE)
            def dep_file = 'java-app/java-app-deployment.yaml'
            def old_w = 'kubison/java-app:1'
            def new_w = "kubison/java-app:${env.BUILD_NUMBER}"
            sh "sed -i 's!${old_w}!${new_w}!g' ${dep_file}"
            sh 'cat java-app/java-app-deployment.yaml'
            ansiblePlaybook(
                
                playbook: 'java-app/playbook.yaml',
                colorized: true,
                extraVars: [
                            kubeconfig: './../kubeconfig' 
                        ]
            )
        }
    }
}
