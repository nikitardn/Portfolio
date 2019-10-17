function Dc = diffsGC(img1, img2, dispRange,box_size)

% dispRange: range of possible disparity values
% --> not all values need to be checked
img1=double(img1);
img2=double(img2);


sz=size(img1);
Cost=zeros(sz(1),sz(2),size(dispRange,2));
for d=dispRange
    img2_shift=shiftImage(img2,d);
    SSD = (img1-img2_shift).^2;
    
    box_filter=fspecial('average',box_size);
    c=conv2(SSD,box_filter,'same');

    Cost(:,:,d-min(dispRange)+1)=c;
end

Dc=Cost;
end