function [Idx Dist] = findnn( D1, D2 )
  % input:
  %   D1  : NxD matrix containing N feature vectors of dim. D
  %   D2  : MxD matrix containing M feature vectors of dim. D
  % output:
  %   Idx : N-dim. vector containing for each feature vector in D1
  %         the index of the closest feature vector in D2.
  %   Dist: N-dim. vector containing for each feature vector in D1
  %         the distance to the closest feature vector in D2.

  N = size(D1,1);
  M = size(D2,1);
  Idx  = zeros(N,1);
  Dist = zeros(N,1);
  
  % Find for each feature vector in D1 the nearest neighbor in D2
  for n=1:N
      dist_all=sqrt(sum((repmat(D1(n,:),M,1)-D2).^2,2));
      [min_dist,ind] = min(dist_all);
      Dist(n)=min_dist;
      Idx(n)=ind;
  end
end
      