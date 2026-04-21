#!/bin/bash

## Develop GIT
sudo apt update
sudo apt upgrade

sudo apt install git -y
git config --global user.name "CS_Animatronics"
git config --global user.email "2023m002@kuas.ac.jp"

git config --global --list

ssh-keygen -t rsa -b 4096 -C "2023m002@kuas.ac.jp"

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

cat ~/.ssh/id_rsa.pub
