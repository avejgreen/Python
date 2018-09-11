

class Stepper(object):

    def __init__(self, **kwargs):

        """
        redundant attributes:
            freq, period
            dc_range, min, max, length
            position, dc

        """

        self.freq = 50
        self.dc_min = 5
        self.dc_max = 10
        self.position = 50
        self.usually = 'up'
        self.delta = 20

        for key in self.__dict__:
            if key in kwargs:
                self.__dict__[key] = kwargs[key]

    def get_dc(self):
        dc = self.dc_min + (self.position / 100) * \
                           (self.dc_max - self.dc_min)
        if self.usually is 'up':
            dc = 100 - dc
        return dc

    def move_up(self):
        if self.position + self.delta > 100:
            self.position = 100
        else:
            self.position += self.delta
        return self.position

    def move_down(self):
        if self.position - self.delta < 0:
            self.position = 0
        else:
            self.position -= self.delta
        return self.position

Step1 = Stepper()

Step1.move_up()

Step1.move_down()

test = 1
