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
# 仮想環境を使用してシステム全体にインストール
install:
	@echo "Creating virtual environment..."
	sudo python3 -m venv /opt/loadreporter
	@echo "Installing dependencies in virtual environment..."
	sudo /opt/loadreporter/bin/pip install --upgrade pip
	sudo /opt/loadreporter/bin/pip install fastapi uvicorn numpy netifaces zeroconf
	@echo "Copying package to virtual environment..."
	SITE_PACKAGES=$$(sudo /opt/loadreporter/bin/python -c "import site; print(site.getsitepackages()[0])"); \
	sudo mkdir -p $$SITE_PACKAGES/loadreporter; \
	sudo cp -r loadreporter/* $$SITE_PACKAGES/loadreporter/; \
	sudo chmod -R 755 $$SITE_PACKAGES/loadreporter/
	@echo "Testing package import..."
	sudo /opt/loadreporter/bin/python -c "import loadreporter.api; print('Package import successful')"
	@echo "Creating systemd service file from template..."
	PYTHON=/opt/loadreporter/bin/python; \
	WORKDIR=/opt/loadreporter; \
	sed -e "s!@PYTHON@!$$PYTHON!g" -e "s!@WORKDIR@!$$WORKDIR!g" < systemctl/loadreporter.tmpl > systemctl/loadreporter.service
	@echo "Installing system files..."
	sudo install -m 0644 avahi/loadreporter.service /etc/avahi/services/
	sudo install -m 0644 systemctl/loadreporter.service /etc/systemd/system
	@echo "Enabling and starting service..."
	sudo systemctl daemon-reload
	sudo systemctl enable loadreporter
	sudo systemctl stop loadreporter || true
	sudo systemctl start loadreporter
	@echo "Installation completed!"
	@echo "Service status:"
	sudo systemctl status loadreporter --no-pager -l

