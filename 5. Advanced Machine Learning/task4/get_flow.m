function [Flow_mag] = get_flow(V,folder,N,i)

Flow=zeros(50,50,2,N);
opticFlow = opticalFlowLK('NoiseThreshold',0.009);
Flow_mag=zeros(N,2500);
for j=1:N
    frameRGB = readFrame(V);
    frameGray = rgb2gray(frameRGB);
    
    flow = estimateFlow(opticFlow,frameGray); 
%     Flow(:,:,1,j)=flow.Orientation;
    flow_mag=imresize(flow.Magnitude,0.5);
%     Flow(:,:,2,j)=flow_mag;
%     flow_im=mat2gray(flow.Magnitude);
%     imwrite(flow_im,strcat(folder,int2str(i),'_',int2str(j),'.png'));
    Flow_mag(j,:)=reshape(flow_mag,1,2500);
end

% mean_Flow=mean(Flow,4);
% min_Flow=min(Flow,[],4);
% max_Flow=max(Flow,[],4);
% var_Flow=var(Flow,0,4);
% 
% var_Flow_mag=var_Flow(:,:,2);
end