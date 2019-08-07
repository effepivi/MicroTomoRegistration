import math
import numpy as np


def lsf(x):
    a2              = 601.873;
    b2              = 54.9359;
    c2              = -3.58452;
    d2              = 0.469614;
    e2              = 6.32561e+09;
    f2              = 1.0;
    
    if hasattr(x, "__len__") == False:
    
        temp_1 = (2.0/(math.sqrt(math.pi)*e2*f2))*math.exp(-(x*x)/(e2*e2));
        temp_2 = 1.0 / (b2 * c2) * math.pow(1+(x*x)/(b2*b2),-1);
        temp_3 = math.pow(2.0/f2+math.pi/c2, -1);
        value = (temp_1 + temp_2) * temp_3;
    
    else:
    
        value = np.zeros(len(x));

        for i in range(1,len(x)):
            temp_1 = (2.0/(math.sqrt(math.pi)*e2*f2))*math.exp(-(x[i]*x[i])/(e2*e2));
            temp_2 = 1.0 / (b2 * c2) * math.pow(1+(x[i]*x[i])/(b2*b2),-1);
            temp_3 = math.pow(2.0/f2+math.pi/c2, -1);
            value[i] = (temp_1 + temp_2) * temp_3;     
        
    print(value)
    
    return value

