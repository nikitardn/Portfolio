% Intrinsic and Extrinsic Camera Parameters
%
% This script file can be directly executed under Matlab to recover the camera intrinsic and extrinsic parameters.
% IMPORTANT: This file contains neither the structure of the calibration objects nor the image coordinates of the calibration points.
%            All those complementary variables are saved in the complete matlab data file Calib_Results.mat.
% For more information regarding the calibration model visit http://www.vision.caltech.edu/bouguetj/calib_doc/


%-- Focal length:
fc = [ 3696.864875174875100 ; 3687.191251636521000 ];

%-- Principal point:
cc = [ 1761.973952949214900 ; 2420.279776735947100 ];

%-- Skew coefficient:
alpha_c = 0.000000000000000;

%-- Distortion coefficients:
kc = [ 0.039018495921262 ; -0.146938433433594 ; -0.000921877881348 ; 0.000958216251686 ; 0.000000000000000 ];

%-- Focal length uncertainty:
fc_error = [ 160.553259762997980 ; 127.369331350616800 ];

%-- Principal point uncertainty:
cc_error = [ 41.318059439062075 ; 166.687689846078850 ];

%-- Skew coefficient uncertainty:
alpha_c_error = 0.000000000000000;

%-- Distortion coefficients uncertainty:
kc_error = [ 0.033963620682586 ; 0.130072617268144 ; 0.003586846450159 ; 0.004119136236787 ; 0.000000000000000 ];

%-- Image size:
nx = 3480;
ny = 4640;


%-- Various other variables (may be ignored if you do not use the Matlab Calibration Toolbox):
%-- Those variables are used to control which intrinsic parameters should be optimized

n_ima = 6;						% Number of calibration images
est_fc = [ 1 ; 1 ];					% Estimation indicator of the two focal variables
est_aspect_ratio = 1;				% Estimation indicator of the aspect ratio fc(2)/fc(1)
center_optim = 1;					% Estimation indicator of the principal point
est_alpha = 0;						% Estimation indicator of the skew coefficient
est_dist = [ 1 ; 1 ; 1 ; 1 ; 0 ];	% Estimation indicator of the distortion coefficients


%-- Extrinsic parameters:
%-- The rotation (omc_kk) and the translation (Tc_kk) vectors for every calibration image and their uncertainties

%-- Image #1:
omc_1 = [ 2.436858e+00 ; -4.900980e-01 ; 3.513678e-01 ];
Tc_1  = [ -1.380664e+01 ; 1.386947e+02 ; 3.427185e+02 ];
omc_error_1 = [ 3.051521e-02 ; 1.094073e-02 ; 1.762582e-02 ];
Tc_error_1  = [ 3.962315e+00 ; 1.701611e+01 ; 1.569217e+01 ];

%-- Image #2:
omc_2 = [ 2.441330e+00 ; 2.820845e-01 ; -7.594808e-03 ];
Tc_2  = [ -1.460884e+02 ; 1.166723e+02 ; 3.947335e+02 ];
omc_error_2 = [ 3.234986e-02 ; 5.080250e-03 ; 1.368125e-02 ];
Tc_error_2  = [ 4.556488e+00 ; 1.912285e+01 ; 1.782377e+01 ];

%-- Image #3:
omc_3 = [ 2.050698e+00 ; 1.581533e+00 ; -4.966161e-01 ];
Tc_3  = [ -1.501991e+02 ; 6.894015e+00 ; 5.106493e+02 ];
omc_error_3 = [ 2.316486e-02 ; 1.862710e-02 ; 2.335638e-02 ];
Tc_error_3  = [ 5.713573e+00 ; 2.314447e+01 ; 2.235541e+01 ];

%-- Image #4:
omc_4 = [ 6.681376e-01 ; 2.789922e+00 ; -5.090248e-01 ];
Tc_4  = [ -1.738380e+01 ; -1.884448e+02 ; 5.637148e+02 ];
omc_error_4 = [ 8.505544e-03 ; 1.988191e-02 ; 2.596158e-02 ];
Tc_error_4  = [ 6.409417e+00 ; 2.331777e+01 ; 2.445668e+01 ];

%-- Image #5:
omc_5 = [ 8.913707e-01 ; -2.845295e+00 ; 5.930971e-01 ];
Tc_5  = [ 1.607921e+02 ; -1.417736e+02 ; 4.506971e+02 ];
omc_error_5 = [ 4.193077e-03 ; 1.576323e-02 ; 3.096931e-02 ];
Tc_error_5  = [ 5.201526e+00 ; 1.866742e+01 ; 1.969807e+01 ];

%-- Image #6:
omc_6 = [ 1.620076e+00 ; -2.318852e+00 ; 3.342076e-01 ];
Tc_6  = [ 1.252671e+02 ; -4.832943e+01 ; 3.823791e+02 ];
omc_error_6 = [ 1.344859e-02 ; 1.599451e-02 ; 2.105300e-02 ];
Tc_error_6  = [ 4.311704e+00 ; 1.677770e+01 ; 1.621985e+01 ];

