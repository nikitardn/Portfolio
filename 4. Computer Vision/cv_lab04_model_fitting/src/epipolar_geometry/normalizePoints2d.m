% Normalization of 2d-pts
% Inputs: 
%           xs = 2d points
% Outputs:
%           nxs = normalized points
%           T = 3x3 normalization matrix
%               (s.t. nx=T*x when x is in homogenous coords)
function [xn, T] = normalizePoints2d(x)
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
