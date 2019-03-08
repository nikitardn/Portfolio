% extract descriptor
%
% Input:
%   keyPoints     - detected keypoints in a 2 x n matrix holding the key
%                   point coordinates
%   img           - the gray scale image
%   
% Output:
%   descr         - w x n matrix, stores for each keypoint a
%                   descriptor. m is the size of the image patch,
%                   represented as vector
function descr = extractDescriptor(corners, img)
    [~, nb]=size(corners);
    descr=zeros(nb,9*9);
    
    %slightly blur and pad the image
    img= imgaussfilt(img);
    img=padarray(img,[4 4],'replicate','both');
    
    %get a descriptor for each corner
    for n=1:nb
        j=corners(1,n)+4;
        i=corners(2,n)+4;
        descr(n,:)=reshape(img(i-4:i+4,j-4:j+4),1,9*9);
    end
end