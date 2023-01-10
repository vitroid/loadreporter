# ubuntu
install:
	install -m 0644 avahi/loadreporter.service /etc/avahi/services/
	install -m 0644 systemctl/loadreporter.service /etc/systemd/system
	pip3 install -e .
	systemctl enable loadreporter
	systemctl start loadreporter
