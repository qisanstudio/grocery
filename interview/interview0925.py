# -*- coding: utf-8 -*-


class MinValueStack(object):

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
            # todo change to right except
            raise Exception('out of range')
        if self.top == self.min:
            self.min = 1
            self._calc_min()
        self.top -= 1
        return self.data.pop()

    def get_min(self):
        if self.min == -1:
            raise Exception('out of range')
        return self.data[self.min]

    def _calc_min(self):
        if len(self.data) == 0:
            self.min = -1
        else:
            self.min = 0
        for i in xrange(len(self.data)):
            if self.data[self.min] > self.data[i]:
                self.min = i


if __name__ == '__main__':
    s = MinValueStack()
    