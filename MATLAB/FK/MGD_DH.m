%% LABWORK2 - quest�o 1

% Escrever uma fun��o MGD_DH que permita estabelecer a posi��o e orienta��o
% da ferramenta de um r�bo com estrutura arbitr�ria: n graus de liberdade e
% com juntas de revolu��o e/ou prism�ticas.

function [Mt, Mi] = MGD_DH(PJ_DH)

n = size(PJ_DH,1);

for i = 1:1:n
     
    Mi(:, :, i) = [ cos(PJ_DH(i,1))  -sin(PJ_DH(i,1))*cos(PJ_DH(i,3))  sin(PJ_DH(i,1))*sin(PJ_DH(i,3))   PJ_DH(i,4)*cos(PJ_DH(i,1));
                    sin(PJ_DH(i,1))  cos(PJ_DH(i,1))*cos(PJ_DH(i,3))   -cos(PJ_DH(i,1))*sin(PJ_DH(i,3))  PJ_DH(i,4)*sin(PJ_DH(i,1));
                    0           sin(PJ_DH(i,3))              cos(PJ_DH(i,3))              PJ_DH(i,2);
                    0           0                       0                       1];
end

Mt = Mi(:,:,1);
for j = 2:1:n
    Mt = Mt * Mi(:,:,j);
end


end