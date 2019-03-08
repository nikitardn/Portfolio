% Generate initial values for mu
% K is the number of segments

function mu = generate_mu(Lmax,Lmin,amax,amin,bmax,bmin,K)

mu = [linspace(Lmin,Lmax,K)' linspace(amin,amax,K)' linspace(bmin,bmax,K)'];

end