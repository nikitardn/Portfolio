function X_nsamp = get_samples(X,nsamp)

    Ind_max=size(X,1);
    ind = randi(Ind_max,nsamp,1);
    
    X_nsamp=X(ind,:);
end