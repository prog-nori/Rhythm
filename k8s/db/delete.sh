#! /bin/bash
#  -*- coding: utf-8 -*-

# if mysql-client pod exists, then delete it.
if [ $((`kubectl get all | grep -c mysql-client`)) -gt 0 ]
then
kubectl delete po mysql-client
fi

# delete all
for file in service db-deployment secret pv
do
kubectl delete -f ~/develop/discord-bot/Rhythm/k8s/db/$file.yaml
done
