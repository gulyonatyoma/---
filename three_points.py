import matplotlib.pyplot as plt
from math import *

plt.style.use('ggplot')

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def hyp_cordinates(x1, y1, dist, ang):
    return x1 + dist * cos(radians(ang)), y1 + dist * sin(radians(ang))

def find_ang(x1, y1, x2, y2):
    if x1 == x2:
        return 90
    if y1 == y2 and x2 < x1:
        return 180
    if y1 == y2 and x1 > x2:
        return 0
    dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return degrees(acos((x2 - x1)/dist))

def circle_straigth(x1, y1, x2, y2, xc, yc, r):
    k = (y2 - y1)/(x2 - x1)
    b = y2 - k * x2
    asq = 1 + k ** 2
    bsq = 2 * (-xc + k * (b - yc))
    csq = xc ** 2 + (b - yc) ** 2 - r ** 2
    if bsq ** 2 - 4 * asq * csq > 0:
        x1 = (- bsq + (bsq ** 2 - 4 * asq * csq) ** 0.5)/(2 * asq)
        x2 = (- bsq - (bsq ** 2 - 4 * asq * csq) ** 0.5)/(2 * asq)
        return [x1, k * x1 + b, x2, k * x2 + b]
    if bsq ** 2 - 4 * asq * csq == 0:
        x = 0.5 * bsq/asq
        return [x, k * x + b]
    return None

json_data = {
    "initial":
    {
        "baseX": 50000,
        "baseY": 0,
        "aimPhiTMinus3": 40,
        "aimRTMinus3": 49680,
        "aimPhiTMinus2": 41,
        "aimRTMinus2": 47880,
        "rocketSpeedCoeff": 2,
        "oneTimeInterval": 0.5,
        "catchDistance": 1000
    },
    "fly": [
    ]
}

initial_data = json_data["initial"]
live_data = json_data["fly"]

xminus3, yminus3 = hyp_cordinates(50000, 0, initial_data['aimRTMinus3'], initial_data['aimPhiTMinus3'])
xminus2, yminus2 = hyp_cordinates(50000, 0, initial_data['aimRTMinus2'], initial_data['aimPhiTMinus2'])

aim_speed_x = xminus2 - xminus3
aim_speed_y = yminus2 - yminus3
aim_speed =  (aim_speed_x ** 2 + aim_speed_y ** 2) ** 0.5
catcher_speed = initial_data['rocketSpeedCoeff'] * aim_speed
ang0 = find_ang(50000, 0, xminus2 + 2 * aim_speed_x, yminus2 + 2 * aim_speed_y)

#массивы для чертежей и анимаций
v_cx = []
v_cy = []
v_ax = []
v_ay = []
d_cx = []
d_cy = []
d_ax = []
d_ay = []

v_cx.extend((50000, 50000))
v_cy.extend((0, 0))
v_ax.extend((xminus3, xminus2))
v_ay.extend((yminus3, yminus2))

for i in range(1, 3):
    now_moment = {'moment' : -2, 'aimPhi' : 0, 'aimR' : 0,
                  'catcherPhi' : 0, 'catcherRho' : 0, 'distance' : 0}
    now_moment['moment'] += i
    now_moment['aimPhi'] = find_ang(50000, 0, xminus2 + i * aim_speed_x, yminus2 + i * aim_speed_y)
    now_moment['aimR'] = distance(50000, 0, xminus2 + i * aim_speed_x, yminus2 + i * aim_speed_y)
    now_moment['catcherPhi'] = ang0
    now_moment['catcherRho'] =  i * catcher_speed

    x1, y1 = hyp_cordinates(50000, 0, now_moment['aimR'], now_moment['aimPhi'])
    x2, y2 = hyp_cordinates(50000, 0, i * catcher_speed, ang0)

    now_moment['distance'] = distance(x1, y1, x2, y2)
    live_data.append(now_moment)

    #массивы для встречи заполнение
    v_cx.append(x2)
    v_cy.append(y2)
    v_ax.append(x1)
    v_ay.append(y1)

