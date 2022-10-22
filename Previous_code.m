clc;
close all

wristwidth = 60; %mm

%reads the image
I1 = imread('Top.png');
I2 = imread('Side.png');
I1 = rgb2gray(I1);
I2 = rgb2gray(I2);
[rows, columns] = size(I1);
[rows2, columns2] = size(I2);

if (rows > rows2)
    maxr = rows;
    I3 = zeros(maxr,columns2);
    I4 = I1;
    for q=1:1:rows2
        for w=1:1:columns2
            I3(q,w) = I2(q,w);
        end
    end
    I = cat(2,I4,I3);
else
    maxr = rows2;
    I4 = I2;
    I3 = zeros(maxr,columns);
    for q=1:1:rows
        for w=1:1:columns
            I3(q,w) = I1(q,w);
        end
    end
    I = cat(2,I3,I4);
end

figure;
imshow(I);


%defines scale of xray images based on a 'real world' dimension
[widthx, widthy] = ginput(2);
distanceInPixels = sqrt((widthx(1)-widthx(2))^2 +(widthy(1)-widthy(2))^2);
pixelwidth = distanceInPixels/60;
MM = pixelwidth*6;

%identifies boney features. 1&3 are ulna 2&4 are radius
[x,y] = ginput(6);
%the y coordinate of the second image is matched to the first for
%simplicity, this may need to change
%y(4) = y(2);
%the second pinning input is a set distance away from the first
%x(5) = x(2)-MM*2;
%x(6) = x(4)-MM;
%y(5) = y(2)+MM*0.9;
%y(6) = y(4)+MM*1.3;

%adds appropriate markers
for i = 1:6
    I=insertMarker(I,[x(i) y(i)],'x','color','red','size',20);
end
imshow(I)

%identifies fracture location and labels
[u,v] = ginput(4);
line(u(1:2), v(1:2), 'color','red', 'linestyle', '--', 'linewidth', 2);
line(u(3:4), v(3:4), 'color','red', 'linestyle', '--', 'linewidth', 2);

%determines the length of each line and their angle to the normal
ul1 = abs(u(1)-u(2));
vl1 = abs(v(1)-v(2));
vl = v(1)-v(2);
theata = atan(vl/ul1)*180/pi();
ul2 = abs(u(3)-u(4));
vl2 = abs(v(3)-v(4));
vl = v(3)-v(4);
alpha = atan(vl/ul2)*180/pi();

%creates a vector for the fracture lines (xy) (zy) (xyz)
va = [u(1) - u(2), v(1) - v(2)];%, u(4) - u(3)];
vb = [u(3) - u(4), v(3) - v(4)];
vab = [u(1) - u(2), v(1) - v(2), u(3) - u(4)];


%sets up the iteration requierments and matricies
loops = 360;
r=0.25;
o = zeros(loops, 1);
a = zeros(loops, 1);
lines = zeros(2*loops, 9);

