import math

class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary


    # Method for modulus (absolute value)
    def abs(self):
        return math.sqrt(self.real ** 2 + self.imaginary ** 2)


    # Angle of a complex number shows its direction in the plane, measuring how far it is rotated from the positive real axis.
    def angle(self):
        return math.atan2(self.imaginary, self.real)


    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)


    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)


    # Real part: ac - bd = 1 * 4 - 2 * 0 = 4
    # Imaginary part: ad + bc = 1 * 0 + 2 * 4 = 8
    def __mul__(self, other):
        return ComplexNumber(self.real * other.real - self.imaginary * other.imaginary, self.real * other.imaginary + self.imaginary * other.real)


    # real = (self.real × other.real + self.imaginary × other.imaginary) / other.real ** 2 + other.imaginary ** 2: 1 * 4 + 2 * 0 / 4^2 + 0^2 = 4/16 = 0.25
    # imaginary = (self.imaginary × other.real − self.real × other.imaginary) / other.real ** 2 + other.imaginary ** 2: 2 * 4 - 1 * 0 / 4^2 + 0^2 = 8/16 = 0.50
    def __truediv__(self, other):
        denom = other.real ** 2 + other.imaginary ** 2
        real = (self.real * other.real + self.imaginary * other.imaginary) / denom
        imaginary = (self.imaginary * other.real - self.real * other.imaginary) / denom
        return ComplexNumber(real, imaginary)


    def __eq__(self, other):
        return self.real == other.real and self.imaginary == other.imaginary


    def __ne__(self, other):
        return self.real != other.real and self.imaginary != other.imaginary


    def __str__(self):
        if self.real == 0 and self.imaginary == 0:
            return 0
        elif self.real == 0:
            return str(self.imaginary) + "i"
        elif self.imaginary == 0:
            return str(self.real)

        if self.imaginary > 0:
            return str(self.real) + "+" + str(self.imaginary) + "i"
        else:
            return str(self.real * self.imaginary) + "i"


# Example usage
a = ComplexNumber(1, 2)
b = ComplexNumber(4, 0)
print(a) #1+2i
print(b) #4
print(a+b) #5+2i
print(a-b) #-3+2i
print(a*b) #4+8i
print(a/b) #0.25+0.5i
print(a==b) #False
print(a!=b) #True
