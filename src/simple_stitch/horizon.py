import os
import cv2


def horizon_stitch(img_arrays: list, out_dir: str):
    base_height = img_arrays[0].shape[0]
    img_arrays = list(img_arrays)
    for i in range(len(img_arrays)):
        if img_arrays[i].shape[0] != base_height:
            ratio = base_height * 1.0 / img_arrays[i].shape[0]
            img_arrays[i] = cv2.resize(img_arrays[i], (0, 0), fx=ratio, fy=ratio)

    stitched = cv2.hconcat(img_arrays)
    cv2.imwrite(os.path.join(out_dir, 'horizon_stitched.jpg'), stitched)
    return stitched
