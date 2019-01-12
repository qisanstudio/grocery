'''
本地小步重构主要考虑：
    1. 如何把长长的函数切开
    2. 把小块的代码移到更合适的类
    3. 降低代码重复量，让新的函数更容易撰写

重构一：找出代码的逻辑泥团，并运用 Extract Method (本例一个明显的泥团就是 if ... else)
    实践步骤1. 找出函数内的局部变量和参数（rental<会被修改>、this_amount<未被修改>）
        注意：任何不会被修改的变量都可以被当成参数传入新的函数，会被修改的变量就要格外小心。
    实践步骤2. 如果不喜欢 amount_for() 函数里的变量名称，现在正是修改它们的时候。
        注意：好的代码应该清楚表达出自己的功能，变量名称是代码清晰的关键。
    实践步骤3. 观察 amount_for() 时，发现这个函数使用了来自Rental类的信息，却没有使用Customer类的信息。
    这很值得怀疑，因为绝大多数情况下，函数应该放在它所使用的数据的所属对象内。这里运用 Move Method,
    "适应新家"意味着去掉参数，此外也要变更函数名称。
    实践步骤4. 找出程序中对旧函数的所有引用点，并修改它们。
    实践步骤5. this_amount变得多余了，因为它接受了get_charge()的结果就不再有任何改变。
    这里运用 Replace Temp with Query把this_amount除去
    注意：尽量除去这一类临时变量，临时变量往往引发问题，他们会导致大量参数被传来传去。
    实践步骤6. 提炼"常客积分计算"代码

'''


class Movie(object):
    REGULAR = 0
    NEW_RELEASE = 1
    CHILDRENS = 2

    def __init__(self, title, price_code):
        self.title = title
        self.price_code = price_code

    def set_price_code(self, price_code):
        self.price_code = price_code


class Rental(object):

    def __init__(self, movie, days):
        self.movie = movie
        self.days = days

    def get_charge(self):
        result = 0
        if self.movie.price_code == Movie.REGULAR:
            result += 2
            if self.days > 2:
                result += (self.days - 2) * 1.5
        elif self.movie.price_code == Movie.NEW_RELEASE:
            result = self.days * 3
        elif self.movie.price_code == Movie.CHILDRENS:
            result += 1.5
            if self.days > 3:
                result += (self.days - 3) * 1.5

        return result

    def get_frequent_renter_points(self):
        # add frequent renter points
        frequent_renter_points = 1
        # add bonus for a two day new release rental
        if (self.movie.price_code == Movie.NEW_RELEASE) and (self.days > 1):
            frequent_renter_points += 1

        return frequent_renter_points


class Customer(object):

    def __init__(self, name, rentals=[]):
        self.name = name
        self.rentals = rentals

    def get_total_charge(self):
        result = 0
        for rental in self.rentals:
            result += rental.get_charge()

        return result

    def get_frequent_renter_points(self):
        result = 0
        for rental in self.rentals:
            result += rental.get_frequent_renter_points()

        return result

    def statement(self):
        result = ''

        for rental in self.rentals:
            # show figures for this rental
            result += '\t' + rental.movie.title + '\t' + str(rental.get_charge()) + '\n'

        # add footer lines
        result += 'Amount owed is ' + str(self.get_total_charge()) + '\n'
        result += 'You earned ' + str(self.get_frequent_renter_points()) + ' frequent renter points'
        return result


if __name__ == '__main__':
    regular_movie = Movie('regular_movie', Movie.REGULAR)
    new_release_movie = Movie('new_release_movie', Movie.NEW_RELEASE)
    childrens_movie = Movie('childrens_movie', Movie.CHILDRENS)

    r1 = Rental(regular_movie, days=1)
    r2 = Rental(new_release_movie, days=1)
    r3 = Rental(childrens_movie, days=1)
    r4 = Rental(regular_movie, days=2)
    r5 = Rental(new_release_movie, days=2)
    r6 = Rental(childrens_movie, days=2)
    r7 = Rental(regular_movie, days=3)
    r8 = Rental(new_release_movie, days=3)
    r9 = Rental(childrens_movie, days=3)

    c1 = Customer('c1', rentals=[r1, r2, r3])
    result = c1.statement()
    assert 'regular_movie\t2' in result
    assert 'new_release_movie\t3' in result
    assert 'childrens_movie\t1.5' in result
    assert 'Amount owed is 6.5' in result
    assert 'You earned 3 frequent renter points' in result

    c2 = Customer('c2', rentals=[r4, r5, r6])
    result = c2.statement()
    assert 'regular_movie\t2' in result
    assert 'new_release_movie\t6' in result
    assert 'childrens_movie\t1.5' in result
    assert 'Amount owed is 9.5' in result
    assert 'You earned 4 frequent renter points' in result

    c3 = Customer('c3', rentals=[r7, r8, r9])
    result = c3.statement()
    assert 'regular_movie\t3.5' in result
    assert 'new_release_movie\t9' in result
    assert 'childrens_movie\t1.5' in result
    assert 'Amount owed is 14.0' in result
    assert 'You earned 4 frequent renter points' in result

    print("OK!")
