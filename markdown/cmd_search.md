#### version 0.1

http://www.ruanyifeng.com/blog/2009/10/5_ways_to_search_for_files_using_the_terminal.html

## 查找命令
find
locate
whereis
which
type

## 辅助命令
xargs
grep
sed
awk

### 情况一：递归搜索所有叫 install.txt 的文件下的 包含click字符串的文件 及对应行数
>>> grep --include=install.txt click -r . -n

### 情况二：当面目录及子目录下，所有文件名包含sitemap的文件路径
>>> find . -name '*sitemap*'
