#!/usr/bin/env bash
# On MAC OS

# Install Go
brew install go

# Install gif-lfs
brew install git-lfs
git lfs install

# Install rocksdb
brew install rocksdb

# Add the following to ~/.bash_profile (GOPATH can be anywhere)
export GOPATH=$HOME/go
export GOROOT=/usr/local/opt/go/libexec
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin

# Clone the git repository with go (doesn't work for me)
# go get -u github.com/iost-official/go-iost

# Create folder in the go path because it seems to be hardcoded in the makefile
mkdir -p $GOPATH/src/github.com/iost-official/go-iost

# Clone the git repository
cd $GOPATH/src/github.com/iost-official/go-iost
git clone https://github.com/iost-official/go-iost.git

# Build the apps
cd go-iost
make build

# Install the apps into the $GOPATH/bin
make install

# Choose a testnet node from the list on this page
# http://developers.iost.io/docs/en/4-running-iost-node/Deployment/
export IOST_NODE='13.229.176.106:30002'

# Run iWallet with the chosen server (example with Singapore node)
iwallet -s $IOST_NODE net

# Create a testnet account (keys are stored in ~/.iwallet/testnet_*)
# Replace id by custom name
iwallet -s $IOST_NODE account -n testnet

# Check the balance
iwallet -s $IOST_NODE balance `cat ~/.iwallet/testnet_ed25519.pub`

# Transfer 0.1 from account testnet to testnet2
iwallet -s $IOST_NODE -k ~/.iwallet/testnet_ed25519 call "iost.system" "Transfer" "[ \
"\""`cat ~/.iwallet/testnet_ed25519.pub`"\"", \
"\""`cat ~/.iwallet/testnet2_ed25519.pub`"\"", \
0.1]"

# Check transaction returned by the previous command
iwallet -s $IOST_NODE transaction C9DvCKGeBdRaPMX3WYExGwL7KXgnaBqR53g9dzJs7VvB

# Or do the signing and publishing separately (required for multi signatures)
iwallet -s $IOST_NODE call "iost.system" "Transfer" "[ \
"\""`cat ~/.iwallet/testnet_ed25519.pub`"\"", \
"\""`cat ~/.iwallet/testnet2_ed25519.pub`"\"", \
0.1]" --signers `cat ~/.iwallet/testnet_ed25519.pub`

# Sign the file with testnet account
iwallet -s $IOST_NODE sign -k ~/.iwallet/testnet_ed25519 ./iost.sc

# Publish the files
iwallet -s $IOST_NODE publish -k ~/.iwallet/testnet_ed25519 ./iost.sc ./iost.sig
