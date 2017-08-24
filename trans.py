# coding: utf-8

import json

import jieba 
from bosonnlp import BosonNLP

nlp = BosonNLP('o9uEJKop.17505.Bh6hezGEy2z2')

def purge_sql(line):

    line = line.lstrip('INSERT INTO `track_extra_information` VALUES ')
    line = line.rstrip(';\n')
    line = line.replace('),(', ')\n(')
    return line + '\n'

def purge_sql_more(line):

    line = line.lstrip('INSERT INTO `track_extra_information` VALUES ')
    line = line.rstrip(';\n')
    line = line.replace('),(', ')\n(')
    return line + '\n'

def replace_null(line):
    
    line = line.replace('NULL', 'None')
    t = eval(line)
    return json.dumps({'id': t[0], 'content':t[4]}) + '\n'

def jieba_line(line):

    line = json.loads(line)
    line = line.get('content')
    line = ' | '.join(list(map(lambda x: x.strip('\n'), jieba.cut(line)))).rstrip('\n')
    line = line + '\n'
    line = line.encode('utf8', errors='strict')
    return line

def boson_line(line):

    l = list(map(lambda x: json.loads(x).get('content'), line))
    result = list(map(lambda x:' | '.join(x.get('word')), nlp.tag(l)))
    result = '\n'.join(result) + '\n'
    result = result.encode('utf8', errors='ignore')
    return result

def read_1_write(ff, tf):

    with open(ff, 'r') as f:
        for line in f:
            line = jieba_line(line)
            with open(tf, 'a') as ft:
                ft.write(line)

def read_100_write(ff, tf):

    n = 100
    with open(ff, 'r') as f:
        lines = f.readlines()
        lines = [lines[i:i+n] for i in range(0, len(lines), n)]
        for line in lines:
            line = boson_line(line)
            with open(tf, 'a') as ft:
                ft.write(line)

def main():
    ff = 't.txt'
    tf = 'bt.txt'

    read_100_write(ff, tf)

main()
