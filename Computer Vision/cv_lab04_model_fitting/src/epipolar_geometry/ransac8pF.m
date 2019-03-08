function [in1, in2, out1, out2, m, F_final] = ransac8pF(x1, x2, threshold)

r=0;
N=8;
p=0;
maxiter=100000;
nb_tot=length(x1);
max_inliers=0;
M=0;

while( M<maxiter && p<0.99)
    inliers_ind=zeros(nb_tot,1);
    
    ind=randperm(nb_tot,8);
    x1_sel=x1(:,ind);
    x2_sel=x2(:,ind);
    
    [Fh, F] = fundamentalMatrix(x1_sel, x2_sel);
    
    nb_inliers=0;
    for i=1:nb_tot
        d=distPointLine(x2(:,i),F*x1(:,i)) +...
        distPointLine(x1(:,i),F'*x2(:,i));
        if d<threshold
            nb_inliers=nb_inliers+1;
            inliers_ind(i)=1;
        end
    end
    
    if nb_inliers>max_inliers
        max_inliers=nb_inliers;
        best_inliers_ind=inliers_ind;
    end
    M=M+1;
    r=max_inliers/nb_tot;
    p=1-(1-r^N)^M
end

    in1=x1(:,best_inliers_ind==1);
    in2=x2(:,best_inliers_ind==1);
    out1=x1(:,best_inliers_ind==0);
    out2=x2(:,best_inliers_ind==0);
    [Fh, ~] = fundamentalMatrix(in1, in2);
    F_final=Fh;
    m=M
    
end


