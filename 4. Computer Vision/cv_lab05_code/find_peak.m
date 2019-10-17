function [ peak ] = find_peak( points, p, r, tol )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

[N, ~]=size(points);
centershift=tol+1;
center=p;

    while centershift>tol
        dist_to_center = sqrt(sum((repmat(center,N,1) - points).^2,2));   
        neighbours = points(dist_to_center < r,:);
        oldcenter=center;
        center=mean(neighbours,1);
        centershift=norm(center-oldcenter);
    end
    peak=center;
end

