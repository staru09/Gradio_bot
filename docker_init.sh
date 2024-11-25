#!/bin/bash
sudo apt remove docker-desktop

rm -r $HOME/.docker/desktop
sudo rm /usr/local/bin/com.docker.cli
sudo apt purge docker-desktop

sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
sudo apt-get update

cd Downloads
sudo apt-get install ./docker.deb

systemctl --user restart docker-desktop
docker --version