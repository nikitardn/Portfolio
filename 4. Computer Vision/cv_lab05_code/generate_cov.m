% Generate initial values for the K
% covariance matrices

function cov = generate_cov(Lmax,Lmin,amax,amin,bmax,bmin,K);

    cov = [Lmax-Lmin 0 0;
           0 amax-amin 0;
           0 0 bmax-bmin];

    cov=repmat(cov,1,1,K);   

end