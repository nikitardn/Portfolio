% Decompose the essential matrix
% Return P = [R|t] which relates the two views
% You will need the point correspondences to find the correct solution for P
function P = decomposeE(E, x1, x2)
    [U,S,V] = svd(E);
    W=[0 -1 0;
       1 0 0;
       0 0 1];
   
    R1=U*W*V';
    R2=U*W'*V';
    R1=R1*sign(det(R1));
    R2=R2*sign(det(R2));
    t1=U(:,3);
    t1=t1/norm(t1);
    t2=-t1;
    
    P1=[eye(3) zeros(3,1)];
    
    P2=[R1 t1];
    [X, ~] = linearTriangulation(P1, x1, P2, x2);
    X2=P2*X;
    z1=min(X(3,:));
    z2=min(X2(3,:));
    if z1>0 && z2>0
        P=P2;
        return
    end
    
    P2=[R2 t1];
    [X, ~] = linearTriangulation(P1, x1, P2, x2);
    X2=P2*X;
    z1=min(X(3,:));
    z2=min(X2(3,:));
    if z1>0 && z2>0
        P=P2;
        return
    end
    
    P2=[R1 t2];
    [X, ~] = linearTriangulation(P1, x1, P2, x2);
    X2=P2*X;
    z1=min(X(3,:));
    z2=min(X2(3,:));
    if z1>0 && z2>0
        P=P2;
        return
    end
    
    P2=[R2 t2];
    [X, ~] = linearTriangulation(P1, x1, P2, x2);
    X2=P2*X;
    z1=min(X(3,:));
    z2=min(X2(3,:));
    if z1>0 && z2>0
        P=P2;
        return
    else
        print('no P found');
    end
end