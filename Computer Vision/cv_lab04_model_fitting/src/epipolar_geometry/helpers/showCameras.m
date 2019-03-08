% showCameras(Ms, fig)
%
% Input
%   Ms      cell array of 4x4 transformation matrices ([R|t]) with last row
%           equal to [0 0 0 1]
%   fig     figure id

function showCameras(Ms, fig)
    n_cam = length(Ms);

    for k = 1:n_cam
        if size(Ms{k},1) == 3
            Ms{k} = [Ms{k}; 0 0 0 1];
        end
    end
    
    o = [0, 0, 0, 1]';
    x = [1, 0, 0, 1]';
    y = [0, 1, 0, 1]';
    z = [0, 0, 1, 1]';

    po = zeros(4, n_cam);
    px = zeros(4, n_cam);
    py = zeros(4, n_cam);
    pz = zeros(4, n_cam);

    for k = 1:n_cam
        po(:, k) = Ms{k}\o;
        px(:, k) = Ms{k}\x;
        py(:, k) = Ms{k}\y;
        pz(:, k) = Ms{k}\z;
    end

    figure(fig);
    hold on, line([po(1, :); px(1,:)], [po(2, :); px(2,:)], [po(3, :); px(3,:)], 'Color', [1, 0, 0]);
    hold on, line([po(1, :); py(1,:)], [po(2, :); py(2,:)], [po(3, :); py(3,:)], 'Color', [0, 1, 0]);
    hold on, line([po(1, :); pz(1,:)], [po(2, :); pz(2,:)], [po(3, :); pz(3,:)], 'Color', [0, 0, 1]);
    %axis equal;
    grid on;
    axis equal
end
