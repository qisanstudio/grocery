# -*- coding: utf-8 -*-


# 【题目】
#     实现一个特殊的栈，在实现栈的基本功能的基础上，再实现返回栈中最小元素的操作。
# 【要求】
#     1. pop、push、get_min 操作的时间复杂度都是O(1)
#     2. 设计的栈类型可以使用现成的栈结构


class SelfMinValueStack(object):

    def __init__(self):
        self.min = -1
        self.top = -1
        self.data = []

    def push(self, value):
        self.data.append(value)
        self.top += 1
        if self.min == -1:
            self.min = self.top
        else:
            if self.data[self.min] >= self.data[self.top]:
                self.min = self.top

    def pop(self):
        if self.top == -1:
            raise IndexError('stack out of range')
        result = self.data.pop()
        if self.top == self.min:
            self.min = -1
            self._calc_min()

        self.top -= 1
        return result

    def get_min(self):
        if self.min == -1:
            return
        return self.data[self.min]

    def _calc_min(self):
        if len(self.data) == 0:
            self.min = -1
        else:
            self.min = 0
        for i in xrange(len(self.data)):
            if self.data[self.min] > self.data[i]:
                self.min = i


class StandardMinValueStack(object):

    def __init__(self):
        self.data_top = -1
        self.min_top = -1
        self.data_stack = []
        self.min_stack = []

    def push(self, value):
        self.data_stack.append(value)
        self.data_top += 1
        if self.min_top == -1:
            self.min_stack.append(value)
            self.min_top += 1
        else:
            if value <= self.min_stack[self.min_top]:
                self.min_stack.append(value)
                self.min_top += 1

    def pop(self):
        if self.data_top == -1:
            raise IndexError('stack out of range')
        value = self.data_stack.pop()
        self.data_top -= 1
        if value == self.min_stack[self.min_top]:
            self.min_stack.pop()
            self.min_top -= 1
        return value

    def get_min(self):
        if self.min_top == -1:
            return
        return self.min_stack[self.min_top]


def test_self():
    s = SelfMinValueStack()
    l = [10, 8, 4, 4, 2, 1, 3, 5, 7, 9]
    for i in l:
        s.push(i)
        m = s.get_min()
        print s.data, m
    for i in xrange(len(l)):
        s.pop()
        m = s.get_min()
        print s.data, m


class ExpertMinValueStack():

    def __init__(self):
        # TODO min_stack 还可以记录data_stack的下标
        pass


def test_standard():
    s = StandardMinValueStack()
    l = [10, 8, 4, 4, 2, 1, 3, 5, 7, 9]
    for i in l:
        s.push(i)
        m = s.get_min()
        print s.data_stack, m
    for i in xrange(len(l)):
        s.pop()
        m = s.get_min()
        print s.data_stack
        print s.min_stack


if __name__ == '__main__':
    test_self()
    test_standard()

