import re

fp = open("compiler/a.ir")
fp1= open("compiler/a.eg", "w+")

for line in fp:
    fp1.write(re.sub('[(){}<>]', '', line))
