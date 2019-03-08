function run_ex5()
close all

% choose image
img = imread('cow.jpg');
name=strcat('cow');
% img = imread('zebra_b.jpg');
% name=strcat('zebra_b');

% for faster debugging you might want to decrease the size of your image
imgr=imresize(img,1);

figure(1), imshow(img), title('original image')
%imwrite(img,strcat('plots/','cow_','original.png'));

% smooth image (6.1a)
H = fspecial('gaussian',[5 5],5);
imgSmoothed = imfilter(imgr,H,'replicate');
%figure(2), imshow(imgSmoothed), title('smoothed image')

% convert to L*a*b* image (6.1b)
cform = makecform('srgb2lab');
imglab = applycform(imgSmoothed,cform);
figure(3), imshow(imglab), title('l*a*b* image')
%imwrite(imglab,strcat('plots/','cow_','lab.png'));

% Choose the algorithm MeanShift or EM 
%% (6.2) MeanShift
%name=strcat(name,'_MS');
% tic
% [mapMS, peak] = meanshiftSeg(imglab);
% visualizeSegmentationResults (mapMS,peak,name);
% toc

%% (6.3) EM
K=4;
name=strcat(name,'_K',int2str(K));
tic
[mapEM, cluster] = EM(imglab,K);
visualizeSegmentationResults (mapEM,cluster,name);
toc
end