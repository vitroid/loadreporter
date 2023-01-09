install:
	sudo install avahi/loadreporter.service /etc/avahi/services/
	sudo install systemctl/loadreporter.service /etc/systemd/system
	sudo pip3 install -e . # git+git://github.com/vitroid/loadreporter.git@main
