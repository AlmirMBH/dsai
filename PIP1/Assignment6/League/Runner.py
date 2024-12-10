"""
1) Has instance variables:
    o Weight (positive float)
    o BestPlace (positive integer)
    o Pace (positive float)
    o Age (positive integer)
    o Name (string)
2) Constructor sets all instance variables and raises a ValueError if any variable has incorrect value
3) Method __str__ returns a string in following format:
    o (Name) is (Age) years old, weights ( Weight) kgs, runs at a pace of (Pace) m/s and his best place at
    a competition on was (BestPlace). place.
4)  Method getList returns a list with following format:
    o [Name, Weight, BestPlace, Pace, Age]
"""
class Runner:
    def __init__(self, name, weight, best_place, pace, age):
        if not (isinstance(weight, float) and weight > 0):
            raise ValueError("Weight must be a positive float.")
        if not (isinstance(best_place, int) and best_place > 0):
            raise ValueError("BestPlace must be a positive integer.")
        if not (isinstance(pace, float) and pace > 0):
            raise ValueError("Pace must be a positive float.")
        if not (isinstance(age, int) and age > 0):
            raise ValueError("Age must be a positive integer.")
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")

        self.name = name
        self.weight = weight
        self.best_place = best_place
        self.pace = pace
        self.age = age


    def __str__(self):
        return f"{self.name} is {self.age} years old, weighs {self.weight} kgs, runs at a pace of {self.pace} m/s and his best place at a competition was {self.best_place} place."


    def getList(self):
        return [self.name, self.weight, self.best_place, self.pace, self.age]