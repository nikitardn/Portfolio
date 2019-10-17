function L = gcDisparity(imgL, imgR, dispRange, box_size)

    imgL = im2single(imgL);
    imgR = im2single(imgR);

    Dc = diffsGC(imgL, imgR, dispRange, box_size);
    k=size(Dc,3);
    Sc = ones(k) - eye(k);

    % spatial variation cost. You may tune the size and sigma of filter to
    % improve performance
    [Hc, Vc] = gradient(imfilter(imgL,fspecial('gauss',[3 3]),'symmetric'));

    gch = GraphCut('open', 1000*Dc, 2*Sc, exp(-Vc*5), exp(-Hc*5));

    [gch, L] = GraphCut('expand',gch);
    gch = GraphCut('close', gch);
end