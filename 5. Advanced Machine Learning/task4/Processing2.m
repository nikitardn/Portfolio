
    n=158;
    for i=1:n

        V=VideoReader(strcat('task4/train/',int2str(i-1),'.avi'));
        I = VarianceVideo(V);
        imwrite(I,strcat('images_var/train/',int2str(i),'.png'))
        disp(i/2/n);
    end


    n=69;
    A=NaN(n,250);
    for i=1:n

        V=VideoReader(strcat('task4/test/',int2str(i-1),'.avi'));
        I = VarianceVideo(V);
        imwrite(I,strcat('images_var/test/',int2str(i),'.png'))
        disp(0.5+i/2/n);
    end
