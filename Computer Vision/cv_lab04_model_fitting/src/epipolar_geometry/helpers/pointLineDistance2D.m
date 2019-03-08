function [ d ] = pointLineDistance2D( p, l )
%Computes the distance between a line given as ax+by+c=0
%and a point.

    a=l(1);
    b=l(2);
    c=l(3);
    x=p(1);
    y=p(2);
    
    d=norm(a*x+b*y+c)/sqrt(a^2+b^2);


end

