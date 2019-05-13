from control import matlab
if True:
    Ps = matlab.tf(*matlab.zpk2tf(
        [-0.01960354 -0.97998085j, -0.01960354 +0.97998085j, -0.01250354 -2.50067649j,
        -0.01250354 +2.50067649j, -0.02158274 -4.31649435j, -0.02158274 +4.31649435j,
        -0.06620907 -5.29631139j, -0.06620907 +5.29631139j, -0.10000737 -5.99960852j,
        -0.10000737 +5.99960852j, -0.03990608 -6.3848482j,  -0.03990608 +6.3848482j,
        -0.15808494 -7.90266611j, -0.15808494 +7.90266611j, -0.14137167 -8.48112199j,
        -0.14137167 +8.48112199j, -3.38325363-43.85197895j, -3.38325363+43.85197895j], 
        [-0.03023783-0.48285941j, -0.03023783+0.48285941j, -0.02739469-1.36946042j,
        -0.02739469+1.36946042j, -0.01747511-2.79596285j, -0.01747511+2.79596285j,
        -0.02280796-4.56153551j, -0.02280796+4.56153551j, -0.05943893-5.34917374j,
        -0.05943893+5.34917374j, -0.10136872-6.08127858j, -0.10136872+6.08127858j,
        -0.04618141-6.46523275j, -0.04618141+6.46523275j, -0.21441370-8.57386735j,
        -0.21441370+8.57386735j, -0.19949113-7.97715131j, -0.19949113+7.97715131j],
        3.64e-4))
    Pa = Ps#*700
    integ = matlab.tf([1],[1,0])