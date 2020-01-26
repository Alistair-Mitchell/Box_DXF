#Importing all the required libraries
import ezdxf
from ezdxf.math import *
import pygame

#Setting up our DXF settings
doc = ezdxf.new('R2000')
msp = doc.modelspace()

# Setting up initial parameters for the box dimmension
t = 3 #Thickness of material
w = 40 #Internal Width of box
wn =5 #Number of fingers along the width
h1 = 40 #Internal Height of box
h2 =h1+2*t #This is used as a fiddle factor cos geometry
hn =5 #Number of fingers along the Height
d = 40 #Internal Depth of the box
d2 = 40+2*t #This is used as a a fiddle factor cos geometry
dn =5 #Number of fingers along the Depth
bufferx = w +15 +d # This is used so that all coordinates are positive
buffery = h1 + 15 + d # As above
buffer = 50 # Padding

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

#Really janky coordinate agregation (will be reworked)
A1=StepMaker(0,0,w,wn,1,0,0,0)
A2=StepMaker(w,0,h2,hn,0,1,1,0)
A3=StepMaker(w,-h2,w,wn,1,1,1,0)
A4=StepMaker(0,-h2,h2,hn,0,0,0,0)

y2 = -h2-2*t # Defining a new starting point
B1=StepMaker(0,y2,w,wn,1,1,0,0)
B2=StepMaker(w,y2,d,dn,0,1,1,0)
B3=StepMaker(w,y2-d,w,wn,1,0,1,0)
B4=StepMaker(0,y2-d,d,dn,0,0,0,0)

x2 = w+2*t #Defining a new starting point
C1=StepMaker(x2,0,d2,dn,1,0,0,0)
C2=StepMaker(x2+d2,0,h2,hn,0,0,1,0)
C3=StepMaker(x2+d2,-h2,d2,dn,1,1,1,0)
C4=StepMaker(x2,-h2,h2,hn,0,1,0,0)

source = A1+A2+A3+A4 #Piece 1 of 3 basically
source2 = B1+B2+B3+B4
source3 = C1+C2+C3+C4

i1 =msp.add_lwpolyline(source) #Writing the points to file as a joined line
i2 =msp.add_lwpolyline(source2)
i3 =msp.add_lwpolyline(source3)
i1.close() # Filling in any gaps between points
i2.close()
i3.close()

#This bit is for future development

# result = list(offset_vertices_2d(source, offset=0.5, closed=True))
# final =msp.add_lwpolyline(result)
# final.close()


#Saves all our lines as a file
doc.saveas("lwpolyline1.dxf")


#This bit is temporary and due a rework, dont really understand what ive done
#but it works
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
