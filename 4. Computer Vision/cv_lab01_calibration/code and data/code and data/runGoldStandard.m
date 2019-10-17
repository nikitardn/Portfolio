function [K, R, t, error] = runGoldStandard(xy, XYZ,savename)

%normalize data points
N=length(xy);
xyh=[xy; ones(1,N)];
XYZh=[XYZ; ones(1,N)];
[xyn, XYZn, T, U] = normalization(xyh, XYZh);

%compute DLT
[Pn] = dlt(xyn, XYZn);

%minimize geometric error
pn = [Pn(1,:) Pn(2,:) Pn(3,:)];
for i=1:1
    [pn] = fminsearch(@fminGoldStandard, pn, [], xyn, XYZn, i/5);
end
P_normalized=[pn(1:4);pn(5:8);pn(9:12)];
%denormalize camera matrix
P=T\P_normalized*U;

%factorize camera matrix in to K, R and t
M=P(1:3,1:3);

[Rinv,Kinv]=qr(inv(M));
K=inv(Kinv);
K=K/K(3,3);
R=inv(Rinv);
C= -Rinv*Kinv*P(:,4);
t=-R*C;
% [U,S,V] = svd(P);
% C2=V(:,end);
% C2=C2/C2(end);
    
%compute reprojection error
nbx=6;
nby=8;
nbz=9;
x_proj=[0:1:nbx-1];
y_proj=[0:1:nby-1];
z_proj=[0:1:nbz-1];
[x zx]=meshgrid(x_proj,z_proj);
[y zy]=meshgrid(y_proj,z_proj);

XYZ_proj=[x(:) zeros(nbx*nbz,1) zx(:) ones(nbx*nbz,1); zeros(nby*nbz,1) y(:) zy(:) ones(nby*nbz,1)]';
XYZ_proj(1:3,:)=XYZ_proj(1:3,:)*27/1000;
xy_hat=P*XYZ_proj;
xy_hat1=P*XYZh;
W=xy_hat(3,:);
xy_hat=xy_hat./[W;W;W];
W=xy_hat1(3,:);
xy_hat1=xy_hat1./[W;W;W];
error=sum(vecnorm(xyh-xy_hat1))/N;
displayPoints(xyh,xy_hat,savename);
end
