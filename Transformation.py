import numpy as np




# L_temp: point that we are interested in
# p_LC: location of the RAS origin relative to global origin
L_temp = np.array([-8,4,-79])     
p_LC = np.array([107, 9, -121])  
# Translation of the CS
# Adding 1 to end of p_LCS and transforming to column vector - needed to get correct shape
p_LCST = np.append(p_LC, 1)
p_LCS = p_LCST.reshape(-1, 1)
   

L = L_temp.reshape(-1, 1)   # Column vector
R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])     # Rotation matrix (identity matrix as no rotation taking place)

T_1 = np.concatenate((R, L), axis=1)                # Partial creation of transformation matrix

finish_matrix = np.array([[0, 0, 0, 1]])            # Other part needed for transformation matrix

T_GL = np.concatenate((T_1, finish_matrix))         # Final transformation matrix

translated = np.dot(T_GL, p_LCS)                    # Result of translation
    
    
# Scaling of the CS
point1 = np.array([0, 22.3, -59.9])             # 3D Slicer point location  - want to find a better way of doing this
point2 = np.array([4, 5, 6])                    # Python point location
    
k1 = point2[0] / point1[0]                      # Finding scale factor in the x, y and z directions
k2 = point2[1] / point1[1]
k3 = point2[2] / point1[2]
    
Sk = [[k1, 0, 0, 0], [0, k2, 0, 0], [0, 0, k3, 0], [0, 0, 0, 1]]    # Scale factor matrix
    
finalCoords = np.dot(Sk, translated)
   