function [x,y,E] = tps_model(X,Y,lambda)

N=size(X,1);
t=dist2(X,X);
K = t.*log(t);
K(isnan(K))=0;
P=[ones(N,1), X];
A=[K+lambda*eye(N),     P;
    P',                 zeros(3,3)];

vx=Y(:,1);
vy=Y(:,2);

bx=[vx;0;0;0];
by=[vy;0;0;0];

x= A\bx;
y=A\by;

w_x=x(1:N);
w_y=y(1:N);
% a_x=x(N+1:N+3);
% a_y=y(N+1:N+3);

E=w_x'*K*w_x + w_y'*K*w_y;
end