while True:
    now_moment = live_data[len(live_data) - 1]
    
    if now_moment['distance'] > initial_data['catchDistance']:
        catcherx, catchery = hyp_cordinates(50000, 0, now_moment['catcherRho'], now_moment['catcherPhi'])
        aimx, aimy = hyp_cordinates(50000, 0, now_moment['aimR'], now_moment['aimPhi'])
        
        aimx += aim_speed_x
        aimy += aim_speed_y

        now_moment['moment'] += 1
        now_moment['aimPhi'] = find_ang(50000, 0, aimx, aimy)        
        now_moment['aimR'] = distance(50000, 0, aimx, aimy)

        points = circle_straigth(50000, 0, aimx, aimy, catcherx, catchery, catcher_speed)

        if len(points) == 4 and distance(points[0], points[1], aimx, aimy) <= distance(points[2], points[3], aimx, aimy):
            catcherx = points[0]
            catchery = points[1]
        elif len(points) == 4 and distance(points[0], points[1], aimx, aimy) > distance(points[2], points[3], aimx, aimy):
            catcherx = points[2]
            catchery = points[3]
        elif len(points) == 2:
            catcherx = points[0]
            catchery = points[1]       
        now_moment['distance'] = distance(catcherx, catchery, aimx, aimy)
        now_moment['catcherPhi'] = find_ang(50000, 0, catcherx, catchery)
        now_moment['catcherRho'] = distance(50000, 0, catcherx, catchery)

        live_data.append(now_moment)
        
        #массивы для встречи заполнение
        v_cx.append(catcherx)
        v_cy.append(catchery)
        v_ax.append(aimx)
        v_ay.append(aimy)
    else: 
        break

print(live_data)

#догон
json_data = {
    "initial":
    {
        "baseX": 50000,
        "baseY": 0,
        "aimPhiTMinus3": 40,
        "aimRTMinus3": 49680,
        "aimPhiTMinus2": 41,
        "aimRTMinus2": 47880,
        "rocketSpeedCoeff": 2,
        "oneTimeInterval": 0.5,
        "catchDistance": 1000
    },
    "fly": [
    ]
}

initial_data = json_data["initial"]
live_data = json_data["fly"]

xminus3, yminus3 = hyp_cordinates(50000, 0, initial_data['aimRTMinus3'], initial_data['aimPhiTMinus3'])
xminus2, yminus2 = hyp_cordinates(50000, 0, initial_data['aimRTMinus2'], initial_data['aimPhiTMinus2'])

aim_speed_x = xminus2 - xminus3
aim_speed_y = yminus2 - yminus3
aim_speed =  (aim_speed_x ** 2 + aim_speed_y ** 2) ** 0.5
catcher_speed = initial_data['rocketSpeedCoeff'] * aim_speed
ang0 = find_ang(50000, 0, xminus2 + 2 * aim_speed_x, yminus2 + 2 * aim_speed_y)
aim_x = xminus2
moment = 1

d_cx.extend((50000, 50000))
d_cy.extend((0, 0))
d_ax.extend((xminus3, xminus2))
d_ay.extend((yminus3, yminus2))

while aim_x > 50000 and aim_x - 50000 > 2 * aim_speed_x:
    now_moment = {'moment' : -2, 'aimPhi' : 0, 'aimR' : 0,
                  'catcherPhi' : 0, 'catcherRho' : 0, 'distance' : 0}
    now_moment['moment'] += moment
    now_moment['aimPhi'] = find_ang(50000, 0, xminus2 + moment * aim_speed_x, yminus2 + moment * aim_speed_y)
    now_moment['aimR'] = distance(50000, 0, xminus2 + moment * aim_speed_x, yminus2 + moment * aim_speed_y)
    now_moment['catcherPhi'] = 0
    now_moment['catcherRho'] =  0
    aim_x += aim_speed_x

    #координаты для догона
    cord_aimx, cordaim_y = hyp_cordinates(50000, 0, now_moment['aimR'], now_moment['aimPhi'])
    cor_catcherx = 50000
    cor_catchery = 0
    
    #заполнение массивов для догона
    d_cx.append(cor_catcherx)
    d_cy.append(cor_catchery)
    d_ax.append(cord_aimx)
    d_ay.append(cordaim_y)
    
    now_moment['distance'] = distance(aim_x, yminus2 + aim_speed_y * moment, 50000, 0)
    live_data.append(now_moment)
    moment += 1

