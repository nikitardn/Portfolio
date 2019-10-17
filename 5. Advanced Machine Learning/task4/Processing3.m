
    n=158;
    features_train=[];
    folder='images_flow/train/';
    targets=csvread('task4/train_target.csv',1);
    Ys=targets(:,2);
    targets_new=[];
    N_sum=0;
    for i=1:n

        V=VideoReader(strcat('task4/train/',int2str(i-1),'.avi'));
        N=uint32(V.Duration*V.Framerate);
        N_sum=N_sum+N;
        F=get_flow(V,folder,N,i);
        targets_new=[targets_new; [(i-1) Ys(i)].*ones(N,2)];
        
        features_train=[features_train;F];
%         I=mat2gray(F);
%         imwrite(I,strcat('images_flow/train/',int2str(i),'.png'))
        
        disp(i/2/n);
        if size(F,1)~=N
            a=1
        end
    end
   csvwrite('features_train_flow_all2.csv',features_train)
%  csvwrite('targets_all_flow.csv',targets_new)

    n=69;
    features_test=[];
    folder='images_flow/test/';
    ids_new=[];
    features_test=[];
    for i=1:n

        V=VideoReader(strcat('task4/test/',int2str(i-1),'.avi'));
        N=uint8(V.Duration*V.Framerate);
        F=get_flow(V,folder,N,i);
        ids_new=[ids_new; (i-1)*ones(N,1)];
            
        features_test=[features_test;F];
%         I=mat2gray(get_flow(V));
%         imwrite(I,strcat('images_flow/test/',int2str(i),'.png'))
        disp(0.5+i/2/n);
    end
    csvwrite('features_test_flow_all2.csv',features_test)  
%  csvwrite('ids_all_flow.csv',ids_new)