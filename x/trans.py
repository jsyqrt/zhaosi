# coding: utf-8

import json

import jieba 
from bosonnlp import BosonNLP

nlp = BosonNLP('o9uEJKop.17505.Bh6hezGEy2z2')

def purge_sql_to_tuple(line):

    line = line.lstrip('INSERT INTO `track_extra_information` VALUES ')
    line = line.rstrip(';\n')
    line = line.replace('),(', ')\n(')
    return line + '\n'

def tuple_to_json_lines(line):
    
    line = line.replace('NULL', 'None')
    t = eval(line)
    return json.dumps({'id': t[0], 'content':t[4]}) + '\n'

def jieba_line(line):

    line = json.loads(line)
    line = line.get('content')
    line = ' | '.join(list(map(lambda x: x.strip('\n'), jieba.cut(line)))).rstrip('\n')
    line = line.replace(' ', '')
    line = line.replace('||', '|')
    line = line.rstrip('|')
    line = line + '\n'
    line = line.encode('utf8', errors='strict')
    return line

def boson_line(line):

    l = list(map(lambda x: json.loads(x).get('content'), line))
    result = list(map(lambda x:' | '.join(x.get('word')).replace(' ', '').replace('||', '| |'), nlp.tag(l)))
    result = '\n'.join(result) + '\n'
    result = result.encode('utf8', errors='ignore')
    return result

def read_1_write(ff, tf, func):

    with open(ff, 'r') as f:
        for line in f:
            line = func(line)
            with open(tf, 'a') as ft:
                ft.write(line)

def read_100_write(ff, tf, func):

    n = 100
    with open(ff, 'r') as f:
        lines = f.readlines()
        lines = [lines[i:i+n] for i in range(0, len(lines), n)]
        for line in lines:
            line = func(line)
            with open(tf, 'a') as ft:
                ft.write(line)

def get_pure_tei(ff, tf):
    import os
    os.system('tail -n 101 %s > %s1' % (ff, tf))
    os.system('head -n 88 %s1 > %s' % (tf, tf))
    os.system('rm %s1' % tf)

def get_diff(ff, tf):
    import os
    os.system('diff -u %s %s > diff.txt' % (ff, tf))

def main():

    teif = 'track_extra_info.sql'
    teifx = 'track_extra_info.txt'
    tplf = 'tuple_tei.txt'
    ff = 'content.txt'
    jf = 'jieba_result.txt'
    bf = 'boson_result.txt'

    #get_pure_tei(teif, teifx)
    #read_1_write(teifx, tplf, purge_sql_to_tuple)
    #read_1_write(tplf, ff, tuple_to_json_lines)
    #read_1_write(ff, jf, jieba_line)
    #read_100_write(ff, bf, boson_line)
    get_diff(jf, bf)

main()
