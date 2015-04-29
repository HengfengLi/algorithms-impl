# Re-write the C code from Computational Geometry in C - Section 3.5. 

# max # of points
PMAX = 1000
P_origin = None

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "x:%.2f,y:%.2f" % (self.x, self.y)
        
    def __repr__(self):
        return self.__str__()

class tsPoint:
    def __init__(self, id, coord):
        self.id = id
        self.coord = coord
        self.flag_deleted = False
    
    def __str__(self):
        return "vnum:%d,coord:%s,deleted:%s" \
            % (self.id, self.coord, self.flag_deleted)
        
    def __repr__(self):
        return self.__str__()

class tStackCell:
    def __init__(self, p):
        self.p = p
        self.next = None

class tStack:
    def __init__(self):
        self.top = None
        self.num = 0
    
    def pop(self):
        if self.num == 0: return None
        
        temp = self.top
        self.top = self.top.next
        self.num -= 1
        
        return temp.p
        
    def push(self, p):
        
        c = tStackCell(p)
        c.next = self.top
        self.top = c
        self.num += 1
    
    def values(self):
        t = self.top
        while t:
            yield t.p
            t = t.next
    
    def __str__(self):
        t = self.top
        output = ""
        while t:
            output += "vnum=%d\tx=%.2f\ty=%.2f\n" \
                % (t.p.id, t.p.coord.x, t.p.coord.y)
            t = t.next
        return output
        
    def __repr__(self):
        return self.__str__()


def area2(a, b, c):
    return (b.x-a.x) * (c.y-a.y) - (c.x-a.x)*(b.y-a.y)

def compare(pi, pj):
    
    a = area2(P_origin.coord, pi.coord, pj.coord)
    
    if a > 0: return -1
    if a < 0: return 1
    
    # collinear with P[0]
    x = abs(pi.coord.x - P_origin.coord.x) - abs(pj.coord.x - P_origin.coord.x)
    y = abs(pi.coord.y - P_origin.coord.y) - abs(pj.coord.y - P_origin.coord.y)
    
    if x < 0 or y < 0:
        pi.flag_deleted = True
        return -1
    elif x > 0 or y > 0:
        pj.flag_deleted = True
        return 1
    else:
        # points are coincident
        if pi.id > pj.id:
            pj.flag_deleted = True
        else:
            pi.flag_deleted = True
        return 0

def swap(P, i, j):
    temp = P[i]
    P[i] = P[j]
    P[j] = temp

def find_lowest(P):
    # get a copy
    P = P[:]
    # index of lowest
    m = 0
    
    for i in range(1,len(P)):
        if (P[i].coord.y < P[m].coord.y or P[i].coord.y == P[m].coord.y) \
        and (P[i].coord.x > P[m].coord.x):
            m = i
    
    swap(P, 0, m)
    
    return P

def graham(P):
    # initalize stack
    stack = tStack()
    stack.push(P[0])
    stack.push(P[1])
    
    assert(stack.num == 2)
    
    # bottom two elements will never be removed
    i = 2
    
    while i < len(P):
        # print "i", i
        p1 = stack.top.next.p
        p2 = stack.top.p
        
        # print area2(p1.coord, p2.coord, P[i].coord)
        if area2(p1.coord, p2.coord, P[i].coord) > 0:
            stack.push(P[i])
            i += 1
        else:
            # print "stack.pop"
            stack.pop()
    
    return stack

def graham_scan(coords):
    global P_origin
        
    # construct the list of points
    P = []
    for i in range(len(coords)):
        x, y = coords[i]
        P.append(tsPoint(i, Coord(x, y)))
    
    # actual # of points
    n = len(P)
    
    # find the right-most of lowest point
    P = find_lowest(P)
    print "lowest:", P[0]
    P_origin = P[0]
    
    # sort other points angularly
    new_P = [P[0]] + sorted(P[1:], cmp=compare)
    
    # squash
    new_P = filter(lambda p: p.flag_deleted != True ,new_P)
    
    # print new_P
    stack = graham(new_P)
    
    return [(p.coord.x, p.coord.y) for p in stack.values()]

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    coords = [(3,-2), (5,1), (7,4), (6,5), (4,2), (3,3), (3,5), (2,5), (0,5), \
         (0,1), (-3,4), (-2,2), (0,0), (-3,2), (-5,2), (-5,1), (-5,-1),  \
         (1,-2), (-3,-2)]
    assert(len(coords) == 19)
    
    convex_hull_points = graham_scan(coords)
    
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
        
    ax.set_aspect('equal')
    ax.grid(True, which='both')

    # set the x-spine (see below for more info on `set_position`)
    ax.spines['left'].set_position('zero')
    # turn off the right spine/ticks
    ax.spines['right'].set_color('none')
    # set the y-spine
    ax.spines['bottom'].set_position('zero')
    # turn off the top spine/ticks
    ax.spines['top'].set_color('none')
    
    ax.xaxis.tick_bottom()
    ax.yaxis.tick_left()
    
    ax.set_xlim([-6,8])
    ax.set_ylim([-3,6])
    
    x1 = [p[0] for p in coords]
    y1 = [p[1] for p in coords]
    
    # "clip_on=False, zorder=100" makes the points are above axes and girds
    ax.scatter(x1, y1, c='red', clip_on=False, zorder=100)
    
    x2 = [p[0] for p in convex_hull_points + [convex_hull_points[0]]]
    y2 = [p[1] for p in convex_hull_points + [convex_hull_points[0]]]
    ax.plot(x2, y2, marker='o', clip_on=False, zorder=100)
    
    plt.show()