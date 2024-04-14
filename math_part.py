import math
class MathFunctions:

    math_list : list = []

    def __init__(self, *input_data) -> None:
        data_list = list(input_data)
        self.math_list = data_list

    def distance(self) -> float:
        return ((self.math_list[2] - self.math_list[0]) ** 2 + (self.math_list[3] - self.math_list[1]) ** 2) ** 0.5
    
    def hyp_cordinates(self) -> tuple:
        return (
            self.math_list[0] + self.math_list[2] * math.cos(math.radians(self.math_list[3])),
            self.math_list[1] + self.math_list[2] * math.sin(math.radians(self.math_list[3])))
    
    def find_ang(self) -> float:
        if self.math_list[0] == self.math_list[2]:
            return 90
        if self.math_list[1] == self.math_list[3] and self.math_list[2] < self.math_list[0]:
            return 180
        if self.math_list[1] == self.math_list[3] and self.math_list[2] > self.math_list[0]:
            return 0
        dist = ((self.math_list[2] - self.math_list[0]) ** 2 +
                (self.math_list[3] - self.math_list[1]) ** 2) ** 0.5
        return math.degrees(math.acos((self.math_list[2] - self.math_list[0])/dist))
    
    #пересечение окружности и прямой
    def circle_straigth(self) -> list:
        straight_k = (self.math_list[3] - self.math_list[1])/ (self.math_list[2] - self.math_list[0])
        straight_b = self.math_list[3] - straight_k * self.math_list[2]
        asq = 1 + straight_k ** 2
        bsq = 2 * (-self.math_list[4] + straight_k * (straight_b - self.math_list[5]))
        csq = self.math_list[4] ** 2 + (straight_b - self.math_list[5]) ** 2 - self.math_list[6] ** 2
        if bsq ** 2 - 4 * asq * csq > 0:
            ret_x1 = (- bsq + (bsq ** 2 - 4 * asq * csq) ** 0.5)/(2 * asq)
            ret_x2 = (- bsq - (bsq ** 2 - 4 * asq * csq) ** 0.5)/(2 * asq)
            return [ret_x1, straight_k * ret_x1 + straight_b, ret_x2,
                    straight_k * ret_x2 + straight_b]
        if bsq ** 2 - 4 * asq * csq == 0:
            ret_x = 0.5 * bsq/asq
            return [ret_x, straight_k * ret_x + straight_b]
        return None
    
    def parallel_straight(self) -> tuple:
        straight_k = (self.math_list[3] - self.math_list[1]) / (self.math_list[2] - self.math_list[0])
        straight_b = self.math_list[5] - straight_k * self.math_list[4]
        return straight_k, straight_b
    
    #угол упреждения
    def method_ang(self) -> float:
        return math.degrees(math.asin((self.math_list[0] * math.sin(math.radians(self.math_list[1]))) / self.math_list[2]))