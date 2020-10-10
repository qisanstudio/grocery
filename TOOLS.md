## install compare code tools
1. download Beyond Compare & install
2. cat /usr/local/bin/compare
```
#! /bin/bash

rm /Users/qisan/Library/Application\ Support/Beyond\ Compare/registry.dat
/Users/qisan/Applications/Beyond\ Compare.app/Contents/MacOS/BCompare $@
```
3. $ compare a.txt b.txt
4. TODO can not support params
