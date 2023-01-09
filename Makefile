install:
	sudo install -m 0644 avahi/loadreporter.service /etc/avahi/services/
	sudo install -m 0644 systemctl/loadreporter.service /etc/systemd/system
	sudo pip3 install -e . # git+git://github.com/vitroid/loadreporter.git@main
