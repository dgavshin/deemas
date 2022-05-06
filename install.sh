#!/bin/bash

sudo apt update -y
sudo apt install zsh python3.9-full neovim -y

XTABLES_LIBDIR="/usr/lib/x86_64-linux-gnu/xtables/"

function install_iptables() {
  echo "[+] Install iptables"

  sudo apt install autoconf libtool libmnl-dev libnftnl-dev -y
  cd /tmp || exit && git clone git://git.netfilter.org/iptables && cd iptables || exit
  ./autogen.sh
  ./configure --prefix=/tmp/iptables
  make
  make install
  sed -i "s/XTABLES_LIBDIR=\/usr\/lib\/x86_64-linux-gnu\/xtables/XTABLES_LIBDIR=\/tmp\/iptables\/lib\/xtables/" .env
}

echo "[+] Python virtual environment installation..."
python3 -m venv venv
. ./venv/bin/activate


if compgen -G "$XTABLES_LIBDIR" 2>/dev/null; then
  pass
else
  install_iptables
fi

echo "Done! Run server with ./start_server.sh"
