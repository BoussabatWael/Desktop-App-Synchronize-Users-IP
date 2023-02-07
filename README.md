# Desktop-App-Synchronize-Users-IP

A desktop application used to sychronize users IP addresses in their serves.
The application check all servers relarted to the user, then check the user IP address if it's synchronized in servers or not.
if NOT, the application will call the firewall script using the middleware, then the script will connect to servers, check their 
operating systems and their system versions, if OS is supported then it will execute commands to synchronize user new IP address.

# Sync.py 
is the main file of the application.
# firewall.py 
is the script that manage and sercure servers it contains all functions that can be executed on server
# networking.php 
is the middleware userd to call the firewall script from the desktop app.
