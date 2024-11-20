from Animal import Animal

"""
b) Bird (inherits from Animal):
Additional Attributes:
• wing_span (float): The wingspan of the bird in meters.
• can_fly (boolean): Indicates whether the bird can fly.
Additional Methods:
• is_endangered(wing_span_threshold: int): Returns True if the bird species is endangered,
otherwise False. Species with a wingspan below a threshold are endangered.
• __str__(): Returns a string representation of a bird.
"""

wing_span_threshold = 2.7

class Bird(Animal):
    def __init__(self, name, species, age, wing_span, can_fly):
        super().__init__(name, species, age)
        self.wing_span = wing_span
        self.can_fly = can_fly


    def is_endangered(self):
        return self.wing_span < wing_span_threshold


    def __str__(self):
        fly_status = "Can fly" if self.can_fly else "Cannot fly"
        return (str(self.name)
                + " (" + str(self.species) + "), Wingspan: " + str(self.wing_span)
                + "m, " + fly_status
                +", Age: " + str(self.age) + " years")