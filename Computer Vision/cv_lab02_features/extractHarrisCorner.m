% extract harris corner
%
% Input:
%   img           - n x m gray scale image
%   thresh        - scalar value to threshold corner strength
%   
% Output:
%   corners       - 2 x k matrix storing the keypoint coordinates
%   H             - n x m gray scale image storing the corner strength
function [corners, H] = extractHarrisCorner(img, thresh)

img= imgaussfilt(img);
[Ix,Iy]=gradient(img);
Wsize=3;
[maxy maxx]=size(Ix);
corners=[];

%compute subelements of H
Ixsq=Ix.*Ix;
Iysq=Iy.*Iy;
IxIy=Ix.*Iy;

H11=movsum(movsum(Ixsq,Wsize,1),Wsize,2);
H12=movsum(movsum(IxIy,Wsize,1),Wsize,2);
H22=movsum(movsum(Iysq,Wsize,1),Wsize,2);

% Compute the response matrix K-> much faster that a loop
K=(H11.*H22-H12.^2)./(H11+H22);
%histogram(K);

%remove unwanted elements from K -> threshold and non-maximum
for i=1:maxy
    for j =1:maxx
        if K(i,j)< thresh || K(i,j)< max(max(K(i-1:i+1,j-1:j+1)))
                K(i,j)=0;
        else
            corners=[corners [j ;i]];
        end
    end
end
H=K;
end