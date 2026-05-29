from abc import ABC, abstractmethod
import math
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    @classmethod
    def describe_shapes(cls):
        print("Shapes are fundamental geometric figures.")
    @staticmethod
    def get_pi():
        return math.pi
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return Shape.get_pi() * self.radius ** 2
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
circle = Circle(5)
rectangle = Rectangle(4, 6)
print(f"Circle area: {circle.area():.2f}")
print(f"Rectangle area: {rectangle.area()}")
Shape.describe_shapes()          
print(f"Value of pi: {Shape.get_pi():.5f}")   