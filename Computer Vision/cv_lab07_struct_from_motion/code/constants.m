%K Matrix for house images (approx.)
K = [  670.0000     0     393.000
         0       670.0000 275.000
         0          0        1];

%Load images
imgName1 = '../data/house.000.pgm';
imgName2 = '../data/house.004.pgm';
imgName3 = '../data/house.001.pgm';
imgName4 = '../data/house.002.pgm';
imgName5 = '../data/house.003.pgm';

SIFT_tresh=0.1;
F_tresh=0.0001;
P_tresh=0.1;
dispRange= -100:100;
box_size=30;
thresh=8;