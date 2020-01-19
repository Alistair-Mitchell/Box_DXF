import ezdxf
from ezdxf.math import *

doc = ezdxf.new('R2000')
msp = doc.modelspace()

t = 3
w = 155
wn =4
hwanted = 80
h =hwanted+2*t
hn =5
d = 0
dn =0

def StepMaker(StartX,StartY,Length,Number,XMajor,MajorMirror,MinorMirror,Add):
    if MajorMirror == 1:
        MM = 1
    else:
        MM=-1
    if MinorMirror == 1:
        MnM = -1
    else:
        MnM=1
    inc = Length/Number
    iter = (Number*2)-1
    result=[0]*iter

    for i in range(iter):
        A = (((i)%2)+(i))/2
        B = ((((i-1)%2)+(i-1))/2)%2
        # wx[i] = [A*w_l, B*t*(-1)]
        C = A*inc*MnM
        D = B*t*MM
        if XMajor == 0:
            result[i] = [D+StartX,C+StartY]
        else:
            result[i] = [C+StartX,D+StartY]
    if Add == 0:
        return result
    else:
        test=msp.add_lwpolyline(result)


A1=StepMaker(0,0,w,wn,1,0,0,0)
A2=StepMaker(w,0,h,hn,0,1,1,0)
A3=StepMaker(w,-h,w,wn,1,1,1,0)
A4=StepMaker(0,-h,h,hn,0,0,0,0)
source = A1+A2+A3+A4
result = list(offset_vertices_2d(source, offset=0.5, closed=True))
final =msp.add_lwpolyline(result)
final.close()


print(A2)



doc.saveas("lwpolyline1.dxf")
