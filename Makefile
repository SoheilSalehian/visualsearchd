# Makefile to build each golang microservice (statically linked and the run docker-compose)
SUBDIRS := $(wildcard u*/.)
build: $(SUBDIRS) 
$(SUBDIRS):
	cd $@ && CGO_ENABLED=0 GOOS=linux go build -ldflags "-s" -a -installsuffix cgo -o main

dev: 
	$(MAKE) build 
	export COMPOSE_FILE=${COMPOSE_FILE} && docker-compose --file ${COMPOSE_FILE} build && docker-compose up

deployment:
	$(MAKE) build 
	export COMPOSE_FILE=${COMPOSE_FILE} && python2.7 build-tag-push.py \
	&& sh fixup-yaml.sh \
	&& echo DEPLOYING: ${COMPOSE_FILE} && ecs-cli compose --file ${COMPOSE_FILE} up

.PHONY: all $(SUBDIRS)
	
