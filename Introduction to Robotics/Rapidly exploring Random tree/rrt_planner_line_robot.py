import time
import random
import drawSample
import math
import _tkinter
import sys
import imageToRects
import csv

# display = drawSample.SelectRect(imfile=im2Small,keepcontrol=0,quitLabel="")

visualize = 1
prompt_before_next = 1  # ask before re-running sonce solved
SMALLSTEP = 10  # what our "local planner" can handle.

G = [[0], []]  # nodes, edges

world = 'world2.png'
s, obstacles = imageToRects.imageToRects(world)
XMAX = s[0]
YMAX = s[1]
AMAX = math.pi / 2
AMIN = - AMAX
MAXITER = 100000
r_length = 50

# goal/target
tx = 800.0
ty = 150.0
ta = 0.0
# start
start_x = 100.0
start_y = 630.0
start_a = 0.0

vertices = [[start_x, start_y, start_a]]

sigmax_for_randgen = XMAX / 2.0
sigmay_for_randgen = YMAX / 2.0
sigmaa_for_randgen = AMAX / 2.0

nodes = 0
edges = 1
maxvertex = 0
gauss = 0
angle = 2


def drawGraph(G):
    global vertices, nodes, edges
    if not visualize: return
    for i in G[edges]:
        if len(vertices) != 1:
            canvas.polyline([vertices[i[0]], vertices[i[1]]])


def genPoint():
    # TODO : Function to implement the sampling technique
    # Uniform distribution
    #       OR
    # Gaussian distribution with mean at the goal
    if gauss:
        x = random.gauss(tx, sigmax_for_randgen)
        y = random.gauss(ty, sigmay_for_randgen)
        a = random.gauss(ta, sigmaa_for_randgen)
    else:
        x = random.uniform(0, XMAX)
        y = random.uniform(0, YMAX)
        a = random.uniform(AMIN, AMAX)
    return [x, y, a]


def genvertex():
    vertices.append(genPoint())
    return len(vertices) - 1


def pointToVertex(p):
    vertices.append(p)
    return len(vertices) - 1


def pickvertex():
    return random.choice(range(len(vertices)))


def lineFromPoints(p1, p2):
    line = []
    llsq = 0.0  # line length squared
    for i in range(len(p1)):  # each dimension
        h = p2[i] - p1[i]
        line.append(h)
        llsq += h * h
    ll = math.sqrt(llsq)  # length
    # normalize line
    if ll <= 0: return [0, 0]
    for i in range(len(p1)):  # each dimension
        line[i] = line[i] / ll
    return line


def pointPointDistance(p1, p2):
    """ Return the distance between a pair of points (L2 norm). """
    llsq = 0.0  # line length squared

    for i in range(len(p1)):  # each dimension, general case
        h = p2[i] - p1[i]
        llsq = llsq + (h * h)
    return math.sqrt(llsq)


def closestPointToPoint(G, p2):
    dmin = 999999999
    for v in G[nodes]:
        p1 = vertices[v]
        # if abs(p1[angle]-p2[angle])> math.pi/2:
        #   p1[angle] +=180
        d = pointPointDistance(p1, p2)
        if d <= dmin:
            dmin = d
            close = v
    return close


def returnParent(k):
    """ Return parent note for input node k. """
    for e in G[edges]:
        if e[1] == k:
            if visualize: canvas.polyline([vertices[e[0]], vertices[e[1]]], style=3)

            v = vertices[e[0]]
            p1 = [0, 0]
            p2 = [0, 0]
            p1[0] = v[0] + math.cos(v[angle]) * r_length / 2
            p1[1] = v[1] + math.sin(v[angle]) * r_length / 2
            p2[0] = v[0] - math.cos(v[angle]) * r_length / 2
            p2[1] = v[1] - math.sin(v[angle]) * r_length / 2
            if visualize:  canvas.polyline([p1, p2], 5)
            return e[0]


def pickGvertex():
    try:
        edge = random.choice(G[edges])
    except:
        return pickvertex()
    v = random.choice(edge)
    return v


