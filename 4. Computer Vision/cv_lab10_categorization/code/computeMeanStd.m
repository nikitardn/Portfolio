function [mu sigma] = computeMeanStd(vBoW)
    mu=mean(vBoW,1);
    sigma=std(vBoW,0,1);
    sigma(sigma<0.5)=0.5;
end