import subprocess

import paramiko as paramiko

import ssh_tools


def get(host):
    command = "sudo batctl o -H -t 7"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, "pi", "pi", timeout=1)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    out = ""
    for line in lines:
        out += line
    ssh.close()
    return out


def resolvName(host):
    return ssh_tools.send("192.168.199.1", f'sudo batctl t {host}').strip()
    # return subprocess.run(f'sudo batctl t {host}'.split(), stdout=subprocess.PIPE).stdout.decode("utf-8").strip()


if __name__ == '__main__':
    print(get("192.168.199.1"))
