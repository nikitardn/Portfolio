clear all 
close all
clc

%% Setup

imds=imageDatastore('images_flow/train');

%Label imdsTrain
train_target=csvread('task4/targets_all_flow.csv',0);
labels=categorical(train_target(:,2));
imds.Labels=labels;

%tbl = countEachLabel(imdsTrain);
img = readimage(imds,1);
shape=size(img);

%Create imageDatastore for Test data, with empty labels
%imdsValidation=imageDatastore('test');



% minibatch = preview(auimds);
% imshow(imtile(minibatch.input));
% 
% minibatch = preview(auimds);
% imshow(imtile(minibatch.input(1)));


numTrainFiles = 3000;
[imdsTrain,imdsValidation] = splitEachLabel(imds,numTrainFiles);

augmenter = imageDataAugmenter( ...
    'RandRotation',[-10 10],...
    'RandXTranslation',[-10 10]...
    ,'RandYTranslation',[-10 10]...
    ,'RandXScale', [0.7 1.3]...
    ,'RandYScale', [0.7 1.3]...
    );

imageSize = [shape, 1];
auimdsTrain = augmentedImageDatastore(shape,imdsTrain,'DataAugmentation',augmenter);

layers = [
    imageInputLayer([shape, 1],'Normalization','zerocenter')
    
    convolution2dLayer(3,16,'Padding','same')
     batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,32,'Padding','same')
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,64,'Padding','same')
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)
    
    
    dropoutLayer(0.5)
    fullyConnectedLayer(64)
    softmaxLayer
   
%     dropoutLayer(0.5)
    fullyConnectedLayer(2)
    softmaxLayer
    classificationLayer];

options = trainingOptions('sgdm', ...
    'InitialLearnRate',0.01, ...
    'MaxEpochs',50, ...
    'Shuffle','every-epoch', ...
    'ValidationData',imdsValidation, ...
    'ValidationFrequency',10,...
    'Verbose',false, ...
    'MiniBatchSize',128,...
    'Plots','training-progress',...
    'ValidationPatience',Inf);

net = trainNetwork(imdsTrain,layers,options);

YPred = classify(net,imdsValidation);
YValidation = imdsValidation.Labels;

accuracy = sum(YPred == YValidation)/numel(YValidation);