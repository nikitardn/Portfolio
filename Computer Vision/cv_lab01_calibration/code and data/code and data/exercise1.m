% Exervice 2
%
close all;
clear all;

IMG_NAME = 'images/image002.jpg';

%This function displays the calibration image and allows the user to click
%in the image to get the input points. Left click on the chessboard corners
%and type the 3D coordinates of the clicked points in to the input box that
%appears after the click. You can also zoom in to the image to get more
%precise coordinates. To finish use the right mouse button for the last
%point.
%You don't have to do this all the time, just store the resulting xy and
%XYZ matrices and use them as input for your algorithms.
% [xy XYZ] = getpoints(IMG_NAME);
load xy_perso.mat;
load XYZperso.mat;

%% Uncomment to use only 6 points
% xy=xy(:,1:6);
% XYZ2=XYZ2(:,1:6);

%% === Task 2 DLT algorithm ===
savename='plots/DLT 6 points unnorm';
[K, R, t, error] = runDLT(xy, XYZ2, savename);

%% === Task 3 Gold Standard algorithm === uncomment to use

% savename='plots/GoldStandard 19 points';
% [K, R, t, error] = runGoldStandard(xy, XYZ2, savename);


