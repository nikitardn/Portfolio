function f = fminGoldStandard(p, xy, XYZ, w)

%reassemble P
P = [p(1:4);p(5:8);p(9:12)];

%compute squared geometric error
xy_hat=P*XYZ;
W=xy_hat(3,:);
xy_hat=xy_hat./[W;W;W];

f=sum(vecnorm(xy-xy_hat));
%compute cost function value
end