# coding: utf-8
import random

ORDER = 3
LEN = 100000

f = open("./urlab.clean")
fc = f.read()
fc = fc.replace("\n", " \n ")

fc = fc.split(" ")
fc = filter(lambda x: not "http://" in x, fc)
fc = " ".join(fc)

fc = fc.replace(":", " : ")
fc = fc.split(" ")

fc = filter(lambda x: not x == "", fc)

fc = map(lambda x: x.replace(":)", "SM_CONTENT"), fc)
fc = map(lambda x: x.replace(":-)", "SM_CONTENT"), fc)
fc = map(lambda x: x.replace(":(", "SM_TRISTE"), fc)
fc = map(lambda x: x.replace(";)", "SM_COLON"), fc)

fc = map(lambda x: x.replace(",", ""), fc)
fc = map(lambda x: x.replace(")", ""), fc)
fc = map(lambda x: x.replace("(", ""), fc)

fc = map(lambda x: x.replace("SM_CONTENT", ":)"), fc)
fc = map(lambda x: x.replace("SM_TRISTE", ":("), fc)
fc = map(lambda x: x.replace("SM_COLON", ";)"), fc)


markov = {}

for i, word in enumerate(fc):
    key = []
    for j in range(i - ORDER, i):
        if j >= 0:
            key.append(fc[j])

    key = " ".join(key)
    val = markov.get(key, [])
    val.append(word)
    markov[key] = val

nicks = filter(lambda x: x.startswith("<"), fc)

nick = random.choice(nicks)
first = random.choice(filter(lambda x: x.startswith(nick), markov.keys()))
text = first.split(" ")
for i in range(LEN):
    word = " ".join(text[-ORDER:])
    text.append(random.choice(markov[word]))

open("result", "w").write(" ".join(text))
