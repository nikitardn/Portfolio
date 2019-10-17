function C = compute_matching_costs(objects,nsamp)

N=size(objects,2);
C=-ones(N);

for i=1:N
    for j=1:N
        if i==j
            C(i,j)=inf;
            continue;
        end
        X1=objects(i).X;
        X2=objects(j).X;

        
        X1=get_samples_1(X1,nsamp);
        X2=get_samples_1(X2,nsamp);
        C(i,j)=shape_matching(X1,X2,0);
    end
     disp(i);
end
end