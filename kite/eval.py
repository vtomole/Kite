import re

tokenize = re.compile(r'''
    \d* \.? \d+ (?: E -? \d+)?                     | # number 
    SIN|COS|TAN|ATN|EXP|ABS|LOG|SQR|RND|INT|FN[A-Z]| # functions
    LET|READ|DATA|PRINT|GOTO|IF|FOR|NEXT|END       | # keywords
    DEF|GOSUB|RETURN|DIM|REM|TO|THEN|STEP|STOP     | # keywords
    [A-Z]\d? | # variable names (letter + optional digit)
    ".*?"    | # labels (strings in double quotes)
    <>|>=|<= | # multi-character relational operators
    \S         # any non-space single character ''', 
    re.VERBOSE).findall


print(tokenize('10 READ N'))
