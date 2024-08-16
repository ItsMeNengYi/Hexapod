import pygame
import time
import math


#game initialization
pygame.init()
pygame.mixer.init()

#constant values
## Colors
BLACK =(0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (98,98,98)

## Environment
WIDTH = 10000
HEIGHT = 10000
DEPTH = 10000

## Screen
FPS = 144

def readFile(file,magnitude):
    vertices=[]
    with open(file, "r") as f:
        for line in f:
            index=0
            v=0
            space=[]
            if line[0] == "v" and line[1] == ' ':
                for char in line:
                    if char == "v":
                        v=1
                    if char == ' ':
                        space.append(index)
                    index += 1
                if v:
                    vertice=[]
                    space.append(len(line)-1)
                    for x in range(0,len(space)-1,1):
                        vertice.append(magnitude*float(line[space[x]+1:space[x+1]]))
                    vertices.append(vertice)
    print(len(vertices))
    return vertices

def draw_text_on_screen(text,position=(0,0),size = 40):
    font = pygame.font.SysFont(None, size)
    img = font.render(f"{text}", True, BLACK)
    screen.blit(img, position)

def matrix_multiply(matrix1,matrix2):
    # Check
    if len(matrix1[0]) != len(matrix2):
        print("Matrix multiplication error!")
        return
    Clen = len(matrix2[0]) # column length
    Rlen = len(matrix1)    # row length

    temp = [[0 for i in range(Clen)] for j in range(Rlen)]
    for i in range(0, Rlen):
        for j in range(0,Clen):
            for k in range(0,len(matrix1[0])):
                temp[i][j] += matrix1[i][k] * matrix2[k][j]
    return temp

def matrix_0Add_1Subtract(matrix1,matrix2,option=0): # option 0 is add, 1 is subtract
    a = 1
    if option == 1:
        a = -1
    Clen = len(matrix1[0]) # column length
    Rlen = len(matrix1)    # row length

    temp = [[0 for i in range(Clen)] for j in range(Rlen)]
    for i in range(0, Rlen):
        for j in range(0,Clen):
                temp[i][j] = matrix1[i][j] + a * matrix2[i][j]
    return temp

def rotation_matrix(angle):
    return [
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ]

def ThreeD_rotation(coordinate,pitch=0,yaw=0,roll=0):
    x = coordinate[0]
    y = coordinate[1]
    z = coordinate[2]
    
    # Rotate about X-axis
    [[y, z]] = matrix_multiply([[y,z]], rotation_matrix(-pitch))
    # Rotate about Y-axis
    [[z, x]] = matrix_multiply([[z,x]], rotation_matrix(-yaw))
    # Rotate about Z-axis
    [[x, y]] = matrix_multiply([[x,y]], rotation_matrix(-roll))

    return [x,y,z]


def weirdo(length):
    return [[
        [0,0,0],
        [0,0,length],

        [length,0,0],
        [length,0,length],

        [length,length,0],
        [length,length,length],

        [0,2*length,0],
        [0,2*length,length],
        
        
        [2*length,length,length],
        [2*length,2*length,length],
    ],[
        [0,1],[2,3],[4,5],[6,7],[0,2],[1,3],[2,4],[3,5],[4,8],[5,8],[8,9],[6,9],[0,6],[7,9],[1,7],[4,6]
    ],[
        [4,6,9,8],[2,0,6,4]
    ]]
## Shapes functions (return vertices and edges lists)
## square vertices:Square(Length)[0] 
## square edges :Square(Length)[1] 
## square faces :Square(Length)[2] 
def Square(length):
    return [[
        [0,0,0],
        [0,length,0],
        [length,0,0],
        [length,length,0],
        [0,0,length],
        [0,length,length],
        [length,0,length],
        [length,length,length]
    ],[
        [0,1],[0,2],[1,3],[0,4],[4,5],[4,6],[6,7],[3,7],[5,7],[2,6],[2,3],[1,5]
    ],[
        [0,2,3,1],[6,4,5,7],[3,1,5,7],[3,2,6,7],[1,0,4,5],[2,0,4,6]
    ]]

def Hexagon(length):
    l = length
    return[[
        [-l*(1*math.cos(DEVIATE_ANGLE)),0,l*math.sin(DEVIATE_ANGLE)],
        [l*(1*math.cos(DEVIATE_ANGLE)),0,l*math.sin(DEVIATE_ANGLE)],
        [l,0,0],
        [l*(1*math.cos(DEVIATE_ANGLE)),0,-l*math.sin(DEVIATE_ANGLE)],
        [-l*(1*math.cos(DEVIATE_ANGLE)),0,-l*math.sin(DEVIATE_ANGLE)],
        [-l,0,0]
    ],[
        [0,1],[1,2],[2,3],[3,4],[4,5],[5,0]
    ],["None"]]
## pyramid vertices:Pyramid(Length)[0] 
## pyramid edges :Pyramid(Length)[1] 
## pyramid faces :Pyramid(Length)[2] 
def Pyramid(length):
    return [[
        [0,0,0],
        [length,0,0],
        [0,0,length],
        [length,0,length],
        [length/2,length,length/2]
    ],[
        [0,2],[0,1],[1,3],[2,3],[0,4],[1,4],[2,4],[3,4]
    ],[
        [4,0,1],[4,0,2],[4,2,3],[4,1,3],[1,0,2,3]
    ]]

def Circle(length):
    resolution = 1
    vertices = []
    for i in range(0,361,resolution):
        vertices.append([length*math.sin(i),length*math.cos(i),0])
    return [vertices,["None"],["None"]]



## Animations
def Animation(Object,vertices,animations):
    value = vertices
    for animation in animations:
        # Checks for animations
        if animation[0:9] == "Transform": 
            value = Transform(vertices,[Object.position],int(animation[10:len(animation)]),animation[9])
            vertices = value

        if animation[0:6] == "Rotate":
            if len(animation)>6:
                Center = animation[7:len(animation)-1]
                center = [0,0,0]
                temp = 0
                index1 = 0
                index2 = 0
                for char in Center:
                    if char == ",":
                        center[index1] = int(Center[temp:index2])
                        temp = index2 + 1
                        index1 += 1
                    index2 += 1
                center[index1] = int(Center[temp:len(Center)])
                value = Rotate(vertices,[center],1)
                vertices = value
            else:
                value = Rotate(vertices,[Object.position],1)
                vertices = value
    return value
    
def Rotate(position,center,speed):
    angular_speed =  time * speed/180 * math.pi
    [[x,y,z]] = matrix_0Add_1Subtract(position,center,1)
    
    
    # Rotate about X-axis
    [[y, z]] = matrix_multiply([[y,z]], rotation_matrix(angular_speed))
    # Rotate about Y-axis
    [[z, x]] = matrix_multiply([[z,x]], rotation_matrix(angular_speed))
    # Rotate about Z-axis
    [[x, y]] = matrix_multiply([[x,y]], rotation_matrix(angular_speed))

    [[x,y,z]] = matrix_0Add_1Subtract([[x,y,z]],center,0)
    return [[x,y,z]]

def Transform(position,center,angle,axis):
    sita = angle/180 * math.pi
    [[x,y,z]] = matrix_0Add_1Subtract(position,center,1)
    if axis=="Y":
        # Rotate about Y-axis
        [[z, x]] = matrix_multiply([[z,x]], rotation_matrix(sita))
    if axis=="X":
        # Rotate about X-axis
        [[y, z]] = matrix_multiply([[y,z]], rotation_matrix(sita))
    if axis=="Z":
        # Rotate about Z-axis
        [[x, y]] = matrix_multiply([[x,y]], rotation_matrix(sita))
    [[x,y,z]] = matrix_0Add_1Subtract([[x,y,z]],center,0)
    return [[x,y,z]]


def Get_screen_position(Player, vertices,Object="None", animation="None"):
    # Animation 
    if animation != "None":
        [vertices] = Animation(Object,[vertices],animation)
    Xr0 = vertices[0] - Player.position[0]
    Yr0 = vertices[1] - Player.position[1]
    Zr0 = vertices[2] - Player.position[2]
    if Zr0 == 0:
        Zr0 = 0.001

    
    sita_y = Player.rotation[0]/180*math.pi
    sita_x = Player.rotation[1]/180*math.pi
    # Rotate about Y-axis
    [[Zr, Xr]] = matrix_multiply([[Zr0,Xr0]], rotation_matrix(sita_y))
    # Rotate about X-axis
    [[Yr, Zr]] = matrix_multiply([[Yr0,Zr]], rotation_matrix(sita_x))


    Zr = math.sqrt(abs(Zr)) 

    aspect_ratio = Player.height/Player.width
    Scale = (math.tan(Player.fov/2) * Player.radius)/Zr

    X = Xr * Scale * aspect_ratio
    Y = Yr * Scale

    X = Player.width/2 * (1 + X/WIDTH)
    Y = Player.height/2 * (1 - Y/HEIGHT)

    #Debug
    # if vertice_index == 0:
    #     draw_text_on_screen(f"X={int(Xr)},Y={int(Yr)},Z={int(Zr)}",(500,0))
    #     draw_text_on_screen(f"x={int(Xr0)},y={int(Yr0)},z={int(Zr0)}",(X,Y-100))
    #     draw_text_on_screen(f"X={int(Xr)},Y={int(Yr)},Z={int(Zr)}",(X,Y))
    return [X,Y]

class Player():
    def __init__(self,fov, dimention, radius, position = [5000,5000,0]):
        self.fov = fov/180*math.pi
        self.width = dimention[0]
        self.height = dimention[1]
        self.radius = radius
        self.position = position
        self.rotation = [0,0] #[yaw,pitch]
        # Moving
        self.speed = 10
        self.angular_speed = 1

    def update(self,mouse_movement):             

        # Rotation #
        increment0 = self.rotation[0] + mouse_movement[0] * 0.1 * self.angular_speed
        increment1 = self.rotation[1] + mouse_movement[1] * 0.1 * self.angular_speed

        if increment0 <180 and increment0 >-180:
            self.rotation[0] = increment0
        else:
            self.rotation[0] = -self.rotation[0] + mouse_movement[0] * 0.1 * self.angular_speed
        if increment1 <180 and increment1 >-180:
            self.rotation[1] = increment1
        else:
            self.rotation[1] = -self.rotation[1] + mouse_movement[0] * 0.1 * self.angular_speed

        # Displacement
        pitch = self.rotation[1]/180*math.pi
        yaw = self.rotation[0]/180*math.pi
        forward = ThreeD_rotation([0,0,self.speed],pitch,yaw)
        backward = ThreeD_rotation([0,0,-self.speed],pitch,yaw)
        left = ThreeD_rotation([-self.speed,0,0],pitch,yaw)
        right = ThreeD_rotation([self.speed,0,0],pitch,yaw)
        upward = ThreeD_rotation([0,self.speed,0],pitch,yaw)
        downward = ThreeD_rotation([0,-self.speed,0],pitch,yaw)

        # # Debug
        # draw_text_on_screen(f"forward = {int(forward[0]),int(forward[1]),int(forward[2])}",(0,500))
        # draw_text_on_screen(f"backward = {int(backward[0]),int(backward[1]),int(backward[2])}",(0,550))
        # draw_text_on_screen(f"left = {int(left[0]),int(left[1]),int(left[2])}",(0,600))
        # draw_text_on_screen(f"right = {int(right[0]),int(right[1]),int(right[2])}",(0,650))
        # draw_text_on_screen(f"upward = {int(upward[0]),int(upward[1]),int(upward[2])}",(0,700))
        # draw_text_on_screen(f"downward = {int(downward[0]),int(downward[1]),int(downward[2])}",(0,750))

        if moving_forward:
            [self.position] = matrix_0Add_1Subtract ([self.position],[forward])
        if moving_backward:
            [self.position] = matrix_0Add_1Subtract ([self.position],[backward])
        if moving_left:
            [self.position] = matrix_0Add_1Subtract ([self.position],[left])
        if moving_right:
            [self.position] = matrix_0Add_1Subtract ([self.position],[right])
        if moving_up:
            [self.position] = matrix_0Add_1Subtract ([self.position],[upward])
        if moving_down:
            [self.position] = matrix_0Add_1Subtract ([self.position],[downward])
    
    def Get_Player_Info(self):
        #      [x,y,z]       [x,y]
        return self.position,self.rotation

class Leg():
    def __init__(self,origin,name):
        self.sita1 = math.radians(0)
        self.sita2 = 0
        self.phi = math.radians(0)
        self.length1 = 110
        self.length2 = 170
        self.vertice1 = origin
        self.vertice2 = [0,0,0]
        self.vertice3 = [0,0,0]
        self.vertices = [self.vertice1,self.vertice2,self.vertice3]
        self.color = BLACK
        self.debugVertices = []
        self.name = name
        self.Debug = False
    def update(self,player,required_position=None):
        if(required_position!=None):
            [x,y,z] = [-required_position[0],required_position[1],required_position[2]]
            # if(self.name=="L2"):
            #     print(int(-required_position[0])/10,int(required_position[1])/10,int(required_position[2])/10)
            self.sita2 = math.atan(z/x)
            a = math.sqrt(x**2 + z**2)
            self.phi = math.acos((z**2+x**2+y**2-self.length1**2-self.length2**2)/(self.length1*self.length2*2))
                
            angle_a = math.atan(math.sin(self.phi)/(self.length1/self.length2 + math.cos(self.phi)))
            if (angle_a<0):
                angle_a = math.pi-abs(angle_a)
            angle_c=math.atan(abs(y/a))

            if(y<0):
                self.sita1 = angle_a-angle_c
            else:
                self.sita1 = angle_a+angle_c

            if(x>0):
                self.phi = -self.phi
                self.sita1=math.pi - self.sita1

            if(self.name=="L2"):
                print(self.sita1/math.pi*180,self.sita2/math.pi*180,self.phi/math.pi*180)

            a = 0
            if(self.name=="L1" or self.name=="R3"):
                a = 1
            if(self.name=="L3" or self.name=="R1"):
                a = -1
            self.sita2 = self.sita2+a*DEVIATE_ANGLE
            
        a = self.length1*math.cos(self.sita1)
        self.vertice2 = [-a*math.cos(self.sita2),self.length1*math.sin(self.sita1),a*math.sin(self.sita2)]

        a = self.length2*math.cos(self.phi-self.sita1)
        self.vertice3 = [-a*math.cos(self.sita2),-self.length2*math.sin(self.phi-self.sita1),a*math.sin(self.sita2)]

        if(self.Debug):
            draw_text_on_screen(f"leg position: {int(self.vertice3[0]+self.vertice2[0]),int(self.vertice3[1]+self.vertice2[1]),int(self.vertice3[2]+self.vertice2[2])}",(0,800))
        

        [self.vertice2] = matrix_0Add_1Subtract ([self.vertice2],[self.vertice1])
        [self.vertice3] = matrix_0Add_1Subtract ([self.vertice3],[self.vertice2])
        
        # if(self.Debug):
            # Display rotation angle
        if(self.name=="L2"):
            draw_text_on_screen(f"sita1: {int(math.degrees(self.sita1))}",(0,600))
            draw_text_on_screen(f"sita2: {int(math.degrees(self.sita2))}",(0,650))
            draw_text_on_screen(f"phi: {int(math.degrees(self.phi))}",(0,700))

        leglength = math.sqrt((self.vertice3[0]-self.vertice1[0])**2+(self.vertice3[1]-self.vertice1[1])**2+(self.vertice3[2]-self.vertice1[2])**2)

        if(self.Debug):
            draw_text_on_screen(f"expected length: {int(math.sqrt(x**2 + y**2 + z**2))} leg length: {int(leglength)}",(0,750))

        ver1 = Get_screen_position(player,self.vertice1,self,"None")
        ver2 = Get_screen_position(player,self.vertice2,self,"None")
        ver3 = Get_screen_position(player,self.vertice3,self,"None")

        pygame.draw.line(screen, self.color, ver1, ver2,5)
        pygame.draw.line(screen, self.color, ver3, ver2,5)
        

        if(self.Debug):
            #Draw Axis
            XYZ_axis(self.vertice1,matrix_0Add_1Subtract ([self.vertice2],[self.vertice1],1)[0],player,[0,self.sita2,self.sita1])
            XYZ_axis(self.vertice2,matrix_0Add_1Subtract ([self.vertice3],[self.vertice2],1)[0],player,[0,self.sita2,self.phi])
            # Debug circle
            circle1 = Object(self.vertice1, Circle(self.length1),[f"TransformY{-int(math.degrees(self.sita2))}"])
            circle2 = Object(self.vertice2, Circle(self.length2),[f"TransformY{-int(math.degrees(self.sita2))}"])
            # circle3 = Object(self.vertice1, Circle(20),[f"TransformY{90+self.sita2}"]
            # circle4 = Object(self.vertice2, Circle(20),[f"TransformY{90+self.sita2}"])
            circle1.update(player)
            circle2.update(player)
            # circle3.update(player)
            # circle4.update(player)

        if (self.vertice3 not in self.debugVertices):
            self.debugVertices.append(self.vertice3)
        for vertice in self.debugVertices:
            rect = pygame.Rect(Get_screen_position(player,vertice),(1,1)) 
            pygame.draw.rect(screen,RED, rect,1)

class Object():
    def __init__(self, initial_position, shape_function, animation = ["None"], color = BLACK, surface_color = GREEN):
        self.position = initial_position
        self.matrix = shape_function[0]
        self.edges = shape_function[1]
        self.faces = shape_function[2]
        self.color = color
        self.face_color = surface_color 
        self.no_of_vertices = len(self.matrix)
        self.animation = animation

    def update(self,player):
        ## Draw vertices
        rects = []
        vertices = [[self.position[0],self.position[1],self.position[2]]] * self.no_of_vertices
        vertices = matrix_0Add_1Subtract(vertices,self.matrix,0)
        for vertice in vertices:
            i = vertices.index(vertice)
            vertices[i] = Get_screen_position(player, vertices[i],self,self.animation)
            rect1 = pygame.Rect(vertices[i],(1,1))
            rects.append(rect1)
        for rect in rects:    
            pygame.draw.rect(screen, self.color, rect,1)

        
        ## Draw edges
        if self.edges != ["None"]:
            for edge in self.edges:
                pygame.draw.line(screen, self.color, vertices[edge[0]], vertices[edge[1]])

        # ## Draw faces
        # if self.faces != ["None"]:
        #     for face in self.faces:
        #         list = []
        #         for vertice in face:
        #             list.append(vertices[vertice])
        #         pygame.draw.polygon(screen,self.face_color,list)

def XYZ_axis(origin,length,player,rot_angles = []):
    # X
    Origin = Get_screen_position(player, origin)
    x_origin = Get_screen_position(player, [origin[0]+length[0],origin[1],origin[2]])
    pygame.draw.line(screen, RED, Origin, x_origin,3)

    y_origin = Get_screen_position(player, [origin[0],origin[1]+length[1],origin[2]])
    pygame.draw.line(screen, GREEN, Origin, y_origin,3)

    z_origin = Get_screen_position(player, [origin[0],origin[1],origin[2]+length[2]])
    pygame.draw.line(screen, BLUE, Origin, z_origin,3)
    if (rot_angles!=[]):
        draw_text_on_screen(f"{int(math.degrees(rot_angles[0]))}",x_origin,30)
        draw_text_on_screen(f"{int(math.degrees(rot_angles[1]))}",y_origin,30)
        draw_text_on_screen(f"{int(math.degrees(rot_angles[2]))}",z_origin,30)

pos_index = 0.5
def required_position(time,leg):
    ZY_half_circle(time,leg)
    # XY_circle(time,leg)
    # draw_text_on_screen(f"expected position: {[int(-r_x),int(r_y),int(r_z)]}",(0,850))
    return [r_x,r_y,r_z]

def ZY_half_circle(time,leg,turning_angle = 0 ):
    global r_x,r_y,r_z,pos_index
    speed = 1
    turning_angle = math.pi/8
    time = time/100*speed
    period = 4
    z_offset=0
    x_offset=130
    y_offset=-70
    DistanceTravel = 50
    if(leg.name=="R1"or leg.name=="R3" or leg.name=="R2"):
        time = time + period/2
    if(leg.name=="L2"or leg.name=="R2"):
        time = time - period/2

    if(leg.name=="L1"or leg.name=="R1"):
        z_offset=-50
    if(leg.name=="L3"or leg.name=="R3"):
        z_offset=50

    # if(turning_angle!=0):
    #     turning_angle = turning_angle/2
    #     Radius = 80/math.tan(turning_angle)
    #     if(leg.name[0]=="L"):
    #         DistanceTravel = abs((Radius-50))*math.sqrt(2*(1-math.cos(turning_angle)))
    #     else:
    #         DistanceTravel = abs((Radius+50))*math.sqrt(2*(1-math.cos(turning_angle)))

    time = time%period
    # time = period-time
    if(time <=period/2):
        #circle
        r_z = DistanceTravel*math.cos(time/(period/2)*math.pi)+z_offset
        r_y = DistanceTravel*math.sin(time/(period/2)*math.pi)+y_offset
        r_x = x_offset
    else:
        #line
        r_z = DistanceTravel*math.cos(time/(period/2)*math.pi)+z_offset
        r_y = y_offset
        r_x = x_offset

    if(leg.name[0]=="R"):
        r_x = -r_x
    
    if(leg.name=="L1"or leg.name=="R3"):
        [r_x,r_y,r_z] = ThreeD_rotation([r_x,r_y,r_z],0,-DEVIATE_ANGLE)
    
    if(leg.name=="L3"or leg.name=="R1"):
        [r_x,r_y,r_z] = ThreeD_rotation([r_x,r_y,r_z],0,DEVIATE_ANGLE)


    # if(turning_angle!=0 ):
    #     center = [CENTER[0]+Radius*abs(turning_angle)/turning_angle,CENTER[1],CENTER[2]]
    #     [r_x,r_y,r_z] = ThreeD_rotation(matrix_0Add_1Subtract ([[r_x,r_y,r_z]],[center],1)[0],0,math.degrees(turning_angle))
    #     [[r_x,r_y,r_z]] = matrix_0Add_1Subtract ([[r_x,r_y,r_z]],[center])


def XY_circle(time,leg):
    global r_x,r_y,r_z
    time = time/100
    phase_diff = math.pi*0
    period = 2
    r_z = 0
    r_y = 10*math.sin(time/period*math.pi+phase_diff)-30
    r_x = 10*math.cos(time/period*math.pi+phase_diff)+30



DEVIATE_ANGLE = math.pi/3
CENTER = [5050,5000,1010]

# Create Elements
Player1 = Player(90, (1920,1080), 1000,)
leg_L1 = Leg([5025,5000,1053.3],"L1")
leg_L2 = Leg([5000,5000,1010],"L2")
leg_L3 = Leg([5025,5000,966.7],"L3")

leg_R1 = Leg([5075,5000,1053.3],"R1")
leg_R2 = Leg([5100,5000,1010],"R2")
leg_R3 = Leg([5075,5000,966.7],"R3")

body = Object(CENTER, Hexagon(50),[])

Objects_list = [
    body
]
leg_list = [
    leg_L1,
    leg_L2,
    leg_L3,
    leg_R1,
    leg_R2,
    leg_R3
]

#InitialSetting
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Player1.width,Player1.height))
font_name = pygame.font.match_font('arial')
    

#movement
moving_left = False
moving_right = False
moving_up = False
moving_down = False
moving_forward = False
moving_backward = False

mouse_position = (0,0)

running = True
# For animation
time = 0 
r_x,r_y,r_z = 0,0,0
while running:
    clock.tick(FPS)
    ### Mouse Settings ###
    mouse_movement = (0,0)
    mouse_movement = pygame.mouse.get_rel()
    ## Set cursor to middle
    # pygame.mouse.set_curser()

    #DetectInput
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moving_forward = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_s:
                moving_backward = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_e:
                moving_down = True
            if event.key == pygame.K_q:
                moving_up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moving_forward = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_s:
                moving_backward = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_e:
                moving_down = False
            if event.key == pygame.K_q:
                moving_up = False
        
    screen.fill(WHITE)

    # Elements update
    if (pygame.mouse.get_pressed()[0]):
        Player1.update(mouse_movement)
    else:
        Player1.update((0,0))
    
    for objects in Objects_list:
        objects.update(Player1)

    for leg in leg_list:
        leg.update(Player1,required_position(time,leg))
    # #Debug

    time += 1
    pygame.display.update()
    
pygame.quit()