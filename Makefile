# ubuntu
install:
	PATH=/usr/local/bin:$$PATH; pip3 install -e .
	PATH=/usr/local/bin:$$PATH; pip3 install numpy
	PATH=/usr/local/bin:$$PATH; p=`which loadreporter`; echo $$p; sed -e "s!LOADREPORTER_PATH!$$p!" < systemctl/loadreporter.tmpl > systemctl/loadreporter.service
	install -m 0644 avahi/loadreporter.service /etc/avahi/services/
	install -m 0644 systemctl/loadreporter.service /etc/systemd/system
	systemctl enable loadreporter
	systemctl stop loadreporter
	systemctl start loadreporter

# PyPIへのデプロイ
deploy:
	@echo "Checking for uncommitted changes..."
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Error: Uncommitted changes exist. Please commit or stash them first."; \
		exit 1; \
	fi
	@echo "Checking for untracked files..."
	@if [ -n "$$(git ls-files --others --exclude-standard)" ]; then \
		echo "Error: Untracked files exist. Please add them to git or add to .gitignore."; \
		exit 1; \
	fi
	@echo "Checking for unpushed commits..."
	@if [ -n "$$(git log @{upstream}..)" ]; then \
		echo "Error: Unpushed commits exist. Please push them first."; \
		exit 1; \
	fi
	@echo "Building package..."
	python3 -m build
	@echo "Uploading to PyPI..."
	twine upload dist/*
	@echo "Creating git tag..."
	@version=$$(python3 -c "import setup; print(setup.setup(name='LoadReporter')['version'])"); \
	git tag -a "v$$version" -m "Release version $$version"; \
	git push origin "v$$version"
	@echo "Deployment completed successfully!"
