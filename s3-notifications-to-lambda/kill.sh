#!/bin/bash

if aws cloudformation describe-stacks --stack-name $1 && aws cloudformation delete-stack --stack-name $1; then
    echo "Successfully deleted" $1
else
    echo "Delete failed"
fi