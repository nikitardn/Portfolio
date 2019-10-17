load('../data/params.mat')
params.alpha=0.0;
params.model=0;
params.sigma_observe=1;
params.sigma_velocity=5;
params.sigma_position=10;
params.initial_velocity=[15 0];
params.alpha=0.0;
videoName= 'video1';

condensationTracker(videoName,params);