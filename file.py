import os
import numpy as np
import pylab as plt

#os.system('close')
#os.system('cls')
wristwidth = 60

#reads the image
I1 = plt.imread("C:\\Users\\Ibrahim\\Desktop\\top.png")
I2 = plt.imread("C:\\Users\\Ibrahim\\Desktop\\side.png")
#I1 = rgb2gray(I1)
#I2 = rgb2gray(I2)

# Grid lines at these intervals (in pixels)
# dx and dy can be different but same is used below
dx, dy = 100,100

# Custom (rgb) grid color
grid_color = [0,0,0]


# Modify the image to include the grid
I1[:,::dy,:] = grid_color
I1[::dx,:,:] = grid_color

I2[:,::dy,:] = grid_color
I2[::dx,:,:] = grid_color

# Show the result
plt.imshow(I1)
plt.show()

rows,columns = I1.shape
rows2,columns2 = I2.shape
if (rows > rows2):
    maxr = rows
    I3 = np.zeros((maxr,columns2))
    I4 = I1
    for q in np.arange(1,rows2+1,1).reshape(-1):
        for w in np.arange(1,columns2+1,1).reshape(-1):
            I3[q,w] = I2(q,w)
    I = np.concatenate((I4,I3.T), axis=1)

    maxr = rows2
    I4 = I2
    I3 = np.zeros((maxr,columns))
    for q in np.arange(1,rows+1,1).reshape(-1):
        for w in np.arange(1,columns+1,1).reshape(-1):
            I3[q,w] = I1(q,w)
    I = np.concatenate((I3,I4.T), axis=1)


plt.imshow(I)
#defines scale of xray images based on a 'real world' dimension
widthx,widthy = ginput(2)
distanceInPixels = np.sqrt((widthx(1) - widthx(2)) ** 2 + (widthy(1) - widthy(2)) ** 2)
pixelwidth = distanceInPixels / 60
MM = pixelwidth * 6
#identifies boney features. 1&3 are ulna 2&4 are radius
x,y = ginput(6)
#the y coordinate of the second image is matched to the first for
#simplicity, this may need to change
#y(4) = y(2);
#the second pinning input is a set distance away from the first
#x(5) = x(2)-MM*2;
#x(6) = x(4)-MM;
#y(5) = y(2)+MM*0.9;
#y(6) = y(4)+MM*1.3;

#adds appropriate markers
for i in np.arange(1,6+1).reshape(-1):
    I = insertMarker(I,np.array([x(i),y(i)]),'x','color','red','size',20)

plt.imshow(I)
#identifies fracture location and labels
u,v = ginput(4)
plt.plot(u(np.arange(1,2+1)),v(np.arange(1,2+1)),'color','red','linestyle','--','linewidth',2)
plt.plot(u(np.arange(3,4+1)),v(np.arange(3,4+1)),'color','red','linestyle','--','linewidth',2)
#determines the length of each line and their angle to the normal
ul1 = np.abs(u(1) - u(2))
vl1 = np.abs(v(1) - v(2))
vl = v(1) - v(2)
theata = np.arctan(vl / ul1) * 180 / np.pi()
ul2 = np.abs(u(3) - u(4))
vl2 = np.abs(v(3) - v(4))
vl = v(3) - v(4)
alpha = np.arctan(vl / ul2) * 180 / np.pi()
#creates a vector for the fracture lines (xy) (zy) (xyz)
va = np.array([u(1) - u(2),v(1) - v(2)])

vb = np.array([u(3) - u(4),v(3) - v(4)])
vab = np.array([u(1) - u(2),v(1) - v(2),u(3) - u(4)])
#sets up the iteration requierments and matricies
loops = 360
r = 0.25
o = np.zeros((loops,1))
a = np.zeros((loops,1))
lines = np.zeros((2 * loops,9)) ##double check this
for q in np.arange(1,loops+1,1).reshape(-1):
    angle = q * (360 / loops)
    #if (angle >10 && 170 > angle) || (angle > 190 && angle < 350) #
#x and y coordinates on the anulus
    angle = angle * np.pi() / 180
    o[q] = r * np.sin(angle)
    a[q] = r * np.cos(angle)
    ul = 0.25 * ul1 + ul1 * (0.5 - r - a(q))
    vl = 0.25 * vl1 + vl1 * (0.5 - r - a(q))
    #adds the x coord to the matrix
    lines[2 * q - 1,1] = u(2) - ul
    lines[2 * q,1] = u(1) + ul
    #adds the y coord to the matrix(checking if the fracture is angled
