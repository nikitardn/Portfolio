% 1DOF ROBOT LOCALIZATION IN A CIRCULAR HALLWAY USING A HISTOGRAM FILTER
function MCLLocalization1DOFRobotInTheHallway
    clear all; %close all;
    global frame figure_handle plot_handle firstTime;

    fprintf('Loading the animation data...\n');
    load('animation.mat');
    fprintf('Animation data loaded\n');

    % Algorithm parameters
    simpar.circularHallway = 0; % 1:yes, 0:no
    simpar.animate = 1;         % 1: Draw the animation of the gaussian. 0: do not draw (speed up the simulation)
    simpar.nSteps = 500;        % number of steps of the algorithm
    simpar.domain = 850;        % domain size (in centimeters)
    simpar.xTrue_0 = [mod(abs(ceil(simpar.domain*randn(1))), simpar.domain); 20];
    simpar.numberOfParticles = 100;
    simpar.wk_stdev = 1;        % stddev of the noise used in acceleration to simulate the robot movement.
    simpar.door_locations = [222,326,611]; % Position of the doors (in centimetres). This is the Map definition.
    simpar.door_stdev= 90/4;    % +-2sigma of the door observation is assumend to be 90 cm which is the wide of the door
    simpar.odometry_stdev = 2;  % Odometry uncertainty. Std. deviation of a Gaussian pdf. [cm]
    simpar.T=1;                 % Simulation sample time

    % Fixe the position of the figure to the up left corner
    % Fixe the size depending on the screen size
    scrsz = get(0,'ScreenSize');
    figure_handle = figure(1);
    figure_handle.Position = [0 0 scrsz(3)/3 scrsz(4)];

    firstTime = ones(6);

    xTrue_k = simpar.xTrue_0;

    % Initial Robot belief is generated from the uniform distribution
    belief_particles = random('unif',0,simpar.domain,1,simpar.numberOfParticles);

    % The localization algorithm starts here %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for k = 1:simpar.nSteps
        DrawRobot(xTrue_k(1), simpar); % plots the robot

        xTrue_k_1=xTrue_k;
        xTrue_k=SimulateRobot(xTrue_k_1,simpar); % simulates the robot movement

        % robot step (>0 left, <0 right)
        uk=get_odometry(xTrue_k,xTrue_k_1,simpar);

        % zk=1 when a door has been sensed
        zk=get_measurements(xTrue_k(1),xTrue_k_1(1),simpar);

        fprintf('step=%d zk=%d uk=%f\n',k,zk,uk);

        % MCL. Particle filter to localize the robot and draws the particles
        belief_particles = MCL(belief_particles,uk,zk,simpar);

    end
end
% The Localization Algorith ends here %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Simulate how the robot moves %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function xTrue_kNew = SimulateRobot(xTrue_k, simpar)
    % We will need to update the robot position here taking into account the
    % noise in acceleration
    wk = randn(1)*simpar.wk_stdev;
    xTrue_kNew = [1 simpar.T; 0 1]* xTrue_k + [simpar.T^2/2; simpar.T] * wk;

    if simpar.circularHallway
        % the hallway is assumed to be circular
        xTrue_kNew=mod(xTrue_kNew,simpar.domain);
    else
        % the hallway is assumed to be linear
        if xTrue_kNew(1)>simpar.domain
            xTrue_kNew(1) = simpar.domain-mod(xTrue_kNew(1),simpar.domain);
            xTrue_kNew(2) = -xTrue_kNew(2); % change direction of motion
        end
        if xTrue_kNew(1)<0
            xTrue_kNew(1) = -xTrue_kNew(1);
            xTrue_kNew(2) = -xTrue_kNew(2); % change direction of motion
        end
    end
end

% Simulates the odometry measurements including noise%%%%%%%%%%%%%%%%%%
function uk = get_odometry(xTrue_k,xTrue_k_1,simpar)
%     uk=mod(xTrue_k(1)-xTrue_k_1(1)+simpar.odometry_stdev*randn(1),simpar.domain);
    speed = xTrue_k(1)-xTrue_k_1(1)+simpar.odometry_stdev*randn(1);
    uk = mod(abs(speed), simpar.domain) * sign(speed);
end

% Simulates the detection of doors by the robot sensor %%%%%%%%%%%%%%%%
function sensor = get_measurements(xTrue_k,xTrue_k_1,simpar)
    i=1;
    sensor = 0;
    while(i<=length(simpar.door_locations) && sensor ~= 1)
    if ((xTrue_k(1) >= simpar.door_locations(i) && simpar.door_locations(i)>= xTrue_k_1(1)) || (xTrue_k(1) <= simpar.door_locations(i) && simpar.door_locations(i)<= xTrue_k_1(1))) && (abs(xTrue_k(1)-xTrue_k_1(1))<180)
        sensor = 1;
    end
    i = i + 1;
    end
end

% Draws the robot
function DrawRobot(x, simpar)
    global frame figure_handle

    if simpar.animate
        figure(figure_handle);
        x = mod(x,simpar.domain);
        i=x*332/simpar.domain;

        % keep the frame within the correct boundaries
        if i<1, i=1; end
        if i>332, i=332; end

        subplot(6,1,1);
        image(frame(ceil(i)).image);  % axis equal;
    end
    drawnow;
end


