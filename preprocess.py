import typer
import numpy as np
import cv2
import numpy as np
import json
import os
import numpy.linalg as la
import subprocess

def remove_perspective(img,corners):
    corners = sorted(corners, key=lambda x: (la.norm(x), x))
  
    # Converting to homogenous coordinate system
    pts = np.array([(*p,1) for p in corners],dtype=np.float32)
    W = 500
    H = 500
    real_pts = np.array([
        [0, 0, 1],
        [0, H, 1],
        [W, 0, 1],
        [W, H, 1],
    ])
    shp=img.shape
    
    H1 = cv2.findHomography(pts,real_pts)[0]
    res_img = cv2.warpPerspective(img,H1,dsize=(W,H))
    # res_img = cv2.resize(res_img,dsize=(shp[1],shp[0]))
    return res_img

def select_vert_lines(width, height, lines):
  # remove outliers (compute line scopes, remove with unusual scope (quantile)
  # search for mean by x and y, select closest to the mean
    vert_lines = []
    for line in lines:  
        x, y, x2, y2 = line
        m = (y2-y)/(x2-x+0.001)
        if np.abs(m)>0.9:
            vert_lines.append(line)

    E = 0.001
    def get_slope(x1, y1, x2, y2, E):
        m = (y2-y1)/(x2-x1+E)
        return m

    def get_bias(x1, y1, slope):
        b = y1 - slope*x1
        return b

    xs, cropped_lines = [], []
    #print(vert_lines)
    for i, line in enumerate(vert_lines):
        # x, y, x2, y2 = line
        #remove very short lines
        line = np.array(line)
        a,b = line[:2],line[2:]

        m = (b[1]-a[1])/(b[0]-a[0]+E)
        n = a[1] - m*a[0]
        if 0>a[1]:
            a[1]=0
            a[0] = -n/m
        elif height<a[1]:
            a[1]=height-1
            a[0]=(a[1]-n)/m
        if 0>b[1]:
            b[1]=0
            b[0] = -n/m
        elif height<b[1]:
            b[1]=height-1
            b[0]=(b[1]-n)/m

        length = np.linalg.norm(a-b)
        if length < height/2.3 or not (0<=a[0]<=width+100 and 0<=b[0]<=width+100):
            continue

        x_i = int((a[0] + b[0])//2)
        xs.append(x_i)
        cropped_lines.append([a,b])

    x_mean = np.mean(np.array(xs))

    #cropped lines already fit in image, search for closest to mean
    dist_left, closest_i_left = width+10, None
    dist_right, closest_i_right = width+10, None
    for i, line in enumerate(cropped_lines):
        a,b = line
        x, y, x2, y2 = a[0],a[1],b[0],b[1]
        slope = get_slope(x, y, x2, y2, E)
        b = get_bias(x, y, slope)
        #-a/b = slope, c/b = -bias 
        
        dist_i = np.abs(slope*x_mean - height//2 + b)/(np.sqrt(np.square(slope)+1))
        if (x + x2)//2 > x_mean:
            if dist_i <= dist_right:
                dist_right = dist_i
                closest_i_right = i
        else:
            if dist_i <= dist_left:
                dist_left = dist_i
                closest_i_left = i
    if closest_i_left is None:
        l = [(1,1),(1,height)]
    else:
        l = cropped_lines[closest_i_left]
    if closest_i_right is None:
        r = [(width,1),(width,height)]
    else:
        r = cropped_lines[closest_i_right]

    points = [*l,*r]
    return x_mean, cropped_lines, points


def main(im_dir: str, out_dir:str):
    subprocess.call(["python", "-m","hawp.predict","--glob",im_dir+"/*.png","--disable-cuda","--json-output"])

    for filename in os.listdir(im_dir):
        if filename.endswith('.png'):
            im = cv2.imread(os.path.join(im_dir,filename))
            width, height = im.shape[0:2]
            
            with open(os.path.join(im_dir,filename) +'.wireframe.json') as f:
                ann=json.load(f)
                lines = []
                for i, edge in enumerate(ann['edges']):
                    v_i, v_j = edge
                    conf = ann['edges-weights'][i]
                    [x, y], [x2, y2] = ann['vertices'][v_i], ann['vertices'][v_j]
                    if conf > 0.8:
                        lines.append([int(x), int(y), int(x2), int(y2)])
                        # cv2.line(im, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), thickness=5)
                    
                x_mean, cropped_lines, points = select_vert_lines(width, height, lines)
                # im = cv2.circle(im, (int(x_mean), height//2), 3, (255, 0, 0), thickness=3)
                # for p in points:
                #     im = cv2.circle(im, (int(p[0]), int(p[1])), 3, (255, 0, 0), thickness=3)


                # for i, line in enumerate(cropped_lines):
                #     x, y, x2, y2 = line
                #     #cv2.line(im, (int(x), int(y)), (int(x2), int(y2)), (255, 255, 0), thickness=2)

                x, y, x2, y2 = points[0][0],points[0][1],points[1][0],points[1][1]
                # cv2.line(im, (int(x), int(y)), (int(x2), int(y2)), (0, 155, 0), thickness=6)
                x, y, x2, y2 = points[0][0],points[0][1],points[1][0],points[1][1]
                # cv2.line(im, (int(x), int(y)), (int(x2), int(y2)), (155, 0, 0), thickness=6)

                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                im2 = remove_perspective(im,points)
                cv2.imwrite(os.path.join(out_dir,filename), im2)



if __name__ == "__main__":
    typer.run(main)
