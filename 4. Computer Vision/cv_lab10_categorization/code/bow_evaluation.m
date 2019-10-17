%
% BAG OF WORDS RECOGNITION EXERCISE
%

acc_nn=zeros(1,1);
acc_bay=zeros(1,1);
nAverage=1;
nDiff_k=1;
for i=1:nAverage
    for j=1:nDiff_k
%         sizeCodebook=j*50;
         sizeCodebook= 200;
%training
disp('creating codebook');

numIterations = 10;
vCenters = create_codebook('../data/cars-training-pos',sizeCodebook,numIterations);
%keyboard;
disp('processing positve training images');
vBoWPos = create_bow_histograms('../data/cars-training-pos',vCenters);
disp('processing ne gative training images');
vBoWNeg = create_bow_histograms('../data/cars-training-neg',vCenters);
%vBoWPos_test = vBoWPos;
%vBoWNeg_test = vBoWNeg;
%keyboard;
disp('processing positve testing images');
vBoWPos_test = create_bow_histograms('../data/cars-testing-pos',vCenters);
disp('processing negative testing images');
vBoWNeg_test = create_bow_histograms('../data/cars-testing-neg',vCenters);

nrPos = size(vBoWPos_test,1);
nrNeg = size(vBoWNeg_test,1);

test_histograms = [vBoWPos_test;vBoWNeg_test];
labels = [ones(nrPos,1);zeros(nrNeg,1)];

disp('______________________________________')
disp('Nearest Neighbor classifier')
acc_nn(i,j)=bow_recognition_multi(test_histograms, labels, vBoWPos, vBoWNeg, @bow_recognition_nearest);
disp('______________________________________')
disp('Bayesian classifier')
acc_bay(i,j)=bow_recognition_multi(test_histograms, labels, vBoWPos, vBoWNeg, @bow_recognition_bayes);
disp('______________________________________')
    end
end