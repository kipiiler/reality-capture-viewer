def look_from_positive_z(vis):
    ctr = vis.get_view_control()
    ctr.set_front([0, 0, 1])
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, 1, 0])
    ctr.set_zoom(0.1)
    return False

def look_from_positive_x(vis):
    ctr = vis.get_view_control()
    ctr.set_front([1, 0, 0])
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, 0, 1])
    ctr.set_zoom(0.1)
    return False

def look_from_positive_y(vis):
    ctr = vis.get_view_control()
    ctr.set_front([0, 1, 0])
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, 0, 1])
    ctr.set_zoom(0.1)
    return False

key_to_callback = {}
key_to_callback[ord("Z")] = look_from_positive_z
key_to_callback[ord("X")] = look_from_positive_x
key_to_callback[ord("Y")] = look_from_positive_y