for q = 1:1:loops
    angle = q*(360/loops);
    %if (angle >10 && 170 > angle) || (angle > 190 && angle < 350) %
    %x and y coordinates on the anulus
    angle = angle*pi()/180;
    o(q) = r*sin(angle);
    a(q) = r*cos(angle);
    
    ul = 0.25*ul1+ul1*(0.5-r-a(q));
    vl = 0.25*vl1+vl1*(0.5-r-a(q));
    %adds the x coord to the matrix
    lines(2*q-1,1) = u(2)-ul;
    lines(2*q,1) = u(1)+ul;
    
    %adds the y coord to the matrix(checking if the fracture is angled
    %up or down and producess a line on the image appropriatly
    if (v(1) < v(2))
        line([x(2) u(2)-ul], [y(2) v(2)-vl], 'color','b', 'linewidth', 1);
        line([x(5) u(1)+ul], [y(5) v(1)+vl], 'color','b', 'linewidth', 1);
        lines(2*q-1,2) = v(2)-vl;
        lines(2*q,2) = v(1)+vl;
    else
        line([x(2) u(2)-ul], [y(2) v(2)+vl], 'color','b', 'linewidth', 1);
        line([x(5) u(1)+ul], [y(5) v(1)-vl], 'color','b', 'linewidth', 1);
        lines(2*q-1,2) = v(2)+vl;
        lines(2*q,2) = v(1)-vl;
    end
    %repeats the above for the second image
    ul = 0.25*ul2+ul2*(0.5-r-o(q));
    vl = 0.25*vl2+vl2*(0.5-r-o(q));
    
    lines(2*q-1,3) = u(4)-ul;
    lines(2*q,3) = u(3)-ul;
    
    if (v(3) < v(4))
        line([x(4) u(4)-ul], [y(4) v(4)-vl], 'color','b', 'linewidth', 1);
        line([x(6) u(3)+ul], [y(6) v(3)+vl], 'color','b', 'linewidth', 1);
        lines(2*q-1,4) = v(4)-vl;
        lines(2*q,4) = v(3)+vl;
    else
        line([x(4) u(4)-ul], [y(4) v(4)+vl], 'color','b', 'linewidth', 1);
        line([x(6) u(3)+ul], [y(6) v(3)-vl], 'color','b', 'linewidth', 1);
        lines(2*q-1,4) = v(4)+vl;
        lines(2*q,4) = v(3)-vl;
    end
    %creates vecotrs for each line. 2D and 3D
    vc = [lines(2*q-1,1) - x(2), lines(2*q-1,2) - y(2)];
    vd = [lines(2*q,1) - x(5), lines(2*q,2) - y(5)];
    ve = [lines(2*q-1,3) - x(4), lines(2*q-1,4) - y(4)];
    vf = [lines(2*q,3) - x(6), lines(2*q,4) - y(6)];
    
    vce = [lines(2*q-1,1) - x(2), lines(2*q-1,2) - y(2), lines(2*q-1,3) - x(4)];
    vdf = [lines(2*q,1) - x(5), lines(2*q,2) - y(5), lines(2*q,3) - x(6)];
    
    %checks the angle to the plane for (xy) and (zy) before (xyz)
    lines(2*q-1,5) = acosd(dot(va, vc) / (norm(va) * norm(vc)));
    lines(2*q,5) = acosd(dot(va, vd) / (norm(va) * norm(vd)));
    
    lines(2*q-1,6) = acosd(dot(vb, ve) / (norm(vb) * norm(ve)));
    lines(2*q,6) = acosd(dot(vb, vf) / (norm(vb) * norm(vf)));
    
    lines(2*q-1,7) = acosd(dot(vab, vce) / (norm(vab) * norm(vce)));
    lines(2*q,7) = acosd(dot(vab, vdf) / (norm(vab) * norm(vdf)));
    
    %n = cross(vce, vdf);
    %d = abs(n'*((lines(2*q-1,1)-(lines(2*q-1,2) - y(2))))/sqrt(n'*n))
    
    %if the line is above the ideal threshold of 60 degrees validates it
    if (lines(2*q-1,7) > 60 && lines(2*q,7) > 60 && lines(2*q-1,7) < 120 && lines(2*q,7) < 120)
        lines(2*q-1,9) = 1;
        lines(2*q,9) = 1;
    elseif (lines(2*q-1,7) > 45 && lines(2*q,7) > 45 && lines(2*q-1,7) < 135 && lines(2*q,7) < 135)
        lines(2*q-1,9) = 2;
        lines(2*q,9) = 2;
    %end
    end
end
%if each 2D line is above the threshold validates it
for q = 1:1:2*loops
    if (lines(q,5) > 60 && lines(q,6) > 60 && lines(q,5) < 120 && lines(q,6) < 120)
        lines(q,8) = 1;
    elseif (lines(q,5) > 45 && lines(q,6) > 45 && lines(q,5) < 135 && lines(q,6) < 135)
        lines(q,8) = 2;
    end
