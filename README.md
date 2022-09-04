# FFEncoding
```
$ git clone https://github.com/katiadesimone/FFEncoding.git 
```
## Deploy Minikube
ci spostiamo nella cartella Prometheus, dove ci sono i file .yaml da deployare su Minikube
$ start minikube
$ kubectl create namespace monitoring 
$ kubectl apply -f file.yaml
## Deploy Docker Image
Terminati i deploy ci spostiamo nella cartella ApplicationEncoding e creiamo l'immagine docker a partire dal Dockerfile ed il contesto contenuti nella cartella:
$ docker build dockerapp
Poi pushiamo l'immagine in Docker Hub in modo da essere reperibile per il deploy su minikube:
$ kubectl run ffmpegApp--image=katiadesimone/progetto:v1.3 -n monitoring
