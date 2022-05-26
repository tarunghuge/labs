Docker Basic Installation ::

Rundeck :
docker pull rundeck/rundeck:4.2.1
docker run -d --name local-rundeck -p 4440:4440 -e RUNDECK_GRAILS_URL=http://localhost:4440 -v ${PWD}:/home/rundeck/server/data rundeck/rundeck:4.2.1

Jenkins :
docker pull jenkins/jenkins
docker run -d --name local-jenkins -p 8080:8080 -p 50000:50000 -v jenkins-data:/var/jenkins_home  jenkins/jenkins

Jupyter :
docker pull jupyter/minimal-notebook
docker run -d --name local-jupyter -p 8081:1001 -v jupyter-data:/opt/bitnami/miniconda/bin bitnami/jupyter-base-notebook:latest

Prometheus :
docker pull prom/prometheus
docker run -d --name local-prom -p 9090:9090 -v prom-data:/etc/prometheus/ prom/prometheus