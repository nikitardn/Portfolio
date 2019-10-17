function [e1, e2] = getEpipoles(F)
%UNTITLED computes the epipoles from F

    [U,S,V] = svd(F);
    e1=V(:,end);
    e2=U(:,end);
    
    e1=e1/e1(3);
    e2=e2/e2(3);
end

