#!/bin/sh
git clone https://github.com/eJRF/chef-ejrf.git ../chef-ejrf
echo $SSH_PEM > ejrf.pem
ssh-add  ejrf.pem
cd ../chef-ejrf
knife solo cook ubuntu@54.194.205.112