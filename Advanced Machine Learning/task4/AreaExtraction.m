
V=VideoReader('task4/train/5.avi');
Vid=read(V);

T=size(Vid,4);
A=zeros(T,1);
for i=1:T
%     imshow(Vid(:,:,:,1))
    I=rgb2gray(Vid(:,:,:,i));
    mask=I<mean(mean(I));
    A(i)=size(find(mask),1);
    
%     I(mask)=160*ones(size(find(mask),1),1);
end
figure
plot(diff(A)./max(A));