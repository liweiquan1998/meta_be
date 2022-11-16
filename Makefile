NAME=meta_be
VERSION=latest
BUILD_TIME      := $(shell date "+%F %T")
COMMIT_SHA1     := $(shell git rev-parse HEAD)
AUTHOR          := $(shell git show -s --format='%an')


.PHONY: all dev pro

dev:
	@docker build -t SXKJ:32775/meta_be:latest --build-arg FLASK_ENV='development' .
	@docker push SXKJ:32775/meta_be:latest

pro:
	@docker build -t registry-vpc.cn-hangzhou.aliyuncs.com/sxkj/meta_be:latest --build-arg FLASK_ENV='production' .
	@docker push registry-vpc.cn-hangzhou.aliyuncs.com/sxkj/metaverse:latest
