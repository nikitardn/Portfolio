function Chi = chi2_cost(Descr1,Descr2)

N1=size(Descr1,1);
N2=size(Descr2,1);

Chi=zeros(N1,N2);

for i=1:N1
    pi=Descr1(i,:);
    for j=1:N2
        pj=Descr2(j,:);
        c=(pi-pj).^2./(pi+pj);
        c(isnan(c))=0;
        Chi(i,j)=0.5*sum(c);
    end
end

    
end

