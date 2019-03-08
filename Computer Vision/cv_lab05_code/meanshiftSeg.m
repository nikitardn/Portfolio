function [map, peaks] = meanshiftSeg(img)

    [m, n, o]=size(img);
    N=m*n;
    points=double(reshape(img,N,o));
    
    tol=0.1;
    r=20;
    map=zeros(N,1);
    Centers=[];
    next_ind=1;
    for i=1:N
       center=find_peak( points, points(i,:), r, tol );
        
       %find closest value in previous centers
       if isempty(Centers)
           map(i)=next_ind;
           Centers=[Centers;center];
           next_ind=next_ind+1;
           continue;
       end
       %check if the peak can be matched with a previous one
       Npeaks=size(Centers,1);
       [~, ind] = min(sqrt(sum((repmat(center,Npeaks,1) - Centers).^2,2)));
       c=Centers(ind,:);
       if norm(c-center)< r/2
           map(i)=ind;
       else
           Centers=[Centers; center];
           map(i)=next_ind;
           next_ind=next_ind+1;
       end
       
    end
    plot3(Centers(:,1),Centers(:,2),Centers(:,3),'.');
    map=reshape(map,m,n);
    peaks=Centers;
end