# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

import math


class BezierTools:

    @staticmethod
    def count_new_point_data(point0_co, point0_handle_right, point1_handle_left, point1_co, t):
        # get data for new point on Bezier curve between p0 and p1 without curve deformation
        point0_handle_right_new = (point0_handle_right - point0_co) * t + point0_co         # p0_hr new position
        t2 = (point1_handle_left - point0_handle_right) * t + point0_handle_right
        point1_handle_left_new = (point1_co - point1_handle_left) * t + point1_handle_left  # p1_hl new position
        point2_handle_left = (t2 - point0_handle_right_new) * t + point0_handle_right_new   # p2_hl position
        point2_handle_right = (point1_handle_left_new - t2) * t + t2                        # p2_hr position
        point2_co = (point2_handle_right - point2_handle_left) * t + point2_handle_left     # p2 position
        return [point0_handle_right_new, point2_handle_left, point2_co, point2_handle_right, point1_handle_left_new]

    @classmethod
    def deselect_all(cls, spline_object):
        for spline in spline_object.data.splines:
            cls.deselect_spline(bezier_spline=spline)

    @staticmethod
    def deselect_spline(bezier_spline):
        for bezier_point in bezier_spline.bezier_points:
            bezier_point.select_control_point = False
            bezier_point.select_left_handle = False
            bezier_point.select_right_handle = False

    @classmethod
    def segment_length(cls, point0, point1, resolution):
        # calculates bezier curve length between two points
        length = 0
        if resolution > 0:
            ratio = 1 / resolution
            p0 = point0.co
            for t in range(resolution - 1):
                p = cls.count_new_point_data(
                    point0_co=point0.co,
                    point0_handle_right=point0.handle_right,
                    point1_co=point1.co,
                    point1_handle_left=point1.handle_left,
                    t=ratio*(t + 1)
                )[2]
                length += CurveTools.vector_length(v0=p0, v1=p)
                p0 = p
            length += CurveTools.vector_length(v0=p0, v1=point1.co)     # last point
        return length

    @classmethod
    def spline_length(cls, bezier_spline, resolution):
        # calculates bezier curve length
        length = 0
        p0 = bezier_spline.bezier_points[0]
        for point in bezier_spline.bezier_points[1:]:
            length += cls.segment_length(point0=p0, point1=point, resolution=resolution)
            p0 = point
        if bezier_spline.use_cyclic_u:
            length += cls.segment_length(point0=p0, point1=bezier_spline.bezier_points[0], resolution=resolution)
        return length


class CurveTools:

    @classmethod
    def min_distance(cls, point0, point1):
        # returns minimal distance between two points
        return cls.vector_length(point0.co, point1.co)

    @staticmethod
    def vector_length(v0, v1):
        # return vector length
        return math.sqrt((v1[0] - v0[0]) ** 2 + (v1[1] - v0[1]) ** 2 + (v1[2] - v0[2]) ** 2)
