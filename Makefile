build:
	cd src && docker build -t nori/rhythm-bot:1.1 .

run:
	kubectl apply -f ./k8s/deployment.yaml && \
	kubectl apply -f ./k8s/secret-pod.yaml && \
	kubectl apply -f ./k8s/mysql-pv.yaml && \
	kubectl apply -f ./k8s/mysql-deployment.yaml

stop:
	kubectl delete svc rhythm-bot-svc && \
	kubectl delete deploy rhythm-bot && \
	kubectl delete deployment,svc mysql

status:
	kubectl get all
