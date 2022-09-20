from drawer import Node

nameMap = {
    "b8:27:eb:fb:8d:72": "Mapper",
    "b8:27:eb:c2:2d:2e": "Gateway",
    "b8:27:eb:25:db:6e": "Bridge",
    "b8:27:eb:89:77:9c": "Setup",
    "b8:27:eb:c1:b9:7a": "Far",
    "b8:27:eb:85:7f:9c": "Felix",
    "b8:27:eb:04:0f:99": "Carlos I",
    "b8:27:eb:b3:65:d8": "Carlos II",
    "b8:27:eb:2b:d5:77": "Carlos III",
    "b8:27:eb:aa:3c:be": "Carlos IV",
    "b8:27:eb:a4:d5:1e": "Carlos V",
    "": "Carlos VI",
}


def mapNode(node: Node):
    node.name = nameMap.get(node.name, node.name)


def mapNames(nodes):
    for node in nodes:
        mapNode(node)
