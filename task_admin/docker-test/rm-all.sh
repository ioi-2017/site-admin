#!/bin/bash
for i in {0..9}
do
    docker rm -f netadmin_sshd$i
done
