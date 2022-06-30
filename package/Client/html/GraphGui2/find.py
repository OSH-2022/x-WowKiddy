from asyncio import subprocess
import subprocess
import sys
from py2neo import Node, Relationship, Graph, Path, Subgraph
from py2neo import NodeMatcher, RelationshipMatcher

# user
neo4j_url = 'neo4j://106.14.156.191'
user = 'neo4j'
pwd = 'DCchengding2003'

# connect
graph = Graph(neo4j_url,  auth=(user, pwd))

# find nodes
matcher = NodeMatcher(graph)
nodes = list(matcher.match(sys.argv[1]))

paths = []
for node in nodes:
    tmp_str = node["path"]
    i = tmp_str.find("mnt")
    i += 4
    tmp_str = tmp_str[i:]
    path = 'X:\\' + tmp_str
    paths.append(path)


with open('C:\\Users\\dingcheng\\Desktop\\x-WowKiddy\\package\\html\\GraphGui2\\warm.txt', 'w') as f:
    for path in paths:
        f.write(path + '\n')

subprocess.Popen(["juicefs","warmup","-f","warm.txt"], shell=True)

