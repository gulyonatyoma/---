import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
def distance_between_two_points(a: Point, b: Point):
    dx = (a.x - b.x) ** 2
    dy = (a.y - b.y) ** 2
    return (dx + dy) ** 0.5 

def straight_linear_angular_serif(a: Point, distance, angle):
    angle = math.radians(angle)
    dx = distance * math.cos(angle)
    dy = distance * math.sin(angle)
    x = a.x + dx
    y = a.y + dy
    return Point(x, y)

def reverse_linear_angular_notching(a: Point, b: Point):
    d = distance_between_two_points(a, b)
    dx = abs(a.x - b.x)
    angle = math.acos(dx / d)
    return math.degrees(angle)

def angle_between_straight_lines(a: Point, b: Point, c: Point, d: Point):
    k_ab = k_factor(a, b)
    k_cd = k_factor(c, d)

    if k_ab == -1 and k_cd == -1:
        if b.x - a.x == d.x - c.x == 0 or b.y - a.y == d.y - c.y == 0:
            angle = 0
        else:
            angle = 90
    elif k_ab == -1:
        angle = math.degrees(math.atan(k_cd))
    elif k_cd == -1:
        angle = math.degrees(math.atan(k_ab))
    else:
        angle = math.degrees(math.atan((abs(k_cd - k_ab) / (1 + k_ab * k_cd))))

    if angle > 90:
        return 180 - angle 
    return angle

def k_factor(a: Point, b: Point):
    k_ab = b.y - a.y
    if b.x - a.x == 0 or b.y - a.y == 0:
        return -1
    k_ab /= (b.x - a.x)
    return k_ab