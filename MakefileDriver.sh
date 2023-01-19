#! /bin/bash

# 1つ目の引数を解析
case $1 in
    "start")
        # 起動処理
        echo "start"
        kubectl apply -f ./k8s/mysql/cm.yaml
        kubectl apply -f ./k8s/mysql/secret.yaml
        kubectl apply -f ./k8s/mysql/mysql-svc.yaml
        kubectl apply -f ./k8s/mysql/mysql-cm-script.yaml
        kubectl apply -f ./k8s/mysql/mysql-sts.yaml
        ;;
    "end")
        # 終了処理
        kubectl delete -f ./k8s/mysql/.yaml
        kubectl delete -f ./k8s/mysql/.yaml
        kubectl delete -f ./k8s/mysql/.yaml
        kubectl delete -f ./k8s/mysql/.yaml
        kubectl delete -f ./k8s/mysql/.yaml
        echo "end"
        ;;
esac
