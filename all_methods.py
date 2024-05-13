import math
from math_part import MathFunctions
class CatcherMethods:
    'класс методов перехватчика'
    __v_cx: list = []
    __v_cy: list = []
    __v_ax: list = []
    __v_ay: list = []
    __d_cx: list = []
    __d_cy: list = []
    __d_ax: list = []
    __d_ay: list = []
    __v_live_data: list = []
    __initial_data: list = []
    __d_live_data: list = []
    __aim_speed_x : int
    __aim_speed_y : int
    __aim_speed : int
    __catcher_speed: int
    def __init__(self, input_data) -> None:
        self.__initial_data = input_data["initial"]
        self.__pre_moments__()
    def __pre_moments__(self) -> None:
        
        xminus3, yminus3 = MathFunctions(50000, 0, self.__initial_data['aimRTMinus3'],
            self.__initial_data['aimPhiTMinus3']).hyp_cordinates()
        xminus2, yminus2 = MathFunctions(50000, 0, self.__initial_data['aimRTMinus2'],
            self.__initial_data['aimPhiTMinus2']).hyp_cordinates()
        
        self.__aim_speed_x = xminus2 - xminus3
        self.__aim_speed_y = yminus2 - yminus3
        self.__aim_speed = (self.__aim_speed_x ** 2 + self.__aim_speed_y ** 2) ** 0.5
        self.__catcher_speed = (self.__aim_speed_x ** 2 + self.__aim_speed_y ** 2) ** 0.5 \
        * self.__initial_data['rocketSpeedCoeff']
        ang0 = MathFunctions(50000, 0,
            xminus2 + 2 * self.__aim_speed_x, yminus2 + 2 * self.__aim_speed_y).find_ang()
        
        self.__v_cx.extend((50000, 50000))
        self.__v_cy.extend((0, 0))
        self.__v_ax.extend((xminus3, xminus2))
        self.__v_ay.extend((yminus3, yminus2))

        for i in range(1, 3):
            now_moment = {'moment' : -2, 'aimPhi' : 0, 'aimR' : 0,
                        'catcherPhi' : 0, 'catcherRho' : 0, 'distance' : 0}
            now_moment['moment'] += i
            now_moment['aimPhi'] = MathFunctions(50000, 0,
                xminus2 + i * self.__aim_speed_x, yminus2 + i * self.__aim_speed_y).find_ang()
            now_moment['aimR'] = MathFunctions(50000, 0,
                xminus2 + i * self.__aim_speed_x, yminus2 + i * self.__aim_speed_y).distance()
            now_moment['catcherPhi'] = ang0
            now_moment['catcherRho'] = i * self.__catcher_speed
            aim_x, aim_y = MathFunctions(50000, 0,
                now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
            catcher_x, catcher_y = MathFunctions(50000, 0,
                i * self.__catcher_speed, ang0).hyp_cordinates()
            now_moment['distance'] = MathFunctions(aim_x, aim_y,
                catcher_x, catcher_y).distance()
            self.__v_cx.append(catcher_x)
            self.__v_cy.append(catcher_y)
            self.__v_ax.append(aim_x)
            self.__v_ay.append(aim_y)
            self.__v_live_data.append(now_moment)

        aim_x = xminus2
        moment = 1
        self.__d_cx.extend((50000, 50000))
        self.__d_cy.extend((0, 0))
        self.__d_ax.extend((xminus3, xminus2))
        self.__d_ay.extend((yminus3, yminus2))

        while aim_x > 50000 and aim_x - 50000 > 2 * self.__aim_speed_x:
            now_moment = {'moment' : -2, 'aimPhi' : 0, 'aimR' : 0,
                        'catcherPhi' : 0, 'catcherRho' : 0, 'distance' : 0}
            now_moment['moment'] += moment
            now_moment['aimPhi'] = MathFunctions(50000, 0, xminus2 + moment * self.__aim_speed_x,
                yminus2 + moment * self.__aim_speed_y).find_ang()
            now_moment['aimR'] = MathFunctions(50000, 0, xminus2 + moment * self.__aim_speed_x,
                yminus2 + moment * self.__aim_speed_y).distance()
            now_moment['catcherPhi'] = 0
            now_moment['catcherRho'] =  0
            aim_x += self.__aim_speed_x
            cord_aimx, cordaim_y = \
                MathFunctions(50000, 0, now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
            cor_catcherx = 50000
            cor_catchery = 0
            self.__d_cx.append(cor_catcherx)
            self.__d_cy.append(cor_catchery)
            self.__d_ax.append(cord_aimx)
            self.__d_ay.append(cordaim_y)
            now_moment['distance'] = \
                MathFunctions(aim_x, yminus2 + self.__aim_speed_y * moment, 50000, 0).distance()
            moment += 1
            self.__d_live_data.append(now_moment)
        aimx, aimy = \
            MathFunctions(50000, 0, self.__d_live_data[len(self.__d_live_data) - 1]['aimR'],
                self.__d_live_data[len(self.__d_live_data) - 1]['aimPhi']).hyp_cordinates()
        ang0 = MathFunctions(50000, 0, aimx + self.__aim_speed_x * 2,
            aimy + self.__aim_speed_y * 2).find_ang()
        moment = 1

        while aim_x > 50000:
            now_moment = self.__d_live_data[len(self.__d_live_data) - 1]
            now_moment['moment'] += 1
            now_moment['aimPhi'] = MathFunctions(50000, 0, xminus2 + moment * self.__aim_speed_x,
                yminus2 + moment * self.__aim_speed_y).find_ang()
            now_moment['aimR'] = MathFunctions(50000, 0, xminus2 + moment * self.__aim_speed_x,
                yminus2 + moment * self.__aim_speed_y).distance()
            now_moment['catcherPhi'] = ang0
            now_moment['catcherRho'] =  moment * self.__catcher_speed
            aimx, aimy = \
                MathFunctions(50000, 0, now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
            catcher_x, catcher_y = \
                MathFunctions(50000, 0, moment * self.__catcher_speed, ang0).hyp_cordinates()
            now_moment['distance'] = MathFunctions(aim_x, aim_y, catcher_x, catcher_y).distance()
            moment += 1
            cord_aimx, cordaim_y =  \
                MathFunctions(50000, 0, now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
            cor_catcherx, cor_catchery = MathFunctions(50000, 0, now_moment['catcherRho'],
                now_moment['catcherPhi']).hyp_cordinates()
            self.__d_cx.append(cor_catcherx)
            self.__d_cy.append(cor_catchery)
            self.__d_ax.append(cord_aimx)
            self.__d_ay.append(cordaim_y)
            self.__d_live_data.append(now_moment)

    def three_points_method(self) -> tuple:
        while True:
            now_moment = self.__v_live_data[len(self.__v_live_data) - 1]
            
            if now_moment['distance'] > self.__initial_data['catchDistance']:
                catcherx, catchery = MathFunctions(50000, 0,
                    now_moment['catcherRho'], now_moment['catcherPhi']).hyp_cordinates()
                aimx, aimy = MathFunctions(50000, 0,
                    now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
                aimx += self.__aim_speed_x
                aimy += self.__aim_speed_y
                now_moment['moment'] += 1
                now_moment['aimPhi'] = MathFunctions(50000, 0, aimx, aimy).find_ang()
                now_moment['aimR'] = MathFunctions(50000, 0, aimx, aimy).distance()
                points = MathFunctions(50000, 0, aimx, aimy,
                    catcherx, catchery, self.__catcher_speed).circle_straigth()
                
                if len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() <= \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[0]
                    catchery = points[1]
                elif len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() >  \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[2]
                    catchery = points[3]
                elif len(points) == 2:
                    catcherx = points[0]
                    catchery = points[1]

                now_moment['distance'] = MathFunctions(catcherx, catchery, aimx, aimy).distance()
                now_moment['catcherPhi'] = MathFunctions(50000, 0, catcherx, catchery).find_ang()
                now_moment['catcherRho'] = MathFunctions(50000, 0, catcherx, catchery).distance()
                self.__v_live_data.append(now_moment)
                self.__v_cx.append(catcherx)
                self.__v_cy.append(catchery)
                self.__v_ax.append(aimx)
                self.__v_ay.append(aimy)
            else:
                break

        while True:
            now_moment = self.__d_live_data[len(self.__d_live_data) - 1]

            if now_moment['distance'] > self.__initial_data['catchDistance']:
                catcherx, catchery = MathFunctions(50000, 0,
                    now_moment['catcherRho'], now_moment['catcherPhi']).hyp_cordinates()
                aimx, aimy = MathFunctions(50000, 0,
                    now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
                aimx += self.__aim_speed_x
                aimy += self.__aim_speed_y
                now_moment['moment'] += 1
                now_moment['aimPhi'] = MathFunctions(50000, 0, aimx, aimy).find_ang()
                now_moment['aimR'] = MathFunctions(50000, 0, aimx, aimy).distance()
                points = MathFunctions(50000, 0, aimx, aimy,
                    catcherx, catchery, self.__catcher_speed).circle_straigth()
                
                if len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() <= \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[0]
                    catchery = points[1]
                elif len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() >  \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[2]
                    catchery = points[3]
                elif len(points) == 2:
                    catcherx = points[0]
                    catchery = points[1]

                now_moment['distance'] = MathFunctions(catcherx, catchery, aimx, aimy).distance()
                now_moment['catcherPhi'] = MathFunctions(50000, 0, catcherx, catchery).find_ang()
                now_moment['catcherRho'] = MathFunctions(50000, 0, catcherx, catchery).distance()
                self.__d_live_data.append(now_moment)
                self.__d_cx.append(catcherx)
                self.__d_cy.append(catchery)
                self.__d_ax.append(aimx)
                self.__d_ay.append(aimy)
            else:
                break

        return (self.__v_cx, self.__v_cy, self.__v_ax, self.__v_ay), \
            (self.__d_cx, self.__d_cy, self.__d_ax, self.__d_ay)

    def straightening_method_05(self) -> tuple:

        while True:
            now_moment = self.__v_live_data[len(self.__v_live_data) - 1]
            if now_moment['distance'] > self.__initial_data['catchDistance']:
                catcherx, catchery = MathFunctions(50000, 0, \
                    now_moment['catcherRho'], now_moment['catcherPhi']).hyp_cordinates()
                aimx, aimy = MathFunctions(50000, 0, \
                    now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
                aimx += self.__aim_speed_x
                aimy += self.__aim_speed_y
                now_moment['moment'] += 1
                now_moment['aimPhi'] = MathFunctions(50000, 0, aimx, aimy).find_ang()
                now_moment['aimR'] = MathFunctions(50000, 0, aimx, aimy).distance()
                deltas = abs(now_moment['aimR'] - now_moment['catcherRho'])
                space = abs(aimx - catcherx)
                height = abs(aimy - catchery)
                dspace = -abs(self.__aim_speed * \
                    math.cos(math.radians(now_moment['aimPhi'])) - self.__catcher_speed)
                dphi = abs(self.__aim_speed)/(height * (1 + (space/height) ** 2))

                if dspace < 0:
                    ang = now_moment['aimPhi'] - dphi * deltas / dspace
                else:
                    ang = now_moment['aimPhi'] + dphi * deltas / dspace

                points = MathFunctions(50000, 0, 50000 + now_moment['aimR'] * \
                    math.cos(math.radians(ang)), 0 + now_moment['aimR'] * \
                    math.sin(math.radians(ang)), catcherx, catchery, \
                    self.__catcher_speed).circle_straigth()

                if len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() <= \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[0]
                    catchery = points[1]
                elif len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() > \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[2]
                    catchery = points[3]
                elif len(points) == 2:
                    catcherx = points[0]
                    catchery = points[1]

                now_moment['distance'] = MathFunctions(catcherx, catchery, aimx, aimy).distance()
                now_moment['catcherPhi'] = MathFunctions(50000, 0, catcherx, catchery).find_ang()
                now_moment['catcherRho'] = MathFunctions(50000, 0, catcherx, catchery).distance()
                self.__v_live_data.append(now_moment)
                self.__v_ax.append(catcherx)
                self.__v_cy.append(catchery)
                self.__v_ax.append(aimx)
                self.__v_ay.append(aimy)
            else:
                break

        while True:
            now_moment = self.__d_live_data[len(self.__d_live_data) - 1]
            if now_moment['distance'] > self.__initial_data['catchDistance']:
                catcherx, catchery = MathFunctions(50000, 0, \
                    now_moment['catcherRho'], now_moment['catcherPhi']).hyp_cordinates()
                aimx, aimy = MathFunctions(50000, 0, \
                    now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
                aimx += self.__aim_speed_x
                aimy += self.__aim_speed_y
                now_moment['moment'] += 1
                now_moment['aimPhi'] = MathFunctions(50000, 0, aimx, aimy).find_ang()
                now_moment['aimR'] = MathFunctions(50000, 0, aimx, aimy).distance()
                deltas = abs(now_moment['aimR'] - now_moment['catcherRho'])
                space = abs(aimx - catcherx)
                height = abs(aimy - catchery)
                dspace = -abs(self.__aim_speed * \
                    math.cos(math.radians(now_moment['aimPhi'])) - self.__catcher_speed)
                dphi = abs(self.__aim_speed)/(height * (1 + (space/height) ** 2))

                if dspace < 0:
                    ang = now_moment['aimPhi'] - dphi * deltas / dspace
                else:
                    ang = now_moment['aimPhi'] + dphi * deltas / dspace

                points = MathFunctions(50000, 0, 50000 + now_moment['aimR'] * \
                    math.cos(math.radians(ang)), \
                    0 + now_moment['aimR'] * math.sin(math.radians(ang)), \
                    catcherx, catchery, self.__catcher_speed).circle_straigth()
                
                if len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() <= \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[0]
                    catchery = points[1]
                elif len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() > \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[2]
                    catchery = points[3]
                elif len(points) == 2:
                    catcherx = points[0]
                    catchery = points[1]

                now_moment['distance'] = MathFunctions(catcherx, catchery, aimx, aimy).distance()
                now_moment['catcherPhi'] = MathFunctions(50000, 0, catcherx, catchery).find_ang()
                now_moment['catcherRho'] = MathFunctions(50000, 0, catcherx, catchery).distance()
                self.__d_live_data.append(now_moment)
                self.__d_cx.append(catcherx)
                self.__d_cy.append(catchery)
                self.__d_ax.append(aimx)
                self.__d_ay.append(aimy)
            else:
                break

        return (self.__v_cx, self.__v_cy, self.__v_ax, self.__v_ay), \
            (self.__d_cx, self.__d_cy, self.__d_ax, self.__d_ay)
    def straightening_method_1(self) -> tuple:

        while True:
            now_moment = self.__v_live_data[len(self.__v_live_data) - 1]

            if now_moment['distance'] > self.__initial_data['catchDistance']:
                catcherx, catchery = MathFunctions(50000, 0, \
                    now_moment['catcherRho'], now_moment['catcherPhi']).hyp_cordinates()
                aimx, aimy = MathFunctions(50000, 0, \
                    now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
                aimx += self.__aim_speed_x
                aimy += self.__aim_speed_y
                now_moment['moment'] += 1
                now_moment['aimPhi'] = MathFunctions(50000, 0, aimx, aimy).find_ang()
                now_moment['aimR'] = MathFunctions(50000, 0, aimx, aimy).distance()
                deltas = abs(now_moment['aimR'] - now_moment['catcherRho'])
                space = abs(aimx - catcherx)
                height = abs(aimy - catchery)
                dspace = -abs(self.__aim_speed * \
                    math.cos(math.radians(now_moment['aimPhi'])) - self.__catcher_speed)
                dphi = abs(self.__aim_speed)/(height * (1 + (space/height) ** 2))

                if dspace < 0:
                    ang = now_moment['aimPhi'] - 0.5 * dphi * deltas / dspace
                else:
                    ang = now_moment['aimPhi'] + 0.5 * dphi * deltas / dspace

                points = MathFunctions(50000, 0, 50000 + now_moment['aimR'] * \
                    math.cos(math.radians(ang)), 0 + now_moment['aimR'] * \
                    math.sin(math.radians(ang)), catcherx, catchery, \
                    self.__catcher_speed).circle_straigth()
                
                if len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() <= \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[0]
                    catchery = points[1]
                elif len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() > \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[2]
                    catchery = points[3]
                elif len(points) == 2:
                    catcherx = points[0]
                    catchery = points[1]

                now_moment['distance'] = MathFunctions(catcherx, catchery, aimx, aimy).distance()
                now_moment['catcherPhi'] = MathFunctions(50000, 0, catcherx, catchery).find_ang()
                now_moment['catcherRho'] = MathFunctions(50000, 0, catcherx, catchery).distance()
                self.__v_live_data.append(now_moment)
                self.__v_cx.append(catcherx)
                self.__v_cy.append(catchery)
                self.__v_ax.append(aimx)
                self.__v_ay.append(aimy)
            else:
                break

        while True:
            now_moment = self.__d_live_data[len(self.__d_live_data) - 1]

            if now_moment['distance'] > self.__initial_data['catchDistance']:
                catcherx, catchery = MathFunctions(50000, 0, \
                    now_moment['catcherRho'], now_moment['catcherPhi']).hyp_cordinates()
                aimx, aimy = MathFunctions(50000, 0, \
                    now_moment['aimR'], now_moment['aimPhi']).hyp_cordinates()
                aimx += self.__aim_speed_x
                aimy += self.__aim_speed_y
                now_moment['moment'] += 1
                now_moment['aimPhi'] = MathFunctions(50000, 0, aimx, aimy).find_ang()
                now_moment['aimR'] = MathFunctions(50000, 0, aimx, aimy).distance()
                deltas = abs(now_moment['aimR'] - now_moment['catcherRho'])
                space = abs(aimx - catcherx)
                height = abs(aimy - catchery)
                dspace = -abs(self.__aim_speed * \
                    math.cos(math.radians(now_moment['aimPhi'])) - self.__catcher_speed)
                dphi = abs(self.__aim_speed)/(height * (1 + (space/height) ** 2))

                if dspace < 0:
                    ang = now_moment['aimPhi'] - 0.5 * dphi * deltas / dspace
                else:
                    ang = now_moment['aimPhi'] + 0.5 * dphi * deltas / dspace

                points = MathFunctions(50000, 0, 50000 + now_moment['aimR'] * \
                    math.cos(math.radians(ang)), \
                    0 + now_moment['aimR'] * math.sin(math.radians(ang)), \
                    catcherx, catchery, self.__catcher_speed).circle_straigth()
                
                if len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() <= \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[0]
                    catchery = points[1]
                elif len(points) == 4 and \
                    MathFunctions(points[0], points[1], aimx, aimy).distance() > \
                    MathFunctions(points[2], points[3], aimx, aimy).distance():
                    catcherx = points[2]
                    catchery = points[3]
                elif len(points) == 2:
                    catcherx = points[0]
                    catchery = points[1]

                now_moment['distance'] = MathFunctions(catcherx, catchery, aimx, aimy).distance()
                now_moment['catcherPhi'] = MathFunctions(50000, 0, catcherx, catchery).find_ang()
                now_moment['catcherRho'] = MathFunctions(50000, 0, catcherx, catchery).distance()
                self.__d_live_data.append(now_moment)
                self.__d_cx.append(catcherx)
                self.__d_cy.append(catchery)
                self.__d_ax.append(aimx)
                self.__d_ay.append(aimy)
            else:
                break
            
        return (self.__v_cx, self.__v_cy, self.__v_ax, self.__v_ay), \
            (self.__d_cx, self.__d_cy, self.__d_ax, self.__d_ay)