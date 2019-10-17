% match descriptors
%
% Input:
%   descr1        - k x n descriptor of first image
%   descr2        - k x m descriptor of second image
%   thresh        - scalar value to threshold the matches
%   
% Output:
%   matches       - 2 x w matrix storing the indices of the matching
%                   descriptors
function matches = matchDescriptors(descr1, descr2, thresh)
    [nb1, ~] = size(descr1);
    [nb2, ~] = size(descr2);
    matches= zeros(2,nb1);
    
    % distance function
    SSD= @(x1,x2) sum((x1-x2).^2);
    
    %the the best match (of im2) for each corner of im1
    for i=1:nb1
        d=thresh;
        for j=1:nb2
            d2=SSD(descr1(i,:),descr2(j,:));

            if d2<d
                matches(:,i)=[i;j];
                % if 2 candidates have similar distance remove both -> high
                % chance of error
                if d2/d <1.2 && d2/d >0.8
                    matches(:,i)=[0;0];
                    break;
                end
                d=d2;
            end
        end
    end
    
    %remove unmatched corners from matches
    matches( :, all(~matches,1) ) = [];
end