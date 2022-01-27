import os

import cv2
import imutils


def stitch(img_arrays: list, out_dir: str):
    images = img_arrays

    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    status, stitched = stitcher.stitch(images)
    if status == 0:
        cv2.imwrite(os.path.join(out_dir, 'whole_stitched.jpg'), stitched)
        return stitched
    else:
        print("[INFO] image stitching failed {}".format(status))
        return None
