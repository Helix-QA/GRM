pipeline {
    agent { label "OneS" }
    stages {
        stage("Подготовка данных"){
            steps{
                script{
                    if (params.nameProduct.contains('finessCorp')){
                        env.applicationId = "ff8080818114016801822509d75d0029"
                        env.folderProduct = "Фитнес клуб КОРП"

                    } else if (params.nameProduct.contains('SpaSalon3')) {
                        env.applicationId = "ff808081811401680182257b91c0002d"
                        env.folderProduct = "SPA - Салон"

                    } else if (params.nameProduct.contains('salon30')){
                        env.applicationId = "ff8080817ccbb453017d0ee91ffe000d"
                        env.folderProduct = "Салон красоты"
                    }
                }                
            }
       }
        stage('Получение предподписанной ссылки') {
            steps {
                script {
                    env.foldercf = "D:\\РЕЛИЗЫ\\${folderProduct}\\cf"
                    def params = [
                        "applicationId": "${env.applicationId}",
                        "name": "${params.version}",
                        "filename": "1Cv8.dt",
                        "releaseDate": new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS").format(new Date())
                    ]
                    def jsonBody = groovy.json.JsonOutput.toJson(params)
                    echo "Request Body: ${jsonBody}"
                    try {
                        def response = httpRequest(
                            url: 'https://1capp.link.1c.ru/1capp-ecw-admin/hs/ECWConfPublication/v1/getPresignedUrl',
                            httpMode: 'GET',
                            contentType: 'APPLICATION_JSON',
                            requestBody: jsonBody,
                            customHeaders: [[name: 'Authorization', value: 'Basic bGFicG86Q28zamlrb20=']],
                            validResponseCodes: '200:299',
                            ignoreSslErrors: true
                        )
                        echo "Response Status: ${response.status}"
                        echo "Response Content: ${response.content}"

                        def jsonSlurper = new groovy.json.JsonSlurper()
                        def responseJson = jsonSlurper.parseText(response.content)
                        def uploadUrl = responseJson.uploadUrl
						env.versionID = responseJson.id

                        echo "Extracted uploadUrl: ${uploadUrl}"
                        env.UPLOAD_URL = uploadUrl
                        echo "Saved uploadUrl to env variable: ${env.UPLOAD_URL}"
                    } catch (Exception e) {
                        echo "Request failed with error: ${e.getMessage()}"
                        error "Failed to get presigned URL: ${e.getMessage()}"
                    }
                }
            }
        }
        stage("Получение .dt"){
            steps{
                script{
                    bat """
                    chcp 65001
                    @call vrunner session kill --db grm --db-user "Админ" --db-pwd "" --uccode grm
                    @call vrunner load --src "${env.foldercf}\\${params.version}.cf" --ibconnection /Slocalhost/grm --uccode grm
                    @call vrunner updatedb --ibconnection /Slocalhost/grm --uccode grm
                    @call vrunner dump dt/1Cv8.dt --ibconnection /Slocalhost/grm --uccode grm
                    @call vrunner session unlock --db grm --db-user "Админ" --db-pwd "" --uccode grm
                    """
                }
            }
        }
		stage('Загрузка файла в объектное хранилище') {
            steps {
                script {
					def uploadUrl = UPLOAD_URL
                    def filePath = "dt/1Cv8.dt" //путь к файлу
                    // Проверка наличия файла
                    if (!fileExists(filePath)) {
                        error "File not found at: ${filePath}"
                    }
                    echo "Uploading file from: ${filePath}"
                    echo "Target URL: ${uploadUrl}"
					// Отправляем запрос через python 
					sh """
					python tools/upload_file.py "${uploadUrl}" "${filePath}"
					"""
                }
            }
        }
		stage('Установка версии по умолчанию') {
			steps {
				script {
					try {
						def response = httpRequest(
							url: "https://1capp.link.1c.ru/1capp-ecw-admin/hs/ECWConfPublication/v1/setDefaultVersion?applicationId=${env.applicationId}&versionId=${env.versionID}",
							httpMode: 'POST',
							contentType: 'APPLICATION_JSON',
							customHeaders: [[name: 'Authorization', value: 'Basic bGFicG86Q28zamlrb20=']],
							validResponseCodes: '200:299', // Ожидаем успешные коды ответа
							ignoreSslErrors: true // Если нужно игнорировать ошибки SSL
						)
						echo "Response Status: ${response.status}"
						echo "Response Content: ${response.content}"
					} catch (Exception e) {
						echo "Request failed with error: ${e.getMessage()}"
						error "Failed to set default version: ${e.getMessage()}"
					}
				}
			}
		}
    }
}