def redraw():
    canvas.clear()
    canvas.markit(start_x, start_y, r=SMALLSTEP)
    canvas.markit(tx, ty, r=SMALLSTEP)
    drawGraph(G)
    for o in obstacles: canvas.showRect(o, outline='blue', fill='blue')
    canvas.delete("debug")


def ccw(A, B, C):
    """ Determine if three points are listed in a counterclockwise order.
    For three points A, B and C. If the slope of the line AB is less than 
    the slope of the line AC then the three points are in counterclockwise order.
    See:  http://compgeom.cs.uiuc.edu/~jeffe/teaching/373/notes/x06-sweepline.pdf
    """
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    """ do lines AB and CD intersect? """
    i = ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
    # if i:
    #    canvas.polyline(  [ A,B ], style=4  , tags = ("debug"))
    #    canvas.polyline(  [ C,D ], style=4  , tags = ("debug"))
    # else:
    #    canvas.polyline(  [ A,B ], style=1  , tags = ("debug")) # green
    #    canvas.polyline(  [ C,D ], style=1  , tags = ("debug"))
    return i


def lineHitsRect(p1, p2, r):
    rline = ((r[0], r[1]), (r[0], r[3]))
    if intersect(p1, p2, rline[0], rline[1]): return 1
    rline = ((r[0], r[1]), (r[2], r[1]))
    if intersect(p1, p2, rline[0], rline[1]): return 1
    rline = ((r[0], r[3]), (r[2], r[3]))
    if intersect(p1, p2, rline[0], rline[1]): return 1
    rline = ((r[2], r[1]), (r[2], r[3]))
    if intersect(p1, p2, rline[0], rline[1]): return 1

    return 0


def inRect(p, rect, dilation):
    """ Return 1 in p is inside rect, dilated by dilation (for edge cases). """
    if p[0] < rect[0] - dilation: return 0
    if p[1] < rect[1] - dilation: return 0
    if p[0] > rect[2] + dilation: return 0
    if p[1] > rect[3] + dilation: return 0
    return 1


# TODO: Implement the rrt_search algorithm in this function.
def rrt_search(G, tx, ty, ta):
    # Implement the rrt_algorithm in this section of the code.
    # You should call genPoint() within this function to 
    # get samples from different distributions.

    dist_to_goal = pointPointDistance([start_x, start_y, start_a], [tx, ty, ta])
    lastnode = 1
    p1 = [0, 0]
    p2 = [0, 0]
    nb_iter = 0
    while dist_to_goal > SMALLSTEP and nb_iter < MAXITER:
        nb_iter += 1
        if visualize: canvas.events()
        p_random = genPoint()
        # only useful for gaussian distribution
        if p_random[0] != max(min(p_random[0], XMAX), 0) or p_random[1] != max(min(p_random[1], YMAX), 0):
            continue

        node_closest = closestPointToPoint(G, p_random)
        p_closest = vertices[node_closest]

        # If the difference between the current and sampled angles is > 90.
        # It is faster to turn in the other direction
        if   (p_closest[angle] - p_random[angle]) >  math.pi / 2: p_random[angle] += math.pi
        elif (p_closest[angle] - p_random[angle]) < -math.pi / 2: p_random[angle] -= math.pi

        # Create the new point. Note: phisically it doesn't make sense
        # to treat angles and distances the same way,but this works fine.
        line = lineFromPoints(p_closest, p_random)
        p_new = [0, 0, 0]
        for i in range(len(p_new)):
            p_new[i] = p_closest[i] + line[i] * SMALLSTEP

        # check that the angle of the robot is between -90 and 90
        if   p_new[angle] >  math.pi / 2: p_new[angle] -= math.pi
        elif p_new[angle] < -math.pi / 2: p_new[angle] += math.pi

        # start and end point of the line robot
        p1[0] = p_new[0] + math.cos(p_new[angle]) * r_length / 2
        p1[1] = p_new[1] + math.sin(p_new[angle]) * r_length / 2
        p2[0] = p_new[0] - math.cos(p_new[angle]) * r_length / 2
        p2[1] = p_new[1] - math.sin(p_new[angle]) * r_length / 2

        for o in obstacles:
            intersect = 0
            if lineHitsRect(p1, p2, o) or inRect(p_new, o, 1):
                intersect = 1
                break
        if intersect:
            # take next sampling point
            continue

        else:
            lastnode += 1
            vertices.append(p_new)
            G[nodes].append(lastnode)
            G[edges].append((node_closest, lastnode))
            if visualize:  canvas.polyline([vertices[node_closest], p_new])
            dist_to_goal = pointPointDistance(p_new, [tx, ty, ta])

    if nb_iter == MAXITER:
        print("path not found")
        return -1, MAXITER
    # finding the path
    k = lastnode
    path = []

    while k != 0:
        k = returnParent(k)
        path.append(k)

    path_lenght = len(path) * SMALLSTEP
    return path_lenght, nb_iter


