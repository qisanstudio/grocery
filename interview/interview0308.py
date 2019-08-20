# -*- coding: utf-8 -*-
import random


def bubble(l):
    # 从序列头开始
    # 两两比对交换，直到最大(小)的在最末尾
    # [i, 0, 0, 0] : [被排序值, 向前移动次数, 向后移动次数, 移动总次数]
    tl = [[i, 0, 0, 0] for i in l]

    for i in range(len(tl)-1):
        swap_times = 0
        for j in range(len(tl)-i-1):
            if tl[j][0] > tl[j+1][0]:
                tl[j][2] += 1
                tl[j+1][1] -= 1
                tl[j][3] += 1
                tl[j+1][3] += 1
                tl[j], tl[j+1] = tl[j+1], tl[j]
                swap_times += 1
        if swap_times == 0:
            break

    return tl


def test_bubble():
    # 【1-3】试分别举出实例说明，在对包含n个元素序列做起泡排序的过程中，可能发生以下情况：

    # case0 = list(range(100))
    # random.shuffle(case0)
    # r0 = bubble(case0)
    # print("case0: %s -> %s" % (case0, r0))

    # 情况一：任何元素都无需移动
    case1 = [1, 2, 3, 4]    # 答案 1，2，3，4
    r1 = bubble(case1)
    print("case1: %s -> %s" % (case1, r1))

    # 情况二：某元素会一度(朝远离其最终位置的方向)逆向移动
    case2 = [4, 3, 1, 2]    # 答案 3
    r2 = bubble(case2)
    print("case2: %s -> %s" % (case2, r2))

    # 情况三：某元素的初始位置与其最终位置相邻，甚至已经处于最终位置，却需要参与n-1次交换
    case3 = [4, 5, 3, 2, 1]    # 答案 3
    r3 = bubble(case3)
    print("case3: %s -> %s" % (case3, r3))

    # 情况四：所有元素都需要参与n-1次交换
    case4 = [4, 3, 2, 1]    # 答案 倒序
    r4 = bubble(case4)
    print("case4: %s -> %s" % (case4, r4))


def bubble_times(l):
    times = 0

    for i in range(len(l)-1):
        swap_times = 0
        for j in range(len(l)-i-1):
            times += 1
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]
                times += 1
                swap_times += 1
        if swap_times == 0:
            break

    return times


def test_bubble_times():
    # 最坏时间复杂度 O(n^{2})
    # 最优时间复杂度 O(n)
    # 平均时间复杂度 O(n^{2})
    # 稳定性：稳定
    # 空间复杂度 总共O(n)，需要辅助空间O(1)
    last_times = 0
    for total in range(30):
        best_case = list(range(total))
        bad_case = list(range(total, -1, -1))
        best_times = bubble_times(best_case)
        bad_times = bubble_times(bad_case)
        print("total: %s, best_times: %s, bad_times: %s" % (total, best_times, bad_times))
    return


if __name__ == '__main__':
    # test_bubble()
    test_bubble_times()
