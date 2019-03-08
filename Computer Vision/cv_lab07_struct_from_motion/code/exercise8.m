% =========================================================================
% Exercise 8
% =========================================================================

% Initialize VLFeat (http://www.vlfeat.org/)
clc
close all
clear variables

constants;
img1 = single(imread(imgName1));
img2 = single(imread(imgName2));

%extract SIFT features and match

[fa, da] = vl_sift(img1,'PeakThresh',SIFT_tresh);
[fb, db] = vl_sift(img2,'PeakThresh',SIFT_tresh);

%don't take features at the top of the image - only background
filter = fa(2,:) > 100;
fa = fa(:,find(filter));
da = da(:,find(filter));

[matches, scores] = vl_ubcmatch(da, db);

% showFeatureMatches(img1, fa(1:2, matches(1,:)), img2, fb(1:2, matches(2,:)), 20);

%% Compute essential matrix and projection matrices and triangulate matched points

%use 8-point ransac or 5-point ransac - compute (you can also optimize it to get best possible results)
%and decompose the essential matrix and create the projection matrices
x1s = [fa(1:2, matches(1,:)); ones(1,size(matches,2))];
x2s = [fb(1:2, matches(2,:)); ones(1,size(matches,2))];
Ps{1} = eye(4);
[F, inliers] = ransacfitfundmatrix(x1s, x2s, F_tresh);
showFeatureMatches(img1, x1s(1:2,:), img2, x2s(1:2,:),inliers, 2);

x1_calibrated=K\x1s(:,inliers);
x2_calibrated=K\x2s(:,inliers);

E=K'*F*K;
% draw epipolar lines in img 1
figure(7),hold off, imshow(img1, []); hold on, plot(x1s(1,inliers), x1s(2,inliers), '*r');
figure(8),hold off, imshow(img2, []); hold on, plot(x2s(1,inliers), x2s(2,inliers), '*b');
figure(7)
for k = 1:size(inliers,2)
    drawEpipolarLines(F'*x2s(:,inliers(k)), img1);
end
% saveas(gcf,'../plots/epilines1.png');
% draw epipolar lines in img 2
figure(8)
for k = 1:size(inliers,2)
    drawEpipolarLines(F*x1s(:,inliers(k)), img2);
end
% saveas(gcf,'../plots/epilines2.png');
Ps{2} = decomposeE(E, x1_calibrated, x2_calibrated);


%triangulate the inlier matches with the computed projection matrix
[X2, err] = linearTriangulation(Ps{1}, x1_calibrated, Ps{2}, x2_calibrated);
%prepare for additional views
da=da(:,matches(1,inliers));
fa=fa(:,matches(1,inliers));


%% Add an addtional view of the scene 

img3 = single(imread(imgName3));
[X3,Ps,x1,x3] = AddView(img1,img3,X2,da,fa,Ps,3);
%% Add more views...

img4 = single(imread(imgName4));
[X4,Ps] = AddView(img1,img4,X2,da,fa,Ps,4);

img5 = single(imread(imgName5));
[X5,Ps] = AddView(img1,img5,X2,da,fa,Ps,5);

%% Plot stuff
figure(1)
plot3(X2(1,:),X2(2,:),X2(3,:),'.'); hold on
plot3(X3(1,:),X3(2,:),X3(3,:),'.'); 
plot3(X4(1,:),X4(2,:),X4(3,:),'.'); 
plot3(X5(1,:),X5(2,:),X5(3,:),'.');
drawCameras(Ps,gcf)

legend('2nd view','3rd view','4th view','5th view');
xlabel('x [m]');
ylabel('y [m]');
zlabel('z [m]');
% saveas(gcf,'../plots/3D_plot.png');

%% Dense reconstruction
% close all
% fprintf('Dense 3d\n');
% [coords,mask] = Dense3D(img1,img3,x1,x3,Ps{3});
% imshow(mask)
% generateObjFile('model3D','imgRectL.png',coords,mask);
% fprintf('done\n');