end
for q = 1:1:2*loops
     if(lines(q,5) > 60 && lines(q,6) > 60 && lines(q,5) < 120 && lines(q,6) < 120)
         lines(q,8) = 1;
     elseif (lines(q,5) > 45 && lines(q,6) > 45 && lines(q,5) < 135 && lines(q,6) < 135)
         lines(q,8) = 2;
     end
end

%finds the 'best' angle set for pinning
pastval = 90;
co = 0;
for q = 1:1:loops
    if (lines(2*q-1,8) == 1 && lines(2*q,8) == 1 && lines(2*q,9) == 1)
        val = lines(2*q-1,7)+lines(2*q,7);
        if val > pastval
            pastval = val;
            co = 2*q;
        end
    elseif (((lines(2*q,8) == 2 && lines(2*q-1,8) == 1) || (lines(2*q,8) && lines(2*q-1,8) ==2)) && lines(2*q,9) == 1)
        val = lines(2*q-1,7)+lines(2*q,7);
        if val > pastval
            pastval = val;
            co = 2*q;
        end
    elseif (((lines(2*q,8) == 2 && lines(2*q-1,8) == 1) || (lines(2*q,8) && lines(2*q-1,8) ==2)) && lines(2*q,9) == 2)
        val = lines(2*q-1,7)+lines(2*q,7);
        if val > pastval
            pastval = val;
            co = 2*q;
        end
    elseif (lines(2*q,8) == 2 && lines(2*q-1,8) == 2 && lines(2*q,9) == 1)
        val = lines(2*q-1,7)+lines(2*q,7);
        if val > pastval
            pastval = val;
            co = 2*q;
        end
    elseif (lines(2*q,8) == 2 && lines(2*q-1,8) == 2 && lines(2*q,9) == 2)
        val = lines(2*q-1,7)+lines(2*q,7);
        if val > pastval
            pastval = val;
            co = 2*q;
        end
    elseif ((lines(2*q-1,8) == 0 && lines(2*q,8) == 2) || (lines(2*q-1,8) == 2 && lines(2*q,8) == 0) && lines(2*q,9) == 1)
        val = lines(2*q-1,7)+lines(2*q,7);
        if val > pastval
            pastval = val;
            co = 2*q;
        end
    end
end


%plots the best pinning angle if available
%if exist('co','var') == 1
H1= 0.1*rows;

    dx = abs(x(4)-lines(co-1,3));
    dy = abs(y(4)-lines(co-1,4));
    omega = atan(dx/dy);
    %H1 = sqrt(dx^2 + dy^2);  
    O2 = 3*H1*sin(omega);
    A2 = 3*H1*cos(omega);
line([x(4) lines(co-1,3)+O2], [y(4) lines(co-1,4)+A2], 'color','g','linewidth', 2);

    dx = abs(x(2)-lines(co-1,1));
    dy = abs(y(2)-lines(co-1,2));
    omega = atan(dx/dy);
    %H1 = sqrt(dx^2 + dy^2);  
    O2 = 3*H1*sin(omega);
    A2 = 3*H1*cos(omega);
line([x(2) lines(co-1,1)-O2], [y(2) lines(co-1,2)+A2], 'color','g','linewidth', 2);

    dx = abs(x(5)-lines(co-1,1));
    dy = abs(y(5)-lines(co-1,2));
    omega = atan(dx/dy);
    %H1 = sqrt(dx^2 + dy^2);  
    O2 = 3*H1*sin(omega);
    A2 = 3*H1*cos(omega);
line([x(5) lines(co,1)+O2], [y(5) lines(co-1,2)+A2], 'color','g','linewidth', 2);

    dx = abs(x(6)-lines(co-1,3));
    dy = abs(y(6)-lines(co-1,4));
    omega = atan(dx/dy);
    %H1 = sqrt(dx^2 + dy^2);  
    O2 = 3*H1*sin(omega);
    A2 = 3*H1*cos(omega);
line([x(6) lines(co,3)-O2], [y(-6) lines(co-1,4)+A2], 'color','g','linewidth', 2);
