#Importing all the required libraries
import ezdxf
from ezdxf.math import *
import pygame

#Setting up our DXF settings
doc = ezdxf.new('R2000')
msp = doc.modelspace()

# Setting up initial parameters for the box dimmension
t = 9 #Thickness of material
w = 50 #Internal Width of box
wn =5 #Number of fingers along the width
h1 = 50 #Internal Height of box
h2 =h1+2*t #This is used as a fiddle factor cos geometry
h2n =5 #Number of fingers along the Height
d = 50 #Internal Depth of the box
d2 = d+2*t #This is used as a a fiddle factor cos geometry
d2n =5 #Number of fingers along the Depth
W = [w,wn]
H = [h2,h2n]
D = [d2,d2n]
bufferx = w +3*t +d2 # This is used so that all coordinates are positive
buffery = h2 + t + d2 # As above
buffer = 50 # Padding
x2 = w+2*t
y2 = -h2-2*t
disp = 1
#Stepmaker is the brains of the operation, makes the 'steps' or castleations
#that become the fingers
def StepMaker(StartX,StartY,Length,Number,XMajor,MajorMirror,MinorMirror,Add):
    #StartX is the starting X coordinate
    #StartY is the starting Y coordinate
    #Length is the length of the section
    #Number is the number of fingers
    #XMajor is true if you want x to be the 'major' axis
    #MajorMirror is true if you want to mirror about the 'major' axis
    #MinorMirror is true if you want to mirror about the 'minor' axis
    #If Add is true, line is immediately added to the DXF and not returned
    #'Major' is the axis that Length will act along, minor is perpendicular
    if MajorMirror == 1:
        MM = 1
    else:
        MM=-1
    if MinorMirror == 1:
        MnM = -1
    else:
        MnM=1
    inc = Length/Number #Splits the Length in to the steps needed
    iter = (Number*2)-1 #Determines how many points we are going to need later
    result=[0]*iter #Creates an empty array for filling with points later

    for i in range(iter): #Iterating through every point to get coordinates
        # A and B are our stepping equations
        A = (((i)%2)+(i))/2 #Bit of maths that goes 1,1,2,2,3,3 etc
        B = ((((i-1)%2)+(i-1))/2)%2 #Bit of maths that goes 0,1,1,2,2,3 etc.
        #Takes our stepping equations and turns them into values
        C = A*inc*MnM #Spreads out the points to create our steps
        D = B*t*MM
        if XMajor == 0: #These just write the coordinates in the form (x,y)
            result[i] = D+StartX+buffer,C+StartY+buffery+buffer
        else:
            result[i] = C+StartX+buffer,D+StartY+buffery+buffer
    if Add == 0:
        return result
    else: #Returns the coordinates so they can be aggregated
        test=msp.add_lwpolyline(result)

def BoxMaker(x,y,dx,dy,X_In,Y_In):
    A1=StepMaker(x,y,dx[0],dx[1],1,X_In,0,disp) #X, no flip
    A2=StepMaker(x+dx[0],y,dy[0],dy[1],0,Y_In,1,disp) #Y, mirror on x and y
    A3=StepMaker(x+dx[0],y-dy[0],dx[0],dx[1],1,not X_In,1,disp) #x, mirror on x and y
    A4=StepMaker(x,y-dy[0],dy[0],dy[1],0,not Y_In,0,disp)# y no flip
    if disp == 0:
        source = A1+A2+A3+A4
        i1 =msp.add_lwpolyline(source)
        i1.close()

#OriginX,OriginY,XDim,YDim,XInwards?,Yinwards?
BoxMaker(0,0,W,H,0,1)
BoxMaker(0,y2,W,D,1,1)
BoxMaker(x2,0,D,H,0,0)


# result = list(offset_vertices_2d(source, offset=0.5, closed=True))
# final =msp.add_lwpolyline(result)
# final.close()


#Saves all our lines as a file
doc.saveas("lwpolyline1.dxf")


#This bit is temporary and due a rework, dont really understand what ive done
#but it works
if disp == 0:
    def Preview():
        pygame.init()
        black = (0,0,0)
        green = (0,255,0)
        white= (255,255,255)
        red = (255,0,0)
        blue = (0,0,255)

        gameDisplay = pygame.display.set_mode((bufferx+2*buffer,buffery+2*buffer))
        gameDisplay.fill(black)


        pygame.draw.polygon(gameDisplay, blue, source)
        pygame.draw.polygon(gameDisplay, green, source2)
        pygame.draw.polygon(gameDisplay, red, source3)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()

    Preview()
