function meanState = estimate(particles,particles_w)
    
    M=size(particles,2);
    meanState=sum(particles.*repmat(particles_w,1,M),1);
end