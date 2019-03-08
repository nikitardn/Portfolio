function mean_frame = mean_image(V)

    j=1;
    sum_frame=zeros(100);
    while hasFrame(V)

        frameRGB = readFrame(V);
        frameGray = rgb2gray(frameRGB);
        mask=frameGray>mean(mean(frameGray));
        I=mask*160;

        sum_frame=sum_frame+I;
    %     imshow(uint8(sum_frame/j),'InitialMagnification','fit');
        j=j+1;

    end
    mean_frame=uint8(sum_frame/j);
end
