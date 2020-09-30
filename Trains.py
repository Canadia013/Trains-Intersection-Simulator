import random
current_time = 1  # used to help track when the train moves (speed factor)
r = True  # Set to False to get a definite collision case


class station:
    xpos = -1
    ypos = -1
    px = -10  # x and y coordinates of sister station
    py = -10
    ltr = '_'

    def __init__(self, x, y, px, py, ltr):
        self.xpos = x
        self.ypos = y
        self.px = px
        self.py = py
        self.ltr = ltr
        if(self.xpos == self.px):
            self.track_type = 'EW'
        elif(self.ypos == self.py):
            self.track_type = 'NS'

    def get_data(self):
        print(self.xpos, ' ', self.ypos, ' ',
              self.px, ' ', self.py, ' ', self.ltr)


class grid:
    # Config
    letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
              'z']

    def __init__(self, l, h, t):
        self.length = l
        self.height = h
        self.trains = t
        self.stations = []
        self.intersections = []
        self.checksignals = []

    def create(self):
        for i in range(0, self.trains):
            x = random.randint(self.length/4, self.length*3/4)
            y = random.randint(self.height/4, self.height*3/4)
            z = random.randint(0, 3)
            if(z == 0):
                py = random.randint(0, y)
                px = x
            elif(z == 1):
                px = random.randint(x, self.length)
                py = y
            elif(z == 2):
                py = random.randint(x, self.height)
                px = x
            elif(z == 3):
                px = random.randint(0, x)
                py = y
            self.stations.append(station(x, y, px, py, self.letter[i]))

    def create2(self):
        x = 10
        y = 20
        px = 50
        py = 20
        self.stations.append(station(x, y, px, py, self.letter[0]))
        x = 20
        y = 30
        px = 20
        py = 10
        self.stations.append(station(x, y, px, py, self.letter[1]))

    def print_stations(self):
        for i in self.stations:
            i.get_data()

    def findIntersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / \
                ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        except ZeroDivisionError:
            return None
        try:
            py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / \
                ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        except ZeroDivisionError:
            return None
        return [int(px), int(py)]

    def find_intersections(self):
        s = self.stations
        i = self.intersections
        for x in range(0, len(s)):
            for y in range(x, len(s)):
                i.append(self.findIntersection(
                    s[x].xpos, s[x].ypos, s[x].px, s[x].py, s[y].xpos,
                    s[y].ypos, s[y].px, s[y].py))
        while(None in i):
            i.remove(None)
        for x in range(0, len(i)):
            # Currently is making infinite line (not line segment) in
            # findInterseciton, so will create intersections that are not
            # within
            # the bounds of the stations/grid
            pass


class Train:
    max_speed = 1
    min_speed = 3
    top_speed = 1

    # coordinates for train_c are in an array of size 2. First entry is row
    # second is column
    def __init__(self, train_l, train_c, train_d, track, d, spd):
        self.train_coordinates = train_c
        self.train_destination = train_d
        self.train_letter = train_l
        self.current_track = track  # either NS or EW
        self.direction = d  # N,S,E, or W
        self.speed = spd

    def move(self):
        if(self.train_coordinates == self.train_destination):
            pass
        else:
            if(current_time % self.speed == 0):
                if(self.direction == 'N'):
                    self.train_coordinates[0] -= 1
                elif(self.direction == 'S'):
                    self.train_coordinates[0] += 1
                elif(self.direction == 'W'):
                    self.train_coordinates[1] -= 1
                elif(self.direction == 'E'):
                    self.train_coordinates[1] += 1
        self.change_speed(1)

    def change_speed(self, i):
        if(i == -1):
            if(self.speed < self.min_speed):
                self.speed = self.speed+1
        elif(i == 1):
            if(self.speed > self.max_speed):
                self.speed = self.speed-1
        else:
            pass

    def print_train(self):
        print(' Train:', self.train_letter, 'Current Location:',
              self.train_coordinates, ' Destination: ',
              self.train_destination, ' Speed: ', self.speed)

    def estimated_arrival_time(self, coordinate_destination, spd):
        self.temp_time = current_time
        self.temp_coordinates = self.train_coordinates.copy()
        while(coordinate_destination != self.temp_coordinates):
            if(self.temp_coordinates == self.train_destination):
                break
            elif(self.temp_time % spd == 0):
                if(self.temp_time != 0):
                    if(self.direction == 'N'):
                        self.temp_coordinates[0] -= 1
                    elif(self.direction == 'S'):
                        self.temp_coordinates[0] += 1
                    elif(self.direction == 'W'):
                        self.temp_coordinates[1] -= 1
                    elif(self.direction == 'E'):
                        self.temp_coordinates[1] += 1
            self.temp_time += 1
            # print("Train is at",self.temp_coordinates) #prints the method
            # step by step till it finishes
            # print(coordinate_destination)
        return self.temp_time


