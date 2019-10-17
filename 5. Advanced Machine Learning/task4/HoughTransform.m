close all

V=VideoReader('task4/train/5.avi');
% Vid=read(V);
opticFlow = opticalFlowLK('NoiseThreshold',0.009);

while hasFrame(V)
    frameRGB = readFrame(V);
    frameGray = rgb2gray(frameRGB);
    mask=frameGray>3;%mean(mean(frameGray));
    I=mask*160 + (ones(size(mask))-mask)*0;
    E = edge(I,'canny');
    imshow(E);

    figure(2)
    [H,T,R] = hough(E);%,'Theta',-60:0.5:60);
    imshow(H,[],'XData',T,'YData',R,...
                'InitialMagnification','fit');
    xlabel('\theta'), ylabel('\rho');
    axis on, axis normal, hold on;

    P  = houghpeaks(H,5,'threshold',ceil(0.1*max(H(:))));
    x = T(P(:,2)); y = R(P(:,1));
    plot(x,y,'s','color','white');

    lines = houghlines(E,T,R,P,'FillGap',5,'MinLength',15);
    figure(3), imshow(I), hold on
    max_len = 0;

    for k = 1:length(lines)
       xy = [lines(k).point1; lines(k).point2];
       plot(xy(:,1),xy(:,2),'LineWidth',2,'Color','green');

       % Plot beginnings and ends of lines
       plot(xy(1,1),xy(1,2),'x','LineWidth',2,'Color','yellow');
       plot(xy(2,1),xy(2,2),'x','LineWidth',2,'Color','red');

       % Determine the endpoints of the longest line segment
       len = norm(lines(k).point1 - lines(k).point2);
       if ( len > max_len)
          max_len = len;
          xy_long = xy;
       end
    end
    pause(1);
end