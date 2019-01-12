
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


class Customer(object):
    
    def __init__(self, name, rentals=[]):
        self.name = name
        self.rentals = rentals

    def statement(self):
        result = ''
        total_amount = 0
        frequent_renter_points = 0

        for rental in self.rentals:
            this_amount = 0
            if rental.movie.price_code == Movie.REGULAR:
                this_amount += 2
                if rental.days > 2:
                    this_amount += (rental.days -2) * 1.5
            elif rental.movie.price_code == Movie.NEW_RELEASE:
                this_amount = rental.days * 3
            elif rental.movie.price_code == Movie.CHILDRENS:
                this_amount += 1.5
                if rental.days > 3:
                    this_amount += (rental.days - 3) * 1.5

            # add frequent renter points
            frequent_renter_points += 1
            # add bonus for a two day new release rental
            if (rental.movie.price_code == Movie.NEW_RELEASE) and (rental.days > 1):
                frequent_renter_points += 1

            # show figures for this rental
            result += '\t' + rental.movie.title + '\t' + str(this_amount) + '\n'
            total_amount += this_amount

        # add footer lines
        result += 'Amount owed is ' + str(total_amount) + '\n'
        result += 'You earned ' + str(frequent_renter_points) + ' frequent renter points'
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













