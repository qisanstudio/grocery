# -*- coding: utf-8 -*-


# 【题目】如何仅用递归函数和栈操作逆序一个栈？
# 【描述】一个栈依次压入1、2、3、4、5，那么从栈顶到栈底依次为5、4、3、2、1，
# 将这个栈转置后，从栈顶到栈底为1、2、3、4、5，也就是实现栈中元素的逆序，
# 但是只能用递归函数来实现，不能借助此栈以外的数据结构。


def get_and_remove_stack_element(stk):
    result = stk.pop()
    if not stk:
        return result
    else:
        last = get_and_remove_stack_element(stk)
        stk.append(result)
        return last

def reverse(stk):
    if not stk:
        return
    i = get_and_remove_stack_element(stk)
    reverse(stk)
    stk.append(i)


if __name__ == '__main__':
    l = [1, 2, 3, 4, 5]
    reverse(l)
    print l
