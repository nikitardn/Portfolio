function hist = color_histogram(xMin,yMin,xMax,yMax,frame,nBins)
    
    [Y,X]=size(frame);
%     IxMax=X-xMin;
%     IxMin=X-xMax;
%     IyMax=Y-yMin;
%     IyMin=Y-yMax;
    
    
    
    xMin=max(1,round(xMin));
    xMax=min(size(frame,2),round(xMax));
    yMin=max(1,round(yMin));
    yMax=min(size(frame,1),round(yMax));
    
    box_R=frame(yMin:yMax,xMin:xMax,1);
    box_G=frame(yMin:yMax,xMin:xMax,2);
    box_B=frame(yMin:yMax,xMin:xMax,3);
    
    nPixels=(xMax-xMin+1)*(yMax-yMin+1);
    edges=linspace(0,255,nBins+1);
    hist_R=histcounts(box_R,edges)/nPixels;
    hist_G=histcounts(box_G,edges)/nPixels;
    hist_B=histcounts(box_B,edges)/nPixels;
    
    hist=[hist_R, hist_G, hist_B];
end