if visualize:
    canvas = drawSample.SelectRect(xmin=0, ymin=0, xmax=XMAX, ymax=YMAX, nrects=0,
                                   keepcontrol=0)  # , rescale=800/1800.)

if 0:  # line intersection testing
    obstacles.append([75, 60, 125, 500])  # tall vertical
    for o in obstacles: canvas.showRect(o, outline='red', fill='blue')
    lines = [
        ((70, 50), (150, 150)),
        ((50, 50), (150, 20)),
        ((20, 20), (200, 200)),
        ((300, 300), (20, 200)),
        ((300, 300), (280, 90)),
    ]
    for l in lines:
        for o in obstacles:
            lineHitsRect(l[0], l[1], o)
    canvas.mainloop()

if 0:
    # random obstacle field
    for nobst in range(0, 6000):
        wall_discretization = SMALLSTEP * 2  # walls are on a regular grid.
        wall_lengthmax = 10.  # fraction of total (1/lengthmax)
        x = wall_discretization * int(random.random() * XMAX / wall_discretization)
        y = wall_discretization * int(random.random() * YMAX / wall_discretization)
        # length = YMAX/wall_lengthmax
        length = SMALLSTEP * 2
        if random.choice([0, 1]) > 0:
            obstacles.append([x, y, x + SMALLSTEP, y + 10 + length])  # vertical
        else:
            obstacles.append([x, y, x + 10 + length, y + SMALLSTEP])  # horizontal
else:
    if 0:
        # hardcoded simple obstacles
        obstacles = []
        obstacles.append([300, 0, 400, 95])  # tall vertical
        # slightly hard
        obstacles.append([300, 805, 400, YMAX])  # tall vertical
        # obstacles.append( [ 300,400,1300,430 ] )
        # hard
        obstacles.append([820, 220, 900, 940])
        obstacles.append([300, 0, 400, 95])  # tall vertical
        obstacles.append([300, 100, 400, YMAX])  # tall vertical
        obstacles.append([200, 300, 800, 400])  # middle horizontal
        obstacles.append([380, 500, 700, 550])
        # very hard
        obstacles.append([705, 500, XMAX, 550])

if visualize:
    for o in obstacles: canvas.showRect(o, outline='red', fill='blue')

c1 = csv.writer(open("results_line_robot.csv", "wb"), delimiter=",")
c1.writerow(["sep=,"])
c1.writerow(["length", "N", "Nb iterations"])
while 1:
    # graph G
    G = [[0], []]  # nodes, edges
    vertices = [[start_x, start_y, start_a], [start_x, start_y, start_a]]

    G[edges].append((0, 1))
    G[nodes].append(1)
    if visualize: canvas.markit(tx, ty, r=SMALLSTEP)
    drawGraph(G)

    if not visualize:
        for l in range(10, 110, 10): #iterate with different robot length
            for n in range(1, 11):
                G = [[1], [(0, 1)]]  # nodes, edges
                vertices = [[start_x, start_y, start_a], [start_x, start_y, start_a]]
                r_length = l
                [path_length, nb_iter] = rrt_search(G, tx, ty, ta)
                print"done l={} n={}".format(l, n)
                c1.writerow([SMALLSTEP, n, nb_iter])
    else:
        [path_length, nb_iter] = rrt_search(G, tx, ty, ta)
    break

# canvas.showRect(rect,fill='red')

if visualize:
    canvas.mainloop()