#up or down and produces a line on the image appropriately
    if (v(1) < v(2)):
        plt.plot(np.array([x(2),u(2) - ul]),np.array([y(2),v(2) - vl]),'color','b','linewidth',1)
        plt.plot(np.array([x(5),u(1) + ul]),np.array([y(5),v(1) + vl]),'color','b','linewidth',1)
        lines[2 * q - 1,2] = v(2) - vl
        lines[2 * q,2] = v(1) + vl
    else:
        plt.plot(np.array([x(2),u(2) - ul]),np.array([y(2),v(2) + vl]),'color','b','linewidth',1)
        plt.plot(np.array([x(5),u(1) + ul]),np.array([y(5),v(1) - vl]),'color','b','linewidth',1)
        lines[2 * q - 1,2] = v(2) + vl
        lines[2 * q,2] = v(1) - vl
    #repeats the above for the second image
    ul = 0.25 * ul2 + ul2 * (0.5 - r - o(q))
    vl = 0.25 * vl2 + vl2 * (0.5 - r - o(q))
    lines[2 * q - 1,3] = u(4) - ul
    lines[2 * q,3] = u(3) - ul
    if (v(3) < v(4)):
        plt.plot(np.array([x(4),u(4) - ul]),np.array([y(4),v(4) - vl]),'color','b','linewidth',1)
        plt.plot(np.array([x(6),u(3) + ul]),np.array([y(6),v(3) + vl]),'color','b','linewidth',1)
        lines[2 * q - 1,4] = v(4) - vl
        lines[2 * q,4] = v(3) + vl
    else:
        plt.plot(np.array([x(4),u(4) - ul]),np.array([y(4),v(4) + vl]),'color','b','linewidth',1)
        plt.plot(np.array([x(6),u(3) + ul]),np.array([y(6),v(3) - vl]),'color','b','linewidth',1)
        lines[2 * q - 1,4] = v(4) + vl
        lines[2 * q,4] = v(3) - vl
    #creates vecotrs for each line. 2D and 3D
    vc = np.array([lines(2 * q - 1,1) - x(2),lines(2 * q - 1,2) - y(2)])
    vd = np.array([lines(2 * q,1) - x(5),lines(2 * q,2) - y(5)])
    ve = np.array([lines(2 * q - 1,3) - x(4),lines(2 * q - 1,4) - y(4)])
    vf = np.array([lines(2 * q,3) - x(6),lines(2 * q,4) - y(6)])
    vce = np.array([lines(2 * q - 1,1) - x(2),lines(2 * q - 1,2) - y(2),lines(2 * q - 1,3) - x(4)])
    vdf = np.array([lines(2 * q,1) - x(5),lines(2 * q,2) - y(5),lines(2 * q,3) - x(6)])
    #checks the angle to the plane for (xy) and (zy) before (xyz)
    lines[2 * q - 1,5] = acosd(np.dot(va,vc) / (norm(va) * norm(vc)))
    lines[2 * q,5] = acosd(np.dot(va,vd) / (norm(va) * norm(vd)))
    lines[2 * q - 1,6] = acosd(np.dot(vb,ve) / (norm(vb) * norm(ve)))
    lines[2 * q,6] = acosd(np.dot(vb,vf) / (norm(vb) * norm(vf)))
    lines[2 * q - 1,7] = acosd(np.dot(vab,vce) / (norm(vab) * norm(vce)))
    lines[2 * q,7] = acosd(np.dot(vab,vdf) / (norm(vab) * norm(vdf)))
    #n = cross(vce, vdf);
#d = abs(n'*((lines(2*q-1,1)-(lines(2*q-1,2) - y(2))))/sqrt(n'*n))
    #if the line is above the ideal threshold of 60 degrees validates it
    if (lines(2 * q - 1,7) > 60 and lines(2 * q,7) > 60 and lines(2 * q - 1,7) < 120 and lines(2 * q,7) < 120):
        lines[2 * q - 1,9] = 1
        lines[2 * q,9] = 1
    else:
        if (lines(2 * q - 1,7) > 45 and lines(2 * q,7) > 45 and lines(2 * q - 1,7) < 135 and lines(2 * q,7) < 135):
            lines[2 * q - 1,9] = 2
            lines[2 * q,9] = 2
            #end

#if each 2D line is above the threshold validates it
for q in np.arange(1,2 * loops+1,1).reshape(-1):
    if (lines(q,5) > 60 and lines(q,6) > 60 and lines(q,5) < 120 and lines(q,6) < 120):
        lines[q,8] = 1
    else:
        if (lines(q,5) > 45 and lines(q,6) > 45 and lines(q,5) < 135 and lines(q,6) < 135):
            lines[q,8] = 2

