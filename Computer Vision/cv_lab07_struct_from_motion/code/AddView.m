function [XS,Ps,x1s,xis] = AddView(img1,imgi,X2,da,fa,Ps,fig)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
constants;
[fc, dc] = vl_sift(imgi,'PeakThresh',SIFT_tresh);

i=size(Ps,2)+1;
%select matched descriptors from image 1

%match against the features from image 1 that where triangulated
[matches, ~] = vl_ubcmatch(da, dc);
% showFeatureMatches(img1, fa(1:2, matches(1,:)), img2, fc(1:2, matches(2,:)), 20);

x1s=[fa(1:2, matches(1,:)); ones(1,size(matches,2))];
xis=[fc(1:2, matches(2,:)); ones(1,size(matches,2))];
x1_calibrated=K\x1s;
xi_calibrated=K\xis;
%run 6-point ransac

[P, inliers] = ransacfitprojmatrix(xi_calibrated, X2(:,matches(1,:)), P_tresh);
showFeatureMatches(img1, x1s(1:2,:), imgi, xis(1:2,:),inliers, 2);
if det(P(1:3,1:3))<0
    P(1:3,1:3)=-P(1:3,1:3);
    P(1:3,4)=-P(1:3,4);
end
Ps{i}=P;
x1s=x1s(:,inliers);
xis=xis(:,inliers);
x1_calibrated=x1_calibrated(:,inliers);
xi_calibrated=xi_calibrated(:,inliers);


% saveas(gcf,strcat('../plots/matches_',int2str(fig),'.png'));
%triangulate the inlier matches with the computed projection matrix
[XS, err] = linearTriangulation(Ps{1}, x1_calibrated, Ps{i}, xi_calibrated);

end

