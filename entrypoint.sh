service dbus start
service bluetooth start
hciconfig hci0 up

python3 server.py -s -a