
res=[];
for k = [1 3 5 7]
    res=[res shape_classification(k)];
end

figure(8)
plot([1 3 5 7],res);
xlabel('k')
ylabel('accuracy')
legend('1 iteration', '6 iterations');
hold on