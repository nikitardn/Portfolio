function particles = propagate(particles,sizeFrame,params)

if (params.model==0 ) %zero velocity
    
    A=[1 0;
       0 1];
   particles=particles*A' + randn(size(particles))*params.sigma_position;
else
    dt=1;
    A=[1 0 dt 0;
       0 1 0 dt;
       0 0 1 0;
       0 0 0 1];
   particles=particles*A' + randn(size(particles))*diag([0; 0;
                                                    params.sigma_velocity;
                                                    params.sigma_velocity]);
end


out1=particles(:,1)<1;
out2=particles(:,2)<1;
out3=particles(:,1) > sizeFrame(2);
out4=particles(:,2)>sizeFrame(1);
particles(out1,1)=1;
particles(out2,2)=1;
particles(out3,1)=sizeFrame(2);
particles(out4,2)=sizeFrame(1);
end

