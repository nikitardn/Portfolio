
    n=158;
    A=NaN(n,250);
    for i=1:n

        V=VideoReader(strcat('task4/train/',int2str(i-1),'.avi'));
        Ai = getAreaTimeSeries(V);
        m=length(Ai);
        A(i,1:m)=Ai;
        disp(i/n);
    end

     csvwrite('Area_timeseries_train.csv',A)

        n=69;
    A=NaN(n,250);
    for i=1:n

        V=VideoReader(strcat('task4/test/',int2str(i-1),'.avi'));
        Ai = getAreaTimeSeries(V);
        m=length(Ai);
        A(i,1:m)=Ai;
        disp(i/n);
    end

     csvwrite('Area_timeseries_test.csv',A)