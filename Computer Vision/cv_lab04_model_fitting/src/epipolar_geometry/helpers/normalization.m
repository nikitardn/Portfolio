function [xn,T] = normalization(x)

%data normalization
%centroid
cI=mean(x');

%scaling
N=length(x);
distI=sum(vecnorm(x-repmat(cI',1,N)))/N;
   
alphaI= sqrt(2)/distI;

T=alphaI*[1 0 -cI(1);
          0 1 -cI(2);
          0 0 1/alphaI];
   

xn = T*x;

end