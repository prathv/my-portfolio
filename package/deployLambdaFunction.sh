#!/usr/bin/env bash

file="./package.yml"
rm $file

sam package   --template-file template.yml   --output-template-file package.yml   --s3-bucket portfoliobuild.prathveerrai.info

sam deploy   --template-file package.yml   --stack-name newPfdeploy   --capabilities CAPABILITY_IAM
