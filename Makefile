build:
	cd src && docker build -t nori/rhythm-bot:1.1 .

run:
	kubectl apply -f ./k8s/deployment.yaml && \
	kubectl apply -f ./k8s/secret-pod.yaml

start_mysql:
	sh ./k8s/db/apply.sh

stop:
	kubectl delete svc rhythm-bot-svc && \
	kubectl delete deploy rhythm-bot

delete_mysql:
	sh ./k8s/db/delete.sh

status:
	kubectl get all
