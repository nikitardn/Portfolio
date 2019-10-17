clc
clear all
close all

IMG_NAME1 = 'images/I1.jpg';
IMG_NAME2 = 'images/I2.jpg';

% read in image
img1 = im2double(imread(IMG_NAME1));
img2 = im2double(imread(IMG_NAME2));

img1 = imresize(img1, 1);
img2 = imresize(img2, 1);

% convert to gray image
imgBW1 = rgb2gray(img1);
imgBW2 = rgb2gray(img2);
imgBW1=255/max(max(imgBW1))*imgBW1;
imgBW2=255/max(max(imgBW2))*imgBW2;

% use the SIFT detector from the vlfeat toolbox
[fa, da] = vl_sift(single(imgBW1), 'PeakThresh', 13) ;
[fb, db] = vl_sift(single(imgBW2), 'PeakThresh', 13) ;
[matches, scores] = vl_ubcmatch(da, db) ;
showFeatureMatches(img1, fa(1:2, matches(1,:)), img2, fb(1:2, matches(2,:)), 20);
saveas(gcf,'results/SIFT_toolbox.png');