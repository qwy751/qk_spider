# -*- coding: utf-8 -*-
import os


def read_name():
    basedir = os.path.abspath(os.path.dirname(__file__))
    name_dict = dict()
    file = open(basedir + "/fp_definition.ini", "r", encoding='utf8')
    for line in file:
        line = line.strip()
        if line != "":
            temp = line.split(":")
            name_dict[temp[0]] = temp[1].strip().strip('\"')
    return name_dict


if __name__ == '__main__':
    names = read_name()
    print(names)
