'''
用户开始提出新的需求：
    1. 准备修改影片分类规则
    注意：虽然还不清楚分类方法，但与之对应的费用计算方式&常客积分方式还有待决定

重构二：进入费用计算&常客积分计算中，把因条件而异的代码(get_charge()中的if...else)替换掉
    实践步骤1. 运用多态取代与价格相关的条件逻辑, 在Movie类里添加了get_charge()和get_frequent_renter_points()方法。
    这样就把根据影片类型而变化的所有东西，都放到了影片类型所属的类中。
    实践步骤2. 我们有多种影片类型，它们以不同的方式回答相同的问题。很像子类的工作。用继承机制来解决。
    遇到问题：一部影片可以在生命周期内修改自己的分类，一个对象却不能在生命周期内修改自己所属的类。
    解决办法：
        首先，运用Replace Type Code with State/Strategy
        然后，将switch语句移到Price类
        最后，运用Replace Conditional with Polymorphism 去掉 switch 语句
'''

import abc


class Price(object):

    @abc.abstractmethod
    def get_price_code(self):
        """
        :return: price_code
        """

    @abc.abstractmethod
    def get_charge(self, rental_days):
        """
        :param rental_days:
        :return: charge
        """

    def get_frequent_renter_points(self, rental_days):
        return 1


class RegularPrice(Price):

    def get_price_code(self):
        return Movie.REGULAR

    def get_charge(self, rental_days):
        result = 2
        if rental_days > 2:
            result += (rental_days - 2) * 1.5
        return result


class NewReleasePrice(Price):

    def get_price_code(self):
        return Movie.NEW_RELEASE

    def get_charge(self, rental_days):
        result = rental_days * 3
        return result

    def get_frequent_renter_points(self, rental_days):
        if rental_days > 1:
            return 2
        else:
            return 1


class ChildrensPrice(Price):

    def get_price_code(self):
        return Movie.CHILDRENS

    def get_charge(self, rental_days):
        result = 1.5
        if rental_days > 3:
            result += (rental_days - 3) * 1.5

        return result


class Movie(object):
    REGULAR = 0
    NEW_RELEASE = 1
    CHILDRENS = 2

    def __init__(self, title):
        self.title = title
        self._price = Price()

    def get_price_code(self):
        return self._price.get_price_code()

    def set_price_code(self, price_code):
        if price_code == Movie.REGULAR:
            self._price = RegularPrice()
        elif price_code == Movie.NEW_RELEASE:
            self._price = NewReleasePrice()
        elif price_code == Movie.CHILDRENS:
            self._price = ChildrensPrice()
        else:
            raise ValueError("error price code")

    def get_charge(self, rental_days):
        return self._price.get_charge(rental_days)


class Rental(object):

    def __init__(self, movie, days):
        self.movie = movie
        self.days = days

    def get_charge(self):
        return self.movie.get_charge(self.days)

    def get_frequent_renter_points(self):
        return self.movie._price.get_frequent_renter_points(self.days)


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
    regular_movie = Movie('regular_movie')
    regular_movie.set_price_code(Movie.REGULAR)
    new_release_movie = Movie('new_release_movie')
    new_release_movie.set_price_code(Movie.NEW_RELEASE)
    childrens_movie = Movie('childrens_movie')
    childrens_movie.set_price_code(Movie.CHILDRENS)

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
