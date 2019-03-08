function [coords, mask,dispStereoL] = Dense3D(img1,img2,x1s,x2s,PL)

constants;
[F, ~] = ransacfitfundmatrix(x1s, x2s, F_tresh);
[imgRectL, imgRectR, Hleft, Hright, maskL, maskR] = rectifyImages(img1, img2, [x1s', x2s'], F);

imwrite(imgRectL,'imgRectL.png');


dispStereoL = stereoDisparity(imgRectL, imgRectR, dispRange, box_size);
dispStereoR = stereoDisparity(imgRectR, imgRectL, dispRange, box_size);

figure(1);

subplot(121); imshow(dispStereoL, [dispRange(1) dispRange(end)]);
title(strcat('window size : ',int2str(box_size),'x',int2str(box_size)));
subplot(122); imshow(dispStereoR, [dispRange(1) dispRange(end)]);

%saveas(gcf,strcat(folder,'disp_box=',int2str(box_size),'.png'));


maskLRcheck = leftRightCheck(dispStereoL, dispStereoR, thresh);
maskRLcheck = leftRightCheck(dispStereoR, dispStereoL, thresh);

maskStereoL = double(maskL).*maskLRcheck;
maskStereoR = double(maskR).*maskRLcheck;

figure(2);

subplot(121); imshow(maskStereoL);
subplot(122); imshow(maskStereoR);

dispStereoL = double(dispStereoL);
dispStereoR = double(dispStereoR);

PR=[eye(3,3) zeros(3,1); 0 0 0 1];
coords = generatePointCloudFromDisps(dispStereoR,PR,PL);
mask=maskStereoL.*maskStereoR;
end

