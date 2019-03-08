function [descriptors,patches] = descriptors_hog(img,vPoints,cellWidth,cellHeight)

    nBins = 8;
    w = cellWidth; % set cell dimensions
    h = cellHeight;   
    nPoints=size(vPoints,1);
    descriptors = zeros(nPoints,nBins*4*4); % one histogram for each of the 16 cells
    patches = zeros(nPoints,4*w*4*h); % image patches stored in rows    
    
    [grad_x,grad_y]=gradient(img);
    grad=sqrt(grad_x.^2 + grad_y.^2);
    grad_orient=atan(grad_y./grad_x);

    bin_edges=linspace(-pi/2,pi/2,nBins+1);
    for i = 1:nPoints % for all local feature points
        descr_i=zeros(1,nBins*4*4);
        m=1;
        for k=-2:1
            for l=-2:1
                startx=vPoints(i,1)+w*k;
                starty=vPoints(i,2)+h*l;
                patch=grad_orient(starty:starty+h,startx:startx+w);
                descr_i_kl=histcounts(reshape(patch,1,[]),bin_edges);
                descr_i(m:m+nBins-1)=descr_i_kl;
                m=m+8;
            end
        end
        descriptors(i,:)=descr_i;
        patch_img=img(vPoints(i,2)-2*h:vPoints(i,2)+2*h-1,vPoints(i,1)-2*w:vPoints(i,1)+2*w-1);
        patches(i,:)=reshape(patch_img,1,[]);
    end % for all local feature points
    
end
