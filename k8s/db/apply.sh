#! /bin/bash
#  -*- coding: utf-8 -*-

# docker image build -t my-db-container:1.0 ~/develop/discord-bot/Rhythm/k8s/db/

for file in pv secret db-deployment service
do
kubectl apply -f ~/develop/discord-bot/Rhythm/k8s/db/$file.yaml
done
