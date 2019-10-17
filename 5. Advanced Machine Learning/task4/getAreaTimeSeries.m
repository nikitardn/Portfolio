function [A] = getAreaTimeSeries(V)
T=size(V,4);
A=-ones(T,1);
j=1;
while hasFrame(V)
    frameRGB = readFrame(V);
    frameGray = rgb2gray(frameRGB);
    mask=frameGray>mean(mean(frameGray));
    I=mask*160 + (ones(size(mask))-mask)*0;
    E = edge(I,'canny');
    [y,x,~]= find(E==1);
    K = convhull(x,y);
    
    Points=[];
    for i=1:100
        black_ys=find(mask(:,i)==0);
        N=length(black_ys);
        p=[i*ones(N,1) black_ys];
        Points=[Points;p];
    end
    Inliers=inhull(Points,[x(K),y(K)],[],-2);
    Points=Points(Inliers,:);
    ImPoints=zeros(100,100);
    
    for k=1:size(Points,1)
        ImPoints(Points(k,2),Points(k,1))=1;
    end

    [IDX, C] = kmeans(Points, 4);
    M=C(:,1)-C(:,2);
    [~,m]=max(M);
    p1=Points(IDX==m,:);
    c=C(m,:);
    Ventricule = bwselect(ImPoints,c(1),c(2),4);

    A(j)=size(find(Ventricule),1);
    j=j+1;
end
end

