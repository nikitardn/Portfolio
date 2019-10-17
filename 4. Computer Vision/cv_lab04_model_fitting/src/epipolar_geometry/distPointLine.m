function d = distPointLine( p, l )
% d = distPointLine( point, line )
% point: inhomogeneous 2d point (2-vector)
% line: 2d homogeneous line equation (3-vector)
    a=l(1);
    b=l(2);
    c=l(3);
    x=p(1);
    y=p(2);
    
    d=norm(a*x+b*y+c)/sqrt(a^2+b^2);
end
