#!/bin/bash
for i in {0..9}
do
    docker run -d --name netadmin_sshd$i rastasheep/ubuntu-sshd
done
