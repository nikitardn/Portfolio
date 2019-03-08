% Compute the essential matrix using the eight point algorithm
% Input
% 	x1s, x2s 	Point correspondences 3xn matrices
%
% Output
% 	Eh 			Essential matrix with the det F = 0 constraint and the constraint that the first two singular values are equal
% 	E 			Initial essential matrix obtained from the eight point algorithm
%

function [Eh, E] = essentialMatrix(x1s, x2s)
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
    e=V(:,end);
    E=[e(1:3)'; e(4:6)'; e(7:9)';];    
    [U,S,V] = svd(E);
    S(3,3)=0;
%     s=mean(diag(S));
%     S(2,2)=s;
%     S(1,1)=s;
    Eh=U*S*V';
    
    E=T2'*E*T1;
    Eh=T2'*Eh*T1;
end
