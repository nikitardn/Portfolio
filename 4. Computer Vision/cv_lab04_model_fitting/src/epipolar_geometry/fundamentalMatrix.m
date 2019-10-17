% Compute the fundamental matrix using the eight point algorithm
% Input
% 	x1s, x2s 	Point correspondences
%
% Output
% 	Fh 			Fundamental matrix with the det F = 0 constraint
% 	F 			Initial fundamental matrix obtained from the eight point algorithm
%
function [Fh, F] = fundamentalMatrix(x1s, x2s)

    %normalization
    [x1s,T1]=normalizePoints2d(x1s);
    [x2s,T2]=normalizePoints2d(x2s);
    
    A1=x1s(1,:)'.*x2s(1,:)';
    A2=x1s(2,:)'.*x2s(1,:)';
    A3=x2s(1,:)';
    A4=x1s(1,:)'.*x2s(2,:)';
    A5=x1s(2,:)'.*x2s(2,:)';
    A6=x2s(2,:)';
    A7=x1s(1,:)';
    A8=x1s(2,:)';
    A9=ones(length(x1s(1,:)),1);
    A=[A1 A2 A3 A4 A5 A6 A7 A8 A9];
    
    
    [U,S,V] = svd(A);
    f=V(:,end);
    F=[f(1:3)'; f(4:6)'; f(7:9)'];
    F=T2'*F*T1;
    
    [U,S,V] = svd(F);
    S(3,3)=0;
    Fh=U*S*V';
end