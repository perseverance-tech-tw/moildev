"""

This is the testing code of moildev, for a green hand people will very easy to get
the idea about what the moildev do during the processing.

last modified: 13/07/2023
writer: Haryanto
contact: perseverance@gmail.com

"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from moildev import Moildev
import cv2

#  Specify the size of window show image
w, h = 400, 300


image = cv2.imread("image_virtual.png")
image = cv2.circle(image, (1295, 1844), 25, (0, 255, 0), 25)
image_experiment = cv2.imread("image_experiment.png")
image_experiment = cv2.circle(image_experiment, (1295, 1844), 25, (0, 255, 0), 25)

original_colon = cv2.resize(image_experiment, (w, h))
cv2.imshow("original experiment", original_colon)

original = cv2.resize(image, (w, h))
cv2.imshow("original virtual", original)

# create moildev object
moildev_virtual = Moildev("params_virtual.json")
moildev = Moildev("params_camera.json")

# test anypoint mode 1 virtual image
map_x, map_y = moildev_virtual.maps_anypoint_mode1(90, 180, 2)
anypoint_m1_by_maps_virtual = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
anypoint_m1_by_maps_virtual = cv2.resize(anypoint_m1_by_maps_virtual, (w, h))
cv2.imshow("anypoint mode 1 by maps virtual image", anypoint_m1_by_maps_virtual)

anypoint_m1 = moildev.anypoint_mode1(image_experiment, 90, 180, 2)
anypoint_m1 = cv2.resize(anypoint_m1, (w, h))
cv2.imshow("anypoint mode 1", anypoint_m1)

# test anypoint mode 2 car
map_x, map_y = moildev_virtual.maps_anypoint_mode2(-90, 0, 0, 3)
anypoint_m2_by_maps = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
anypoint_m2_by_maps = cv2.resize(anypoint_m2_by_maps, (w, h))
cv2.imshow("anypoint mode 2 by maps", anypoint_m2_by_maps)

# anypoint mode 2 using image experiment
anypoint_m2_exp = moildev.anypoint_mode2(image_experiment, -90, 0, 0, 3)
anypoint_m2_exp = cv2.resize(anypoint_m2_exp, (w, h))
cv2.imshow("anypoint mode 2 experiment", anypoint_m2_exp)

# panorama tube
panorama_tube = moildev_virtual.panorama_tube(image, 10, 110)
panorama_tube = cv2.resize(panorama_tube, (round(panorama_tube.shape[1] / 4), round(panorama_tube.shape[0] / 4)))
cv2.imshow("panorama tube virtual image", panorama_tube)

# panorama tube
panorama_tube = moildev.panorama_tube(image_experiment, 10, 110)
panorama_tube = cv2.resize(panorama_tube, (round(panorama_tube.shape[1] / 4), round(panorama_tube.shape[0] / 4)))
cv2.imshow("panorama tube", panorama_tube)

# test panorama car
panorama_car = moildev_virtual.panorama_car(image, 180, 90, 0, 0, 1, 0, 1)
panorama_car = cv2.resize(panorama_car, (round(panorama_car.shape[1] / 6), round(panorama_car.shape[0] / 6)))
cv2.imshow("panorama car", panorama_car)

recenter = moildev.recenter(image, 110, -90, 0)
recenter = cv2.resize(recenter, (w, h))
cv2.imshow("recenter", recenter)

cv2.waitKey(0)
