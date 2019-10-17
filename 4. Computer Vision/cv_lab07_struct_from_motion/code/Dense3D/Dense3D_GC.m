function [dispsGCL, dispsGCR, maskGCL, maskGCR] = Dense3D_GC(img1,img2,x1s,x2s,F)

constants;

[imgRectL, imgRectR, Hleft, Hright, maskL, maskR] = rectifyImages(img1, img2, [x1s', x2s'], F);
figure(1)
imshow(imgRectL);
figure(2)
imshow(imgRectR);

Labels = gcDisparity(imgRectL, imgRectR, dispRange, box_size);
dispsGCL = double(Labels + dispRange(1));
Labels = gcDisparity(imgRectR, imgRectL, dispRange, box_size);
dispsGCR = double(Labels + dispRange(1));

figure(3);
imshow(dispsGCL, [dispRange(1) dispRange(end)]);
figure(2);

 subplot(121); imshow(dispsGCL, [dispRange(1) dispRange(end)]);
 title(strcat('window size : ',int2str(box_size),'x',int2str(box_size)));
 subplot(122); imshow(dispsGCR, [dispRange(1) dispRange(end)]);
 
%saveas(gcf,strcat(folder,'GC_box=',int2str(box_size),'.png'));

maskLRcheck = leftRightCheck(dispsGCL, dispsGCR, thresh);
maskRLcheck = leftRightCheck(dispsGCR, dispsGCL, thresh);

maskGCL = double(maskL).*maskLRcheck;
maskGCR = double(maskR).*maskRLcheck;

figure(4);
subplot(121); imshow(maskGCL);
subplot(122); imshow(maskGCR);
imshow(maskGCL);
end


