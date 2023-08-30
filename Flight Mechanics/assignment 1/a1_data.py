import numpy as np

fuse_l1 = 2.8
fuse_l2 = 0.1
fuse_l3 = 5
fuse_w = 1
fuse_h = 1
wing_l = 1.5
wing_w = 7
tail_l = 1
tail_h = 1.5
tailwing_w = 3.3
tailwing_l = 0.75
prop_l = 2
prop_w = 0.5

points = np.array([[fuse_l1, 0, 0],                                   # 0 - front tip
                   [fuse_l2, fuse_h / 2, fuse_h / 2],             # 1 - nose top left
                   [fuse_l2, -fuse_h / 2, fuse_h / 2],            # 2 - nose top right
                   [fuse_l2, -fuse_h / 2, -fuse_h / 2],           # 3 - nose bot right
                   [fuse_l2, fuse_h / 2, -fuse_h / 2],            # 4 - nose bot left
                   [-fuse_l3, 0, 0],                                  # 5 - rear tip
                   [0, wing_w / 2, 0],                                # 6 - wing front left
                   [-wing_l, wing_w / 2, 0],                        # 7 - wing back left
                   [-wing_l, -wing_w / 2, 0],                       # 8 - wing back right
                   [0, -wing_w / 2, 0],                               # 9 - wing front right
                   [tailwing_l - fuse_l3, tailwing_w / 2, 0],     # 10 - tail wing front left
                   [-fuse_l3, tailwing_w / 2, 0],                   # 11 - tail wing back left
                   [-fuse_l3, -tailwing_w / 2, 0],                  # 12 - tail wing back right
                   [tailwing_l - fuse_l3, -tailwing_w / 2, 0],    # 13 - tail wing front right
                   [tailwing_l - fuse_l3, 0, 0],                    # 14 - vert front
                   [-fuse_l3, 0, tail_h],                           # 15 - vert top
                   ])
