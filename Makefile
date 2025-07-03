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
	sudo install -m 0644 avahi/loadreporter.service /etc/avahi/services/
	sudo install -m 0644 systemctl/loadreporter.service /etc/systemd/system
	sudo systemctl enable loadreporter
	sudo systemctl stop loadreporter
	sudo systemctl start loadreporter

