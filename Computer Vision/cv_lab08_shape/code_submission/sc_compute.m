function ShapeDescriptors = sc_compute(X,nbBins_theta,nbBins_r,smallest_r,biggest_r)
N=size(X,2);

mean_dist=mean2(sqrt(dist2(X',X')));

maxr=log(biggest_r);
minr=log(smallest_r);
dr=(maxr-minr)/nbBins_r;
bins_r=linspace(minr,maxr-dr,nbBins_r)';

dtheta=2*pi/nbBins_theta;
bins_theta=linspace(0,2*pi-dtheta,nbBins_theta)';

edges={bins_theta,bins_r};

ShapeDescriptors=zeros(N,nbBins_theta,nbBins_r);
for i=1:N
    vec=X-repmat(X(:,i),1,N);
    vec(:,i)=[];
    [theta,r] = cart2pol(vec(1,:),vec(2,:));
    logr=log(r/mean_dist);
    ShapeDescriptors(i,:,:)=hist3([theta', logr'],'Edges',edges);
end
end

