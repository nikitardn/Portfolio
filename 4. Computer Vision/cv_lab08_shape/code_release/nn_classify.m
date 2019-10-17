function testClass = nn_classify(Cvec,trainClasses,k)
    
    [min_vals, min_ids] = sort(Cvec, 'ascend');
%     max_vals = max_vals(1:k);
    min_ids = min_ids(1:k);
    
    score=zeros(15,1);
    for i=1:k
        correct=find(strcmp(trainClasses,trainClasses{min_ids(i)}));
        score(correct)=score(correct)+1;
    end
    [~, result]=max(score);
    testClass=trainClasses{result};
end