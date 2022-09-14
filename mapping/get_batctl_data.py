import subprocess
import re
import csv
import get_batctl_ssh

pattern = "(.)\s(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)\s*\S*\s*\((\s*\d+)\)\s*(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)"


def createCSV(hosts):
    nn = []
    dn = []
    names = ["from/to"]
    for host in hosts:
        try:
            if host == "127.0.0.1":
                resstr = subprocess.run('sudo batctl o -H'.split(), stdout=subprocess.PIPE).stdout.decode("utf-8")
                name = "This node"
            else:
                resstr = get_batctl_ssh.get(host)
                name = get_batctl_ssh.resolvName(host)

            nodes = {}
            adjacencies = {}
            matches = re.findall(pattern, resstr)
            for match in matches:
                isNextHop = match[0] == '*'
                originator = match[1]
                TQ = int(match[2])
                nextHop = match[3]
                if originator == nextHop:
                    nodes[originator] = TQ
                if isNextHop:
                    if not originator in names:
                        names.append(originator)
                adjacencies[originator] = isNextHop
            nodes["from/to"] = name
            nn.append(nodes)
            adjacencies["from/to"] = name
            dn.append(adjacencies)
        except:
            pass

    with open("rsiMat.csv", 'w') as cf:
        w = csv.DictWriter(cf, fieldnames=names)
        w.writeheader()
        for dlist in nn:
            w.writerow(dlist)

    with open("adjMat.csv", 'w') as cf:
        w = csv.DictWriter(cf, fieldnames=names)
        w.writeheader()
        for dlist in dn:
            w.writerow(dlist)
