from .base_stitch import stitch

import os
import numpy as np
import cv2


def stitch_crop(img_arrays: list, out_dir: str):
    stitched = stitch(img_arrays, out_dir)
    if stitched is None:
        print('[INFO] stitch crop failed')
        return None

    stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
    gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(cnts, key=cv2.contourArea)

    mask = np.zeros(thresh.shape, dtype="uint8")
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

    minRect = mask.copy()
    sub = mask.copy()

    while cv2.countNonZero(sub) > 0:
        minRect = cv2.erode(minRect, None)
        sub = cv2.subtract(minRect, thresh)

    cnts, hierarchy = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)

    stitched = stitched[y:y + h, x:x + w]
    cv2.imwrite(os.path.join(out_dir, 'whole_stitched_crop.jpg'), stitched)
    return stitched
