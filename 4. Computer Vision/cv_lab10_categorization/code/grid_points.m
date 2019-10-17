function vPoints = grid_points(img,nPointsX,nPointsY,border)
    [n, m]=size(img);
    points_x=linspace(1+border,m-border,nPointsX)';
    points_y=linspace(1+border,n-border,nPointsY)';

   [A,B]=meshgrid(points_x,points_y);
    c=[A,B];
    vPoints=int32(reshape(c,[],2));
    
end
