function [k, b] = ransacLine(data, iter, threshold)
% data: a 2xn dataset with #n data points
% iter: the number of iterations
% threshold: the threshold of the distances between points and the fitting line

num_pts = size(data,2); % Total number of points
max_inliers = 0;       % Best fitting line with largest number of inliers
k=0; b=0;                % parameters for best fitting line
for i=1:iter
    % Randomly select 2 points and fit line to these
    % Tip: Matlab command randperm is useful here 
    rand_id=randperm(num_pts,2);
    p1=data(:,rand_id(1));
    p2=data(:,rand_id(2));
    % Model is y = k*x + b
    
    ki=(p2(2)-p1(2))/(p2(1)-p1(1));
    bi=p1(2)-ki*p1(1);
    % Compute the distances between all points with the fitting line    
    dist=vecnorm(data(2,:)-ki*data(1,:)-bi)/sqrt(1+ki^2);
    % Compute the inliers with distances smaller than the threshold
    inliers_id=find(dist<threshold);
    inliers=data(:,inliers_id);
    % Update the number of inliers and fitting model if better model is found
    nb_inliers= length(inliers_id);
    if nb_inliers>max_inliers
        max_inliers=nb_inliers;
        k=ki;
        b=bi;
        best_inliers=inliers;
    end
end
[~,k, b]=regression(best_inliers(1,:),best_inliers(2,:));
end
