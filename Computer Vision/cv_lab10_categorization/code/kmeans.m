function vCenters = kmeans(vFeatures,k,numiter)

  nPoints  = size(vFeatures,1);
  nDims    = size(vFeatures,2);
  vCenters = zeros(k,nDims);
   
  
  % Initialize each cluster center to a different random point.

  vCenters=vFeatures(randperm(nPoints,k),:);
  % Repeat for numiter iterations
  for i=1:numiter
      
    % Shift each cluster center to the mean of its assigned points
    [Idx, ~] = findnn( vFeatures, vCenters );
    for c=1:k
        vCenters(c,:)=mean(vFeatures(Idx==c,:),1);
    end
    disp(strcat(num2str(i),'/',num2str(numiter),' iterations completed.'));
  end
 
 
end
