import os
import cv2


def vertical_stitch(img_arrays: list, out_dir: str):
    base_width = img_arrays[0].shape[1]
    img_arrays = list(img_arrays)
    for i in range(len(img_arrays)):
        if img_arrays[i].shape[1] != base_width:
            ratio = base_width * 1.0 / img_arrays[i].shape[1]
            img_arrays[i] = cv2.resize(img_arrays[i], (0, 0), fx=ratio, fy=ratio)

    stitched = cv2.vconcat(img_arrays)
    cv2.imwrite(os.path.join(out_dir, 'vertical_stitched.jpg'), stitched)
    return stitched
