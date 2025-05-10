# インストール（GitHubからクローンしてインストール）
install-from-github:
	@echo "Cloning repository..."
	git clone https://github.com/vitroid/loadreporter.git /tmp/loadreporter
	@echo "Installing dependencies..."
	cd /tmp/loadreporter && pip3 install -e .
	@echo "Installing system files..."
	cd /tmp/loadreporter && \
	p=`which loadreporter`; \
	sed -e "s!LOADREPORTER_PATH!$$p!" < systemctl/loadreporter.tmpl > systemctl/loadreporter.service && \
	install -m 0644 avahi/loadreporter.service /etc/avahi/services/ && \
	install -m 0644 systemctl/loadreporter.service /etc/systemd/system
	@echo "Enabling and starting service..."
	systemctl daemon-reload
	systemctl enable loadreporter
	systemctl start loadreporter
	@echo "Cleaning up..."
	rm -rf /tmp/loadreporter
	@echo "Installation completed!"

# ローカルインストール
install:
	pip3 install -e .
	p=`which loadreporter`; echo $$p; sed -e "s!LOADREPORTER_PATH!$$p!" < systemctl/loadreporter.tmpl > systemctl/loadreporter.service
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
	poetry build
	@echo "Uploading to PyPI..."
	@if [ -z "$$POETRY_PYPI_TOKEN_PYPI" ]; then \
		echo "Note: POETRY_PYPI_TOKEN_PYPI environment variable is not set."; \
		echo "You will be prompted for PyPI credentials."; \
	fi
	poetry publish --build
	@echo "Creating git tag..."
	@version=$$(poetry version -s); \
	git tag -a "v$$version" -m "Release version $$version"; \
	git push origin "v$$version"
	@echo "Deployment completed successfully!"
