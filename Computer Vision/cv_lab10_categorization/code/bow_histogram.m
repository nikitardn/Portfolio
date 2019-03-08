function histo = bow_histogram(vFeatures, vCenters)
  % input:
  %   vFeatures: MxD matrix containing M feature vectors of dim. D
  %   vCenters : NxD matrix containing N cluster centers of dim. D
  % output:
  %   histo    : N-dim. vector containing the resulting BoW
  %              activation histogram.
  
  
  % Match all features to the codebook and record the activated
  % codebook entries in the activation histogram "histo".
  nFeatures=size(vFeatures,1);
 nCenters=size(vCenters,1);
 histo=zeros(nCenters,1);
 for i=1:nFeatures
     dist=sum((vCenters-repmat(vFeatures(i,:),nCenters,1)).^2,2);
    [~,ind]=min(dist);
    histo(ind)=histo(ind)+1;
end
