#!/usr/bin/env bash

#go get -u github.com/iost-official/go-iost
#go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway

cat $GOPATH/src/github.com/iost-official/go-iost/rpc/apis.proto | \
sed 's|import "google/protobuf/Empty.proto"|import "google/protobuf/empty.proto"|' \
> $GOPATH/src/github.com/iost-official/go-iost/rpc/apis.proto.tmp

mv $GOPATH/src/github.com/iost-official/go-iost/rpc/apis.proto.tmp \
$GOPATH/src/github.com/iost-official/go-iost/rpc/apis.proto

find $GOPATH/src/github.com/iost-official/go-iost/* -name "*.proto" | grep -v "vendor" | xargs -n1 \
python -m grpc_tools.protoc -I. -I/usr/local/include -I$GOPATH/src \
-I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
--python_out=./pyost/grpc --grpc_python_out=./pyost/grpc

find pyost/grpc/github.com -name \*py | while read f
do cp "$f" "pyost/grpc/github/com${f#pyost/grpc/github.com}"
done

rm -rf pyost/grpc/github.com

