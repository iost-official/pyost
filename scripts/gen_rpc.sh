#!/usr/bin/env bash

#go get -u github.com/iost-official/go-iost
#go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway

IOSTPATH=$GOPATH/src/github.com/iost-official/go-iost
DEST="`dirname \"$0\"`/../pyost/grpc"

# Get the list of .proto files
PROTO_FILES=`cd $IOSTPATH && find * -name "*.proto" | grep -v "vendor"`

# Recreate the hierarchy of folders locally
for f in $PROTO_FILES; do
    mkdir -p "$DEST/`dirname $f`"
done

# Copy the .proto files to the local hierarchy
# Strip out the github references in the imports
# Fix the empty.proto typo
for f in $PROTO_FILES; do
    cat "$IOSTPATH/$f" | sed -e "s|github.com/iost-official/go-iost/||" \
            -e "s|google/protobuf/Empty.proto|google/protobuf/empty.proto|" \
            > "$DEST/$f"
done

for f in $PROTO_FILES; do
    python -m grpc_tools.protoc --proto_path="$DEST:$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis" \
    --python_out="$DEST" --grpc_python_out="$DEST" "$DEST/$f"
done