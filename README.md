# FFEncoding
```
git clone https://github.com/katiadesimone/FFEncoding.git 
```
## Deploy Minikube
ci spostiamo nella cartella Prometheus, dove ci sono i file .yaml da deployare su Minikube
```
cd FFEncoding/Prometheus/
```
A questo punto, possiamo 
1. avviare minikube;
```
minikube start
```
2. creare il namespace monitoring;
```
kubectl create namespace monitoring 
```
3. deployare i vari pod contenuti nella cartella corrente.
```
kubectl apply -f [file YAML]
```
## Deploy Docker Image
Terminati i deploy ci spostiamo nella cartella ApplicationEncoding:
1.creiamo l'immagine docker a partire dal Dockerfile ed il contesto contenuti nella cartella;
```
docker build dockerapp
```
2. Poi ho pushato l'immagine in Docker Hub in modo da essere reperibile per il deploy su minikube;
3. Infine, possiamo deployare il pod basato sull'immagine creata con il seguente comando:
```
kubectl run ffmpeg --image=katiadesimone/progetto:v1.3 -n monitoring
```
