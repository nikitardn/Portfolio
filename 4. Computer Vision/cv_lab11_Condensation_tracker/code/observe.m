function particles_w = observe(particles,frame,H,W,nBins,hist_target,sigma_observe)
    nParticles= size(particles,1);
    particles_w=zeros(nParticles,1);
    for i=1:nParticles
        xMin=particles(i,1)-W/2;
        xMax=particles(i,1)+W/2;
        yMin=particles(i,2)-H/2;
        yMax=particles(i,2)+H/2;
        
        particle_hist=color_histogram(xMin,yMin,xMax,yMax,frame,nBins);
                
        cost=chi2_cost(particle_hist,hist_target);
        particles_w(i)= 1/sqrt(2*pi)/sigma_observe*exp(-cost^2/2/sigma_observe^2);
    end
    particles_w=particles_w/sum(particles_w);
end

