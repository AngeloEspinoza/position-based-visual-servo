import cv2

# Colors
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

def draw_axis(img, start_pts, img_pts):
    start_point = list(start_pts[0].ravel().astype(int))
    end_point_x = list(img_pts[0].ravel().astype(int))
    end_point_y = list(img_pts[1].ravel().astype(int))
    end_point_z = list(img_pts[2].ravel().astype(int))

    cv2.arrowedLine(img, start_point, end_point_x, RED, 2)
    cv2.arrowedLine(img, start_point, end_point_y, GREEN, 2)
    cv2.arrowedLine(img, start_point, end_point_z, BLUE, 2)

    end_point_x[0] = end_point_x[0] + 10
    end_point_y[1] = end_point_y[1] - 10
    end_point_z[1] = end_point_z[1] + 10
    end_point_z[0] = end_point_z[0] - 10

    cv2.putText(img, 'x', end_point_x, cv2.FONT_HERSHEY_PLAIN, 0.8, RED, 1, cv2.LINE_AA)
    cv2.putText(img, 'y', end_point_y, cv2.FONT_HERSHEY_PLAIN, 0.8, GREEN, 1, cv2.LINE_AA)
    cv2.putText(img, 'z', end_point_z, cv2.FONT_HERSHEY_PLAIN, 0.8, BLUE, 1, cv2.LINE_AA)