function disp = stereoDisparity(img1, img2, dispRange,box)

% dispRange: range of possible disparity values
% --> not all values need to be checked
img1=double(img1);
img2=double(img2);
box_size=box;
disp=zeros(size(img1));
first=1;
for d=dispRange
    img2_shift=shiftImage(img2,d);
    SSD = (img1-img2_shift).^2;
    
    box_filter=fspecial('average',box_size);
    Cost=conv2(SSD,box_filter,'same');
    if first
        Cost_best=Cost;
        first=0;
    end
    mask= Cost<Cost_best;
    Cost_best(mask)=Cost(mask);
    disp(mask)=d*mask(mask);
end
end