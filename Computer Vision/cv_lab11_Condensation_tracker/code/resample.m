function [updated_particles, updated_particles_w] = resample(particles,particles_w)
    %whell resampling + allways keep the best particle
    [N,M]=size(particles);
    updated_particles=zeros(N,M);
    updated_particles_w=zeros(N,1);
    
    beta=0;
    ind= randi(N);
    for i=1:N-1
        beta=beta+rand(1)*2*max(particles_w);
        while particles_w(ind)<beta
            beta=beta-particles_w(ind);
            ind= 1+mod(ind,N);
        end
        updated_particles(i,:)=particles(ind,:);
        updated_particles_w(i)=particles_w(ind);
    end
    [~,k]=max(particles_w);
    updated_particles(N,:) = particles(k,:);
    updated_particles_w(N) = particles_w(k);
    updated_particles_w=updated_particles_w/sum(updated_particles_w);
end