aimx, aimy = hyp_cordinates(50000, 0, live_data[len(live_data) - 1]['aimR'], live_data[len(live_data) - 1]['aimPhi'])
ang0 = find_ang(50000, 0, aimx + aim_speed_x * 2, aimy + aim_speed_y * 2)
i = 1

while aim_x > 50000:
    now_moment = live_data[len(live_data) - 1]
    now_moment['moment'] += 1
    now_moment['aimPhi'] = find_ang(50000, 0, xminus2 + i * aim_speed_x, yminus2 + i * aim_speed_y)
    now_moment['aimR'] = distance(50000, 0, xminus2 + i * aim_speed_x, yminus2 + i * aim_speed_y)
    now_moment['catcherPhi'] = ang0
    now_moment['catcherRho'] =  i * catcher_speed

    x1, y1 = hyp_cordinates(50000, 0, now_moment['aimR'], now_moment['aimPhi'])
    x2, y2 = hyp_cordinates(50000, 0, i * catcher_speed, ang0)

    now_moment['distance'] = distance(x1, y1, x2, y2)
    live_data.append(now_moment)
    i += 1

    #координаты для догона в конце
    cord_aimx, cordaim_y = hyp_cordinates(50000, 0, now_moment['aimR'], now_moment['aimPhi'])
    cor_catcherx, cor_catchery = hyp_cordinates(50000, 0, now_moment['catcherRho'], now_moment['catcherPhi'])
                                                                                               
    #заполнение массивов для догона
    d_cx.append(cor_catcherx)
    d_cy.append(cor_catchery)
    d_ax.append(cord_aimx)
    d_ay.append(cordaim_y)

while True:
    now_moment = live_data[len(live_data) - 1]
    
    if now_moment['distance'] > initial_data['catchDistance']:
        catcherx, catchery = hyp_cordinates(50000, 0, now_moment['catcherRho'], now_moment['catcherPhi'])
        aimx, aimy = hyp_cordinates(50000, 0, now_moment['aimR'], now_moment['aimPhi'])
                                                                                               
        aimx += aim_speed_x
        aimy += aim_speed_y

        now_moment['moment'] += 1
        now_moment['aimPhi'] = find_ang(50000, 0, aimx, aimy)        
        now_moment['aimR'] = distance(50000, 0, aimx, aimy)

        points = circle_straigth(50000, 0, aimx, aimy, catcherx, catchery, catcher_speed)

        if len(points) == 4 and distance(points[0], points[1], aimx, aimy) <= distance(points[2], points[3], aimx, aimy):
            catcherx = points[0]
            catchery = points[1]
        elif len(points) == 4 and distance(points[0], points[1], aimx, aimy) > distance(points[2], points[3], aimx, aimy):
            catcherx = points[2]
            catchery = points[3]
        elif len(points) == 2:
            catcherx = points[0]
            catchery = points[1]       

        now_moment['distance'] = distance(catcherx, catchery, aimx, aimy)
        now_moment['catcherPhi'] = find_ang(50000, 0, catcherx, catchery)
        now_moment['catcherRho'] = distance(50000, 0, catcherx, catchery)

        live_data.append(now_moment)
        
        #заполнение массивов для догона
        d_cx.append(catcherx)
        d_cy.append(catchery)
        d_ax.append(aimx)
        d_ay.append(aimy)
    else: break