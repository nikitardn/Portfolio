function [P] = dlt(xy, XYZ)
%computes DLT, xy and XYZ should be normalized before calling this function

M= @(x,X) [X' 0 0 0 0 -x(1)*X';
           0 0 0 0 -X' x(2)*X'];
A=[];
for i=1:length(xy)
    A=[A;M(xy(:,i),XYZ(:,i))];
end
[U,S,V] = svd(A);
P=[V(1:4,end)';
   V(5:8,end)';
   V(9:12,end)'];