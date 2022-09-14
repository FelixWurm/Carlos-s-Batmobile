import subprocess

import paramiko as paramiko


def get(host):
    command = "sudo batctl o -H"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, "pi", "pi")
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    out = ""
    for line in lines:
        out += line
    ssh.close()
    return out


def resolvName(host):
    return subprocess.run(f'sudo batctl t {host}'.split(), stdout=subprocess.PIPE).stdout.decode("utf-8").strip()


if __name__ == '__main__':
    print(get("192.168.199.1"))
