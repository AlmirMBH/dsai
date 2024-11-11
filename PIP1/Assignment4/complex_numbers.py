import math

class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    # Method for modulus (absolute value)
    def abs(self):
        return math.sqrt(self.real ** 2 + self.imag ** 2)

    # Method for phase angle
    def angle(self):
        return math.atan2(self.imag, self.real)

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    # Overload * operator
    def __mul__(self, other):
        return ComplexNumber(self.real * other.real - self.imag * other.imag,
                             self.real * other.imag + self.imag * other.real)

    # Overload / operator
    def __truediv__(self, other):
        denom = other.real ** 2 + other.imag ** 2
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.imag * other.real - self.real * other.imag) / denom
        return ComplexNumber(real, imag)

    # Overload == operator
    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    # Overload != operator
    def __ne__(self, other):
        return self.real != other.real and self.imag != other.imag

    # String representation
    def __str__(self):
        if self.real == 0 and self.imag == 0:
            return "0"
        elif self.real == 0:
            return f"{self.imag}i"
        elif self.imag == 0:
            return str(self.real)

        if self.imag > 0:
            return f"{self.real}+{self.imag}i"
        else:
            return f"{self.real}{self.imag}i"


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
