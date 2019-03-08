function P = expectation(mu,cov,alpha,X)

K = length(alpha);
N = size(X,1);
P=zeros(N,K);
for i=1:K
    P(:,i)=mvnpdf(X,mu(i,:),cov(:,:,i));
end
P=P.*repmat(alpha',N,1)./repmat(sum(P*alpha,2),1,K);
end