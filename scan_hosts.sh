nmap --open -p 8554 192.168.199.1-254 -oG - | grep "/open" | awk '{ print $2 }' > 'hosts'