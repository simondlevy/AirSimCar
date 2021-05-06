'''
Adapted from
https://github.com/microsoft/AirSim/blob/master/PythonClient/car/hello_car.py

MIT License
'''
import airsim
import cv2
import numpy as np
import os
import time
import tempfile
from sys import stdout


def debug(message):
    print(message)
    stdout.flush()


def main():

    # connect to the AirSim simulator
    client = airsim.CarClient()
    client.confirmConnection()
    client.enableApiControl(True)
    debug("API Control enabled: %s" % client.isApiControlEnabled())
    car_controls = airsim.CarControls()

    tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_car")

    debug("Saving images to %s" % tmp_dir)

    try:
        os.makedirs(tmp_dir)
    except OSError:
        if not os.path.isdir(tmp_dir):
            raise

    for idx in range(3):
        # get state of the car
        car_state = client.getCarState()
        debug("Speed %d, Gear %d" % (car_state.speed, car_state.gear))

        # go forward
        car_controls.throttle = 0.5
        car_controls.steering = 0
        client.setCarControls(car_controls)
        debug("Go Forward")
        time.sleep(3)   # let car drive a bit

        # Go forward + steer right
        car_controls.throttle = 0.5
        car_controls.steering = 1
        client.setCarControls(car_controls)
        debug("Go Forward, steer right")
        time.sleep(3)   # let car drive a bit

        # go reverse
        car_controls.throttle = -0.5
        car_controls.is_manual_gear = True
        car_controls.manual_gear = -1
        car_controls.steering = 0
        client.setCarControls(car_controls)
        debug("Go reverse, steer right")
        time.sleep(3)   # let car drive a bit
        car_controls.is_manual_gear = False  # change back gear to auto
        car_controls.manual_gear = 0

        # apply brakes
        car_controls.brake = 1
        client.setCarControls(car_controls)
        debug("Apply brakes")
        time.sleep(3)   # let car drive a bit
        car_controls.brake = 0  # remove brake

        # get camera images from the car
        responses = client.simGetImages([

            # depth visualization image
            airsim.ImageRequest("0", airsim.ImageType.DepthVis),

            # depth in perspective projection
            airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True),

            # scene vision image in png format
            airsim.ImageRequest("1", airsim.ImageType.Scene),

            # scene vision image in uncompressed RGB array
            airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])

        debug('Retrieved images: %d' % len(responses))

        for response_idx, response in enumerate(responses):
            fmt = f"{idx}_{response.image_type}_{response_idx}"
            filename = os.path.join(tmp_dir, fmt)

            if response.pixels_as_float:
                debug("Type %d, size %d" % (response.image_type,
                      len(response.image_data_float)))
                airsim.write_pfm(os.path.normpath(filename + '.pfm'),
                                 airsim.get_pfm_array(response))
            elif response.compress:  # png format
                debug("Type %d, size %d" %
                      (response.image_type, len(response.image_data_uint8)))
                airsim.write_file(os.path.normpath(filename + '.png'),
                                  response.image_data_uint8)
            else:  # uncompressed array
                debug("Type %d, size %d" %
                      (response.image_type, len(response.image_data_uint8)))

                # get numpy array
                img1d = np.fromstring(response.image_data_uint8,
                                      dtype=np.uint8)

                # reshape array to 3 channel image array H X W X 3
                img_rgb = img1d.reshape(response.height, response.width, 3)

                # write to png
                cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb)

    # restore to original state
    client.reset()

    client.enableApiControl(False)


main()
