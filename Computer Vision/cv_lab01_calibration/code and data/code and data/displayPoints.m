function [ output_args ] = displayPoints( xy, xy_hat,savename )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

IMG_NAME = 'images/image002.jpg';
img = imread(IMG_NAME);
image(img);
hold on;
plot(xy(1,:), xy(2,:), 'ro')
plot(xy_hat(1,:), xy_hat(2,:), 'g*')
saveas(gcf,strcat(savename,'.png'));
end

