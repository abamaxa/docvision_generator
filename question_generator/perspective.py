from math import cos, sin, radians, hypot, tan
import time

from PIL import Image
import numpy as np
import cv2

# taken from Iwillnotexist Idonotexist at
# https://stackoverflow.com/questions/17087446/how-to-calculate-perspective-transform-for-opencv-from-rotation-angles
def warp_matrix(sz, theta, phi, gamma, scale, fovy) :      
    corners = []
    st = sin(radians(theta))
    ct = cos(radians(theta))
    sp = sin(radians(phi))
    cp = cos(radians(phi))
    sg = sin(radians(gamma))
    cg = cos(radians(gamma))

    halfFovy = fovy*0.5
    d = hypot(sz[0],sz[1])
    sideLength = scale * d / cos(radians(halfFovy))
    h = d / (2.0 * sin(radians(halfFovy)))
    n = h - (d / 2.0)
    f = h + (d / 2.0)

    F = np.identity(4) # Allocate 4x4 transformation matrix F
    Rtheta = np.identity(4) # Allocate 4x4 rotation matrix around Z-axis by theta degrees
    Rphi = np.identity(4) # Allocate 4x4 rotation matrix around X-axis by phi degrees
    Rgamma = np.identity(4) # Allocate 4x4 rotation matrix around Y-axis by gamma degrees

    T = np.identity(4) # Allocate 4x4 translation matrix along Z-axis by -h units
    P = np.zeros((4,4)) # Allocate 4x4 projection matrix

     # Rtheta
    Rtheta[0,0]=Rtheta[1,1]=ct
    Rtheta[0,1]=-st
    Rtheta[1,0]=st
     # Rphi
    Rphi[1,1]=Rphi[2,2]=cp
    Rphi[1,2]=-sp
    Rphi[2,1]=sp
     # Rgamma
    Rgamma[0,0]=Rgamma[2,2]=cg
    Rgamma[0,2]=sg
    Rgamma[2,0]=sg

     # T
    T[2,3]=-h
     # P
    P[0,0]=P[1,1]=1.0/tan(radians(halfFovy))
    P[2,2]=-(f+n)/(f-n)
    P[2,3]=-(2.0*f*n)/(f-n)
    P[3,2]=-1.0
    
    F = np.matmul(Rtheta, Rgamma)
    F = np.matmul(Rphi, F)
    F = np.matmul(T, F)
    F = np.matmul(P, F)
    
     # Transform 4x4 points
    ptsIn = np.zeros(12) 
    
    halfW=sz[0]/2
    halfH=sz[1]/2

    ptsIn[0]=-halfW
    ptsIn[1]= halfH
    ptsIn[3]= halfW
    ptsIn[4]= halfH
    ptsIn[6]= halfW
    ptsIn[7]=-halfH
    ptsIn[9]=-halfW
    ptsIn[10]=-halfH
    
    ptsInMat = ptsIn.reshape((1, 4, 3))
    ptsOutMat = cv2.perspectiveTransform(ptsInMat,F) # Transform points

    # Get 3x3 transform and warp image
    ptsInPt2f = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], dtype=np.float32)
    ptsOutPt2f = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], dtype=np.float32)
    half_side = sideLength * 0.5
    
    for i in range(4) :
        ptsInPt2f[i][0] = ptsIn[i * 3 + 0] + halfW
        ptsInPt2f[i][1] = ptsIn[i * 3 + 1] + halfH
        ptsOutPt2f[i][0] = (ptsOutMat[0][i][0] + 1) * half_side
        ptsOutPt2f[i][1] = (ptsOutMat[0][i][1] + 1) * half_side       
    
    M = cv2.getPerspectiveTransform(ptsInPt2f,ptsOutPt2f)

     # Load corners vector
    corners = []
    corners.append(ptsOutPt2f[0]) # Push Top Left corner
    corners.append(ptsOutPt2f[1]) # Push Top Right corner
    corners.append(ptsOutPt2f[2]) # Push Bottom Right corner
    corners.append(ptsOutPt2f[3]) # Push Bottom Left corner

    return M, corners

def warp_image(src, theta, phi, gamma, scale, fovy) :
    size = ((src.shape[1], src.shape[0]))
    halfFovy=fovy*0.5
    d=hypot(size[0],size[1])
    sideLength=int(scale*d/cos(radians(halfFovy)))

    M, corners = warp_matrix(size,theta,phi,gamma, scale,fovy) # Compute warp matrix
    return cv2.warpPerspective(src, M, (sideLength,sideLength)) # Do actual image warp

# taken from mmgp at
# https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

# taken from amir at
# https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
def find_rotation_coeffs(theta, x0, y0):
    ct = math.cos(math.radians(theta))
    st = math.sin(math.radians(theta))
    return np.array([ct, -st, x0*(1-ct) + y0*st, 
                     st,  ct, y0*(1-ct) - x0*st, 
                     0, 0])


def transform_test_opencv() :
    img = cv2.imread("www_output/17601.png")
    
    start_time = time.time()
    counter = 0
    for r in range(-25,30,5) :
        for z in range(-40,45,5) :
            for y in range(-25,30,5) :
                img2 = warp_image(img, r, z, y, 1, 30)
                cv2.imwrite("open_output/cvwow-{}-{}-{}.png".format(r,z,y), img2)
                counter +=1
                
    print("Wrote {} images in {:.2f} seconds".format(counter, time.time() - start_time))

def transform_test() :
    img = Image.open("www_output/17601.png")
    
    #coeff = find_coeffs([(0, 0), (256, 0), (256, 256), (0, 256)],
    #    [(0, 0), (256, 0), (new_width, height), (xshift, height)]))

    
    M, corners = warp_matrix((1000, 1375),5, 50, 0, 1, 30)
    
    coeff = find_coeffs([(0, 0), (1000, 0), (1000, 1375), (0, 1375)], 
                        [corners[3], corners[2], corners[1], corners[0] ])
    
    pimg = img.transform((1000, 1375), Image.PERSPECTIVE, coeff)
    
    pimg.save("wow.png")
    
if __name__ == '__main__' :
    transform_test_opencv()