% Plots a Gaussian using a bar plot %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function DrawParticles(sp,label,pdf,weight,simpar)
    global firstTime plot_handle figure_handle

    if simpar.animate
        if firstTime(sp)
            figure(figure_handle);
            subplot(6,1,sp);
            firstTime(sp)=0;
            plot_handle(sp)=scatter(pdf,zeros(1,simpar.numberOfParticles), ...
                                    weight*20+2, 'filled');
            axis([0 simpar.domain -0.1 1]);
            xlabel(label);
        else
            figure(figure_handle);
            subplot(6,1,sp);

            set(plot_handle(sp),'XData',pdf,'YData', ...
                zeros(1,simpar.numberOfParticles),'SizeData',weight*20+2);
        end
    end
end

function DrawGaussian(sp,label,pdf_values,simpar)
    global figure_handle

    if simpar.animate
        figure(figure_handle);
        subplot(6,1,sp);
        plot([1:simpar.domain],pdf_values,'-b');
        axis([0 simpar.domain 0 max(pdf_values)]);
        xlabel(label);
    end
end

function DrawWeights(sp,label,positions,weights,simpar)
    global figure_handle

    if simpar.animate
        figure(figure_handle);
        subplot(6,1,sp);
        bar(positions, weights);
        % axis([0 simpar.domain 0 max(weights)]);
        axis([0 simpar.domain 0 max(0.02, max(weights))]);
        xlabel(label);
    end
end

%Aplies the MCL algorithm and plots the results
function updated_belief_particles = MCL(priorbelief_particles,uk,zk,simpar)
    % This variable is not really needed, it is just for displaying purposes.
    measurement_model_particles =  ...
      pdf('Normal', 1:simpar.domain, simpar.door_locations(1), simpar.door_stdev) + ...
      pdf('Normal', 1:simpar.domain, simpar.door_locations(2), simpar.door_stdev) + ...
      pdf('Normal', 1:simpar.domain, simpar.door_locations(3), simpar.door_stdev);
    measurement_model_particles = measurement_model_particles / sum(measurement_model_particles);  % normalization

    % 1. Motion (prediction)
    predict_particles = sample_motion_model(uk, priorbelief_particles, simpar);

    % 2. Measurement
    particle_weights  = measurement_model(zk, predict_particles, simpar);

    % 3. Resampling
    updated_belief_particles = resampling(predict_particles, particle_weights, simpar);

    % plotting the pdfs for the animation
    DrawParticles(2,'prior', priorbelief_particles,ones(1,simpar.numberOfParticles),simpar);
    DrawParticles(3,'predict', predict_particles,ones(1,simpar.numberOfParticles),simpar);
    DrawGaussian (4,'measurement model', measurement_model_particles,simpar);
    DrawWeights  (5,'Weighted Particles', predict_particles, particle_weights, simpar);
    DrawParticles(6,'update',updated_belief_particles,ones(1,simpar.numberOfParticles), simpar);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%   COMPLETE THESE FUNCTIONS   %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% 1. Motion
function predict_particles = sample_motion_model(uk, priorbelief_particles, simpar)
%
% COMPLETE THIS FUNCTION
%
    % Tips:
    %   * Each particle has to evolve indenpently, so you could add some noise
    %   (possibly using 'simpar.odometry_stdev')
    %
    %   * Use mod() to handle circular halls (when simpar.circularHallway=1)
    %
    % change this value for the correct one
    N=simpar.numberOfParticles;
    noise=simpar.T^2/2*simpar.odometry_stdev*randn(1,N);
    
    predict_particles = priorbelief_particles + uk*simpar.T*ones(1,N) + noise;
    
    if simpar.circularHallway
        %circular hallway
        predict_particles = mod(predict_particles,simpar.domain);
    else
        % linear hallway
        A=predict_particles> simpar.domain; % all particules above the domain
        B=predict_particles<0; % all particules below 0
        
        %Update all necessary particles at once without using for loops
        predict_particles= A.*(simpar.domain-mod(predict_particles,simpar.domain)) + ...
                           B.*(-predict_particles) + ~A.*~B.*predict_particles;
        
    end
end

% 2. Measurement
function particle_weights = measurement_model(zk, predict_particles, simpar)
%
% COMPLETE THIS FUNCTION
%

    % wk = P( zk | xk )
   
    % ToDo: change this value for the correct one. Tip: it should be similar to
    % 'measurement_model_particles' except for the second 'pdf' argument (the
    % values at which to evaluate the pdf)
    
    particle_weights =  ...
          pdf('Normal', predict_particles, simpar.door_locations(1), simpar.door_stdev) + ...
          pdf('Normal', predict_particles, simpar.door_locations(2), simpar.door_stdev) + ...
          pdf('Normal', predict_particles, simpar.door_locations(3), simpar.door_stdev);
    
    % if z=0, you can just invert the weights. P( ~zk | xk ) =  1 - P( zk | xk )
    if zk==0 
        particle_weights= 1- particle_weights;
    end
    % normalization: simple (we could also use exponential weighting)
    particle_weights = particle_weights / sum(particle_weights);

end

% 3. Resampling
function updated_belief_particles = resampling(predict_particles, particle_weights, simpar)
%
% COMPLETE THIS FUNCTION
%
    r=rand(1);
    % Wheel resampling + allways add the best particule (elitism)
    % Important note!! It is not allowed to use randsample()
    
    N=simpar.numberOfParticles;
    
    updated_belief_particles=zeros(1,N);
    
    
    beta=0;
    ind= randi(N);
    for i=1:N-1
        beta=beta+rand(1)*2*max(particle_weights);
        while particle_weights(ind)<beta
            beta=beta-particle_weights(ind);
            ind= 1+mod(ind,N);
        end
        updated_belief_particles(i)=predict_particles(ind);
    end
    [~,k]=max(particle_weights);
    updated_belief_particles(N) = predict_particles(k);
end
