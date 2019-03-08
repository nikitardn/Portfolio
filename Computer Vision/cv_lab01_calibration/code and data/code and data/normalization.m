function [xyn, XYZn, T, U] = normalization(xy, XYZ)

%data normalization
%centroid
cI=mean(xy');
cO=mean(XYZ');

%scaling
distI=0;
distO=0;
N=length(xy);
for i=1:N
    distI=distI+norm(xy(:,i)-cI')/N;
    distO=distO+norm(XYZ(:,i)-cO')/N;
end

alphaI= sqrt(2)/distI;
alphaO= sqrt(3)/distO;

T=alphaI*[1 0 -cI(1);
          0 1 -cI(2);
          0 0 1/alphaI];
      
U=alphaO*[1 0 0 -cO(1);
          0 1 0 -cO(2);
          0 0 1 -cO(3);
          0 0 0 1/alphaO];

xyn = T*xy;
XYZn = U*XYZ;

end