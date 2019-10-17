function [map cluster] = EM(img,K)

    tol= 1e-6;
    [m, n, o]=size(img);
    N=m*n;
    points=double(reshape(img,N,o));
    
    Lmax=max(points(:,1)); Lmin=min(points(:,1));
    amax=max(points(:,2)); amin=min(points(:,2));
    bmax=max(points(:,3)); bmin=min(points(:,3));
    
    % initialize mus
    mu=generate_mu(Lmax,Lmin,amax,amin,bmax,bmin,K);
    %initialize covariances
    cov=generate_cov(Lmax,Lmin,amax,amin,bmax,bmin,K);
    alpha=1/K*ones(K,1);
    
    % iterate between maximization and expectation
    theta={alpha, mu, cov};
    step=tol+1;
    P=zeros(N,K);
    while step>tol
        muold=mu;
        P = expectation(mu,cov,alpha,points);
        [mu, cov, alpha] = maximization(P, points);
        step=norm(muold-mu);
    end
    [~,map]= max(P,[],2);
    cluster=mu;
    
    digits(5);
    map=reshape(map,m,n);
 
% Use this to save matrices to Latex (requieres special package)

% for i=1:K
% matrix2latexmatrix(mu(i,:)',strcat('latex/matrices/mu_K',int2str(K),'_',int2str(i),'.tex'));
% matrix2latexmatrix(cov(:,:,i),strcat('latex/matrices/cov_K',int2str(K),'_',int2str(i),'.tex'));
% end
% matrix2latexmatrix(alpha,strcat('latex/matrices/alpha_K',int2str(K),'.tex'));
end