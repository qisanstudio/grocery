# -*- coding: utf-8 -*-


# 【题目】快速排序
# 【描述】


def quick_sort(l):
    # 分解
    sentry = 0
    start, end = 0, len(l)-1
    while(start != end):
        if l[sentry] < l[end]:
            break
        end -= 1

    while(start != end):
        if l[sentry] > l[]

    # 排序
    # 合并
    return l


if __name__ == '__main__':
    l1 = [1, 4, 2, 3, 5]
    r1 = quick_sort(l1)
    print(r1)
