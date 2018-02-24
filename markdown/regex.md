#### version 0.1


import re


URL_PATTERN = r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)'

## 语法


## 作用

### 1. 校验

### 2. 切分

### 3. 分组


if __name__ == '__main__':
    test_urls = [
        'https://v.qq.com/x/cover/iqi6xvfp07qp6vt/x0549x5gov8.html',
    ]
    for url in test_urls:
        m = re.match(URL_PATTERN, url)
        if m:
            print m.groups()
        else:
            print 'match fail'
