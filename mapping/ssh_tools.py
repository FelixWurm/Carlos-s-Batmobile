import re
import paramiko


def send(host, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, "pi", "pi", timeout=10)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.readlines()
    out = ""
    for line in lines:
        out += line
    ssh.close()
    return out


def get_host_list():
    return re.findall("192\.168\.199\.[0-9]*", send("192.168.199.1", 'cat /var/lib/misc/dnsmasq.leases'))
