@ECHO OFF
ECHO Fix DHCP Configuration:
ECHO The network card is restarting
ECHO Please wait...
ipconfig /release>NUL 1>NUL 2>NUL
ipconfig /renew>NUL 1>NUL 2>NUL
ipconfig /flushdns
ipconfig /registerdns
ECHO All Done. The network card has restarted !
ECHO Please enjoy it.
:EN