import numpy as np
import a1_data as p

points = np.array([[p.fuse_l1, 0, 0],                                   # 0 - front tip
                   [p.fuse_l2, p.fuse_h / 2, p.fuse_h / 2],             # 1 - nose top left
                   [p.fuse_l2, -p.fuse_h / 2, p.fuse_h / 2],            # 2 - nose top right
                   [p.fuse_l2, -p.fuse_h / 2, -p.fuse_h / 2],           # 3 - nose bot right
                   [p.fuse_l2, p.fuse_h / 2, -p.fuse_h / 2],            # 4 - nose bot left
                   [-p.fuse_l3, 0, 0],                                  # 5 - rear tip
                   [0, p.wing_w / 2, 0],                                # 6 - wing front left
                   [-p.wing_l, p.wing_w / 2, 0],                        # 7 - wing back left
                   [-p.wing_l, -p.wing_w / 2, 0],                       # 8 - wing back right
                   [0, -p.wing_w / 2, 0],                               # 9 - wing front right
                   [p.tailwing_l - p.fuse_l3, p.tailwing_w / 2, 0],     # 10 - tail wing front left
                   [-p.fuse_l3, p.tailwing_w / 2, 0],                   # 11 - tail wing back left
                   [-p.fuse_l3, -p.tailwing_w / 2, 0],                  # 12 - tail wing back right
                   [p.tailwing_l - p.fuse_l3, -p.tailwing_w / 2, 0],    # 13 - tail wing front right
                   [p.tailwing_l - p.fuse_l3, 0, 0],                    # 14 - vert front
                   [-p.fuse_l3, 0, p.tail_h],                           # 15 - vert top
                   ])