g = grid(100, 100, 3)
if(r):
    g.create()
else:
    g.create2()

g.print_stations()
g.find_intersections()
print(g.intersections)
intersections_in_use = [False] * len(g.intersections)
train_right_of_way = [None] * len(g.intersections)


def prevent_collisions(train):
    global intersections_in_use
    global train_right_of_way
    for index, i in enumerate(g.intersections):
        if(in_range_of_intersection(train, i)):
            # print("In Check", train.train_letter)
            if(intersections_in_use[index]):
                if(train_right_of_way[index] == train.train_letter):
                    pass
                # else:
                #     intersections_in_use[index]=False
                #     print(intersections_in_use[index])

                else:
                    train.change_speed(-1)
                    if(train.max_speed < train.min_speed):
                        train.max_speed += 1
            else:
                train_right_of_way[index] = train.train_letter
                intersections_in_use[index] = True
                # print("Moving as normal", train.train_letter)
                train.max_speed = train.top_speed
        elif(train_right_of_way[index] == train.train_letter):
            intersections_in_use[index] = False


def in_range_of_intersection(train, intersection):
    if(abs(intersection[0]-train.train_coordinates[0]) <= 3):
        if(abs(intersection[1]-train.train_coordinates[1]) <= 3):
            return True
    else:
        return False


list_trains = []
print(len(g.stations))
character_int = 65
for s in g.stations:
    if(s.track_type == 'NS'):
        if(s.xpos-s.px < 0):
            list_trains.append(Train(chr(character_int), [s.xpos, s.ypos], [
                               s.px, s.py], s.track_type, 'S', 3))
        else:
            list_trains.append(Train(chr(character_int), [s.xpos, s.ypos], [
                               s.px, s.py], s.track_type, 'N', 3))
    elif(s.track_type == 'EW'):
        if(s.ypos-s.py > 0):
            list_trains.append(Train(chr(character_int), [s.xpos, s.ypos], [
                               s.px, s.py], s.track_type, 'W', 3))
        else:
            list_trains.append(Train(chr(character_int), [s.xpos, s.ypos], [
                               s.px, s.py], s.track_type, 'E', 3))
    character_int += 1
# train1=Train('X',[g.stations[0].xpos, g.stations[0].ypos],[g.stations[0].px,
# g.stations[0].py],g.stations[0].track_type, 'S', 3)
# train2=Train('Y',[g.stations[1].xpos, g.stations[1].ypos],[g.stations[1].px,
# g.stations[1].py],g.stations[1].track_type, 'W', 3)
for x in range(0, 50):
    for z in list_trains:
        z.print_train()
        prevent_collisions(z)
        z.move()
    # train1.print_train()
    # train2.print_train()
    # prevent_collisions(train1)
    # prevent_collisions(train2)
    # train1.move()
    # train2.move()
    # current_time=current_time+1

# print(g.intersections)
# print(g.stations[0].track_type)


# print("ETA to next station", train1.estimated_arrival_time([g.stations[0].px,
# g.stations[0].py], train1.speed))
