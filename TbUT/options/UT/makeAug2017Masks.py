#!/usr/bin/env python

with open("MambaMasks_P_1.dat","w") as f:
    for i in range(46):
        f.write("0\n")
    for i in range(46,128):
        if i==94 or i==123:
            f.write("0\n")
        else:
            f.write("1\n")
    for i in range(128,256):
        f.write("0\n")
    for i in range(256,384):
        if i==332:
            f.write("0\n")
        else:
            f.write("1\n")
    for i in range(384,512):
        f.write("0\n")
