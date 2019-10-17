function label = bow_recognition_bayes( histogram, vBoWPos, vBoWNeg)

P_Car=0.5;
P_notCar=0.5;

[muPos sigmaPos] = computeMeanStd(vBoWPos);
[muNeg sigmaNeg] = computeMeanStd(vBoWNeg);

% Calculating the probability of appearance each word in observed histogram
% according to normal distribution in each of the positive and negative bag of words
log_pos=sum(log(normpdf(histogram,muPos,sigmaPos)));
log_neg=sum(log(normpdf(histogram,muNeg,sigmaNeg)));

if log_pos*P_Car>log_neg*P_notCar
    label=1;
else
    label=0;
end