for q in np.arange(1,2 * loops+1,1).reshape(-1):
    if (lines(q,5) > 60 and lines(q,6) > 60 and lines(q,5) < 120 and lines(q,6) < 120):
        lines[q,8] = 1
    else:
        if (lines(q,5) > 45 and lines(q,6) > 45 and lines(q,5) < 135 and lines(q,6) < 135):
            lines[q,8] = 2

#finds the 'best' angle set for pinning
pastval = 90
co = 0
for q in np.arange(1,loops+1,1).reshape(-1):
    if (lines(2 * q - 1,8) == 1 and lines(2 * q,8) == 1 and lines(2 * q,9) == 1):
        val = lines(2 * q - 1,7) + lines(2 * q,7)
        if val > pastval:
            pastval = val
            co = 2 * q
    else:
        if (((lines(2 * q,8) == 2 and lines(2 * q - 1,8) == 1) or (lines(2 * q,8) and lines(2 * q - 1,8) == 2)) and lines(2 * q,9) == 1):
            val = lines(2 * q - 1,7) + lines(2 * q,7)
            if val > pastval:
                pastval = val
                co = 2 * q
        else:
            if (((lines(2 * q,8) == 2 and lines(2 * q - 1,8) == 1) or (lines(2 * q,8) and lines(2 * q - 1,8) == 2)) and lines(2 * q,9) == 2):
                val = lines(2 * q - 1,7) + lines(2 * q,7)
                if val > pastval:
                    pastval = val
                    co = 2 * q
            else:
                if (lines(2 * q,8) == 2 and lines(2 * q - 1,8) == 2 and lines(2 * q,9) == 1):
                    val = lines(2 * q - 1,7) + lines(2 * q,7)
                    if val > pastval:
                        pastval = val
                        co = 2 * q
                else:
                    if (lines(2 * q,8) == 2 and lines(2 * q - 1,8) == 2 and lines(2 * q,9) == 2):
                        val = lines(2 * q - 1,7) + lines(2 * q,7)
                        if val > pastval:
                            pastval = val
                            co = 2 * q
                    else:
                        if ((lines(2 * q - 1,8) == 0 and lines(2 * q,8) == 2) or (lines(2 * q - 1,8) == 2 and lines(2 * q,8) == 0) and lines(2 * q,9) == 1):
                            val = lines(2 * q - 1,7) + lines(2 * q,7)
                            if val > pastval:
                                pastval = val
                                co = 2 * q

#plots the best pinning angle if available
#if exist('co','var') == 1
H1 = 0.1 * rows
dx = np.abs(x(4) - lines(co - 1,3))
dy = np.abs(y(4) - lines(co - 1,4))
omega = np.arctan(dx / dy)
#H1 = sqrt(dx^2 + dy^2);
O2 = 3 * H1 * np.sin(omega)
A2 = 3 * H1 * np.cos(omega)
plt.plot(np.array([x(4),lines(co - 1,3) + O2]),np.array([y(4),lines(co - 1,4) + A2]),'color','g','linewidth',2)
dx = np.abs(x(2) - lines(co - 1,1))
dy = np.abs(y(2) - lines(co - 1,2))
omega = np.arctan(dx / dy)
#H1 = sqrt(dx^2 + dy^2);
O2 = 3 * H1 * np.sin(omega)
A2 = 3 * H1 * np.cos(omega)
plt.plot(np.array([x(2),lines(co - 1,1) - O2]),np.array([y(2),lines(co - 1,2) + A2]),'color','g','linewidth',2)
dx = np.abs(x(5) - lines(co - 1,1))
dy = np.abs(y(5) - lines(co - 1,2))
omega = np.arctan(dx / dy)
#H1 = sqrt(dx^2 + dy^2);
O2 = 3 * H1 * np.sin(omega)
A2 = 3 * H1 * np.cos(omega)
plt.plot(np.array([x(5),lines(co,1) + O2]),np.array([y(5),lines(co - 1,2) + A2]),'color','g','linewidth',2)
dx = np.abs(x(6) - lines(co - 1,3))
dy = np.abs(y(6) - lines(co - 1,4))
omega = np.arctan(dx / dy)
#H1 = sqrt(dx^2 + dy^2);
O2 = 3 * H1 * np.sin(omega)
A2 = 3 * H1 * np.cos(omega)
plt.plot(np.array([x(6),lines(co,3) - O2]),np.array([y(- 6),lines(co - 1,4) + A2]),'color','g','linewidth',2)