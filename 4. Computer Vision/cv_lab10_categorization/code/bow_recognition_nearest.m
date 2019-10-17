function sLabel = bow_recognition_nearest(histogram,vBoWPos,vBoWNeg)
  
 % Find the nearest neighbor in the positive and negative sets
  % and decide based on this neighbor
  nPos=size(vBoWPos,1);
  nNeg=size(vBoWNeg,1);
  DistPos=min(sum((vBoWPos-repmat(histogram,nPos,1)).^2,2));
  DistNeg=min(sum((vBoWNeg-repmat(histogram,nNeg,1)).^2,2));
  
  if (DistPos<DistNeg)
    sLabel = 1;
  else
    sLabel = 0;
  end
  
end
