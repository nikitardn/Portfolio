function classificationAccuracy = shape_classification(k)

% perform the shape classification task

temp = load('dataset.mat');
objects = temp.objects;

nbObjects = length(objects);
nbSamples = 100;

%write the computeMatchingCosts.m function
matchingCostMatrix = compute_matching_costs(objects,nbSamples);

%be sure that the diagonal matrix matchingCostMatrix contains infinite energies
for o1 = 1:length(objects)
   matchingCostMatrix(o1,o1) = inf; 
end

allClasses = {objects(:).class};

hits = 0;
for o1 = 1:length(objects)        
    %nearest neighbour classification    
    %write the nn_classify.m function
    testClass = nn_classify(matchingCostMatrix(o1,:),allClasses,k);    
    if strcmpi(allClasses{o1},testClass)        
        hits = hits + 1;                
    end
end

fprintf('done\ntrue positives: %d/%d\n', hits, nbObjects);

classificationAccuracy = hits/nbObjects;
