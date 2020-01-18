import ezdxf

doc = ezdxf.new('R2000')
msp = doc.modelspace()

t = 3
w = 155
wn =3
hwanted = 80
h =hwanted+2*t
hn =3
d = 0
dn =0

def StepMaker(StartX,StartY,Length,Number,XMajor,MajorMirror,Add):
    if MajorMirror == 1:
        MM = 1
    else:
        MM=-1
    inc = Length/Number
    iter = Number*2
    result=[0]*iter

    for i in range(iter):
        A = (((i)%2)+(i))/2
        B = ((((i-1)%2)+(i-1))/2)%2
        # wx[i] = [A*w_l, B*t*(-1)]
        C = A*inc
        D = B*t*MM
        if XMajor == 0:
            result[i] = [D+StartX,C+StartY]
        else:
            result[i] = [C+StartX,D+StartY]
    if Add == 0:
        return result
    else:
        msp.add_lwpolyline(result)


StepMaker(0,0,w,wn,1,0,1)
StepMaker(0,-h,h,hn,0,0,1)
StepMaker(0,-h,w,wn,1,1,1)
StepMaker(w,-h,h,hn,0,1,1)


doc.saveas("lwpolyline1.dxf")
