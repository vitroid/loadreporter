install:
	sudo install avahi/loadreporter.service /etc/avahi/services/
	sudo install systemctl/loadreporter.service /etc/systemd/system
	sudo python setup.py install
