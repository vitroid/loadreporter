# ubuntu
install:
	pip3 install -e .
	PATH=$$PATH:/usr/local/bin; p=`which loadreporter`; echo $$p; sed -e "s!LOADREPORTER_PATH!$$p!" < systemctl/loadreporter.tmpl > systemctl/loadreporter.service
	install -m 0644 avahi/loadreporter.service /etc/avahi/services/
	install -m 0644 systemctl/loadreporter.service /etc/systemd/system
	systemctl enable loadreporter
	systemctl stop loadreporter
	systemctl start loadreporter
