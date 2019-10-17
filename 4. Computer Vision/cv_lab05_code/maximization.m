function [mu, cov, alpha] = maximization(P, X)

K = size(P,2);
N = size(X,1);

mu=zeros(K,3);
cov=zeros(3,3,K);

sumP=sum(P,1);
alpha=1/N*sumP';

for i=1:K
    mu(i,:)=sum(P(:,i)'*X,1)/sumP(i);
    
    Di=X-repmat(mu(i,:),N,1);
    cov(:,:,i)=Di'*(repmat(P(:,i),1,3).*Di)/sumP(i);
end
end