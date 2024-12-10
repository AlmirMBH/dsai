import numpy as np
import matplotlib.pyplot as plt
"""
Create a class Polynomial that represents a polynomial P (x) and has 6 instance variables:
    • coefs - list of coefficients for the polynomial (starting from the smallest term)
    • xmin - lower limit for x
    • xmax - upper limit for x
    • numx - number of data points for x
    • x - data for x axis
    • y - data for y axis
- Variables x and y are calculated, while others are defined in the constructor.
- If xmin is greater than xmax, raise a ValueError with a message (xmax must be greater than xmin!).
- Create method createData that creates the arrays for variables x and y where y= P(x).
- Create method plotData that creates a graph using matplotlib library based on x and y variables.
- Finally, enable the use of + operator for adding two polynomials that adds the values from the lists of
coefficients and keeps the values xmin, xmax and numx from the first polynomial.
"""

class Polynomial:
    def __init__(self, coefs, xmin, xmax, numx):
        if xmin > xmax:
            raise ValueError("xmax must be greater than xmin!")
        self.coefs = coefs
        self.xmin = xmin
        self.xmax = xmax
        self.numx = numx
        self.x = None
        self.y = None


    def createData(self):
        self.x = np.linspace(self.xmin, self.xmax, self.numx) # coef * x^i
        self.y = sum(coefficient * self.x ** i for i, coefficient in enumerate(self.coefs))


    def plotData(self):
        if self.x is None or self.y is None:
            print("Data not generated yet. Call createData first.")
            return

        plt.plot(self.x, self.y, label="Polynomial Curve")
        plt.xlabel("X-axis")
        plt.ylabel("P(x)-axis")
        plt.title("Polynomial plot")
        plt.legend()
        plt.grid(True)
        plt.show()


    def __add__(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("The operands must be Polynomial instances.")

        if self.xmin != other.xmin or self.xmax != other.xmax or self.numx != other.numx:
            raise ValueError("The polynomial must have the same xmin, xmax, and numx to be added.")
        new_coefficients = [
            (self.coefs[i] if i < len(self.coefs) else 0) + (other.coefs[i] if i < len(other.coefs) else 0)
            for i in range(max(len(self.coefs), len(other.coefs))) # take the longer list
        ]

        return Polynomial(new_coefficients, self.xmin, self.xmax, self.numx)


# Create the two polynomials (1+2x+3x^2)
p1 = Polynomial([1, 2, 3], -10, 10, 1000)
p1.createData()
p1.plotData()

p2 = Polynomial([4, 5, 6], -10, 10, 1000)
p2.createData()
p2.plotData()

# Add the two polynomials
p3 = p1 + p2
p3.createData()
p3.plotData()
