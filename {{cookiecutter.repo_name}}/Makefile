.DEFAULT_GOAL := help
DEFAULT_BRANCH := main
ROLE_DIR := $(shell basename $(CURDIR))

# Determine this makefile's path.
# Be sure to place this BEFORE `include` directives, if any.
THIS_FILE := $(lastword $(MAKEFILE_LIST))
VERSION := 0.0.0
#  use the long commit id
COMMIT := $(shell git rev-parse HEAD)
AWS_ACCOUNT_ID := $(shell aws sts get-caller-identity --output text | awk '{print $$1}')


help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

clean-venv: ## re-create virtual env
	rm -rf .venv
	python3 -m venv .venv
	( \
       . .venv/bin/activate; \
       pip install --upgrade pip setuptools; \
    )

git-status: ## require status is clean so we can use undo_edits to put things back
	@status=$$(git status --porcelain); \
	if [ ! -z "$${status}" ]; \
	then \
		echo "Error - working directory is dirty. Commit those changes!"; \
		exit 1; \
	fi

undo_edits: ## undo staged and unstaged change. ohmyzsh alias: grhh
	git reset --hard

rebase: git-status ## rebase current feature branch on to the default branch
	git fetch && git rebase origin/$(DEFAULT_BRANCH)

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

shellcheck:
	find . -type f -name "*.sh" -exec "shellcheck" "--format=gcc" {} \;

bump: git-status ## bump version in main branch
ifeq ($(CURRENT_BRANCH), $(MAIN_BRANCH))
	( \
	   . .venv/bin/activate; \
	   pip install bump2version; \
	   bump2version $(part); \
	)
else
	@echo "UNABLE TO BUMP - not on Main branch"
	$(info Current Branch: $(CURRENT_BRANCH), main: $(MAIN_BRANCH))
endif

build: git-status ## push images to registry and upload python package to artifacts
	( \
       docker build --tag $(CONTROLLER)-appd-db-agent:$(AGENT_VERSION) appd-db-agent; \
    )

docker-run:  ##  run wiht docker run
	docker run -d --rm --memory=3g \
	--name=$(CONTROLLER)-appd-db-agent \
	-e DB_AGENT_NAME="$(DB_AGENT_NAME)" \
	$(CONTROLLER)-appd-db-agent:$(AGENT_VERSION); \

docker-stop:  ##  run wiht docker run
	docker stop $(CONTROLLER)-appd-db-agent

docker-login:
	$$(aws ecr get-login --no-include-email  --region us-east-1)

docker-pull: docker-login  ## pull the image from ecr
	( \
       docker pull $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(CONTROLLER)-appd-db-agent:$(AGENT_VERSION); \
       docker tag $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(CONTROLLER)-appd-db-agent:$(AGENT_VERSION) $(CONTROLLER)-appd-db-agent:$(AGENT_VERSION); \
    )

upload_to_ecr: docker-login ## push images to registry and upload python package to artifacts
	( \
       docker tag $(CONTROLLER)-appd-db-agent:$(AGENT_VERSION) $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(CONTROLLER)-appd-db-agent:$(AGENT_VERSION); \
       docker push $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(CONTROLLER)-appd-db-agent:$(AGENT_VERSION); \
    )


.PHONY: static shellcheck test