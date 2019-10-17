load('acc_bay.mat')
load('acc_nn.mat')
mean_nn=mean(acc_nn,1);
mean_bay=mean(acc_bay,1);
figure(1)
K=[ones(5,1)*50,ones(5,1)*100,ones(5,1)*150,ones(5,1)*200];
plot([50 100 150 200],mean_bay,'b');hold on
plot([50 100 150 200],mean_nn,'r');
plot(K,acc_bay,'bx');
plot(K,acc_nn,'rx');
xlabel('k')
ylabel('accuracy')
legend('Bayesian','Nearest neighbour');
