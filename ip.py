# coding: utf-8
f = open("./#urlab.log")
fc = f.readlines()
fc = filter(lambda x: not x.startswith("---"), fc)
fc = filter(lambda x: not x[6:].startswith("-!-"), fc)
fc = filter(lambda x: not x[6:].startswith("::"), fc)
fc = map(lambda x: "<" + x[8:], fc)
fc = filter(lambda x: not x == "<", fc)
open("urlab.clean", "w").write("".join(fc))
