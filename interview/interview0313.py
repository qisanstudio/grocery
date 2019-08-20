# -*- coding: utf-8 -*-


def quick(l):
    # 通过一趟排序将待排记录分隔成独立的两部分: 其中一部分记录的关键字均比另一部分的关键字小，则可分别对这两部分记录继续进行排序，以达到整个序列有序。
    # 升序
    front, end = 0, len(l) - 1
    sentry = 0
    while(end != front):
        if l[end] < l[sentry]:
            break
        end -= 1

    while(front != end):
        if l[front] > l[sentry]:
            break
        front += 1

    if front == end:
        l[sentry], l[front] = l[front], l[sentry]
    else:
        l[front], l[end] = l[end], l[front]


def test_quick():
    pass


if __name__ == '__main__':
    # test_bubble()
    test_quick()
