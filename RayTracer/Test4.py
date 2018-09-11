import numpy as np
import tkinter as tk
import sys

class ray_canvas(tk.Canvas):
    # Initialize with mouse enter and exit binds
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        test = 1
        self.region_started_flag = False
        self.node0_distance = 10
        self.all_regions = []
        self.all_rays = []
        self.top_rays = []
        self.motion_tag = None
        self.button_tag = None
        self.left = False
        self.bind('<Enter>', self.enter_cmd)
        self.bind('<Leave>', self.leave_cmd)
        self.polygons = []

    def enter_cmd(self, event):
        self.motion_tag = self.bind('<Motion>', self.motion_func)
        self.button_tag = self.bind('<Button-1>', self.button_func)

    def leave_cmd(self, event):
        self.unbind('<Motion>', self.motion_tag)
        self.unbind('<Button-1>', self.button_tag)

    def update_top_rays(self):
        if len(self.all_regions) > 1:
            test = 1
        pass

    def CCW_angle(self, v_0, v_1):

        cos_angles = []
        sin_angles = []

        new_cos_angle = np.dot(v_0, v_1)
        new_cos_angle = np.arccos(new_cos_angle)
        cos_angles.append(new_cos_angle)

        new_sin_angle = np.cross(v_0, v_1)
        new_sin_angle = np.arcsin(new_sin_angle)
        sin_angles.append(new_sin_angle)

        # Note: acos range is from 0 to pi
        # Note: asin range is from -pi/2 to pi/2
        # ---> Flipped because of coordinate system???
        if new_sin_angle > 0:
            angle = new_cos_angle
            angle_helper = new_cos_angle / np.pi
        else:
            angle = 2 * np.pi - new_cos_angle
            angle_helper = (2 * np.pi - new_cos_angle) / np.pi

        return angle

    def rotation_array(self, angle):
        return np.array([[np.cos(angle), -np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])

    def find_intersections(self, test_ray, lines):

        intersection_number = 0
        intersection_times = []
        intersection_rays = []
        intersection_points = []

        ray_v = test_ray.get_v()
        ray_p0 = test_ray.get_p0()

        test_line_number = -1
        for test_line in lines:
            # Equation to solve
            # p0 + v0*t0 = p1 + v1*t1
            # v0*t0 - v1*t1 = p1 - p0
            # t * v = p
            # t = p * v^-1
            #
            # v = [[v0x, v0y],
            #      [v1x, v1y]]
            # t = [t0, -t1]
            # p = [p1x - p0x, p1y - p0y]

            test_line_number += 1
            line_v = test_line.get_v()
            line_p0 = test_line.get_p0()

            v = np.array([[ray_v[0], ray_v[1]], [line_v[0], line_v[1]]])
            p = line_p0 - ray_p0

            if np.linalg.det(v) == 0:
                # Lines are parallel, no intersection
                pass
            else:
                # Find the intersection. note that t[1] is negative!
                t = np.matmul(p, np.linalg.inv(v))

                if (0 <= t[0] <= test_ray.get_t1()) and \
                        (0 <= -t[1] <= test_line.get_t1()):
                    intersection_times.append(t[0])
                    intersection_rays.append(test_line_number)

        for t1 in intersection_times:
            intersection_number += 1
            intersection_points.append(test_ray.get_p0() + t1 * test_ray.get_v())
        return {'number': intersection_number,
                'times': intersection_times,
                'rays': intersection_rays,
                'points': intersection_points}


    def motion_func(self, event):

        started_flag = self.region_started_flag
        new_point = np.array([event.x, canvas_height + 1 - event.y])
        canvas.itemconfigure(position_text, text=str(event.x) + ',' + str(canvas_height + 1 - event.y))

        # If the ray is being drawn, redraw its line
        if started_flag:
            new_region_rays = self.all_rays[-1]

            line_tag = new_region_rays[-1].get_name()
            p0 = new_region_rays[-1].get_p0()

            node0 = new_region_rays[0].get_p0()
            t_node0 = new_point - node0
            t_node0 = np.linalg.norm(t_node0)

            def draw_full_ray():
                # Priorities for line drawing protocols:
                # 1. If there's an intersection, draw up to it (first)
                # 2. If the ray nears node0, try to stick to it
                # 3. Else, just draw it.
                if len(new_region_rays) < 2:
                    canvas.coords(line_tag, p0[0], canvas_height + 1 - p0[1],
                                  event.x, event.y)
                elif first_intersection['number'] is not 0:
                    canvas.coords(line_tag, p0[0], canvas_height + 1 - p0[1],
                                  first_intersection['points'][0][0],
                                  canvas_height + 1 - first_intersection['points'][0][1])
                elif t_node0 < self.node0_distance:
                    canvas.coords(line_tag, p0[0], canvas_height + 1 - p0[1],
                                  node0[0], canvas_height + 1 - node0[1])
                else:
                    canvas.coords(line_tag, p0[0], canvas_height + 1 - p0[1],
                                  event.x, event.y)

            if len(new_region_rays) < 2:
                first_intersection = {'number': 0}
            else:
                # If there's an intersection, only draw line up to it.
                temp_ray = new_region_rays[-1]
                temp_ray.set_p1(new_point)
                temp_ray.finish_ray()
                first_intersection = self.find_intersections(temp_ray, new_region_rays[:-2])

            draw_full_ray()

    def button_func(self, event):
        # Get the new point.
        started_flag = canvas.region_started_flag
        new_point = np.array([event.x, canvas_height + 1 - event.y])
        new_region_rays = []        # Just a holder for global user in make_new_ray. Will redefine
                                    # according to conditional.

        def make_new_ray(point):
            # Simple create ray. But need to know which number ray in which region
            # Once ray is created, draw it on the canvas and return it.
            new_ray = ray()
            new_ray.set_p0(point)
            new_ray.set_name('region' + str(len(self.all_regions)) +
                             '_ray' + str(len(new_region_rays)))
            canvas.create_line(point[0], point[1],
                               point[0], point[1],
                               fill='black', width=2, tags=new_ray.get_name())
            return new_ray

        if not started_flag:
            # Ray and region new. Draw trivial line.
            # Create new region for all_rays and add the new ray to the list.
            started_flag = True
            new_region_rays = [make_new_ray(new_point)]
            self.all_rays.append(new_region_rays)

        elif started_flag:
            # Ray is ending. Add the last point to the current (last) region, compute v and t1
            # Gather the newest region's rays
            # new_region_rays is an ALIAS
            new_region_rays = self.all_rays[-1]

            if len(new_region_rays) < 2:
                # Say no intersection possible. Just finish and create new ray.
                new_region_rays[-1].set_p1(new_point)
                new_region_rays[-1].finish_ray()
                new_region_rays.append(make_new_ray(new_point))
                # self.all_rays[-1] = new_region_rays

            else:
                # If the ray is ending near the first node, close the region.
                t_node0 = new_region_rays[-1].get_p1() - new_region_rays[0].get_p0()
                t_node0 = np.linalg.norm(t_node0)

                if t_node0 < self.node0_distance:
                    started_flag = False
                    new_region_rays[-1].set_p1(new_region_rays[0].get_p0())
                    new_region_rays[-1].finish_ray()
                    # self.all_rays[-1] = new_region_rays

                    new_region = region(new_region_rays)
                    new_region.finish_region()
                    self.all_regions.append(new_region)

                    self.update_top_rays()

                else:
                    # Not closing. Keep going.
                    new_region_rays[-1].set_p1(new_point)
                    new_region_rays[-1].finish_ray()
                    new_region_rays.append(make_new_ray(new_point))
                    # self.all_rays[-1] = new_region_rays

        self.region_started_flag = started_flag

class region(object):

    def __init__(self, init_rays=None):
        self.rays = []
        self.num_rays = 0
        self.inside_angles = []
        self.inside_direction = None
        self.area = None
        self.colors = ['white', 'black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
        self.name = None
        self.refractive_index = None
        self.depth = len(canvas.all_regions)
        self.polygon = None
        if init_rays is not None:
            for i in init_rays:
                self.add_ray(i)

    def add_ray(self, new_ray):
        self.rays.append(new_ray)
        self.num_rays += 1

    def set_inside_angles(self, angles):
        self.inside_angles = angles

    def set_inside_direction(self, direction):
        self.inside_direction = direction

    def set_area(self, area):
        self.area = area

    def get_ray(self, ray_num):
        return self.rays[ray_num]

    def get_all_rays(self):
        return self.rays

    def get_num_rays(self):
        return self.num_rays

    def get_inside_angles(self):
        return self.inside_angles

    def get_inside_direction(self):
        return self.inside_direction

    def get_area(self):
        return self.area

    def finish_region(self):

        def finish_angles():

            # First, figure out inside/outside by checking angles
            # Inside has total angle sum(i) = 180*(n-2)
            # Outside has total angle sum(360-i) = 360*n - 180*(n-2)
            #                                    = 180*(n+2)
            # Get oriented angles with cross product:
            # sin(q) = cross(a,b)       because vectors are unit velocity
            # in 2D, no other complications needed - sign gives +CCW / -CW

            CCW_angles = []

            for i in range(self.get_num_rays()):
                CCW_angles.append((region_rays[i].angle - region_rays[(i - 1) % self.get_num_rays()].angle + np.pi) %
                                  (2 * np.pi))

            # Find inside. Check if sum within 1 degree of expected
            CCW_sum = sum(CCW_angles) * 180 / np.pi
            inside_angle_sum = 180 * (self.get_num_rays() - 2)
            if inside_angle_sum - 1 < CCW_sum < inside_angle_sum + 1:
                # CCW angles are inside
                # These angles are drawn from ray i to ray i+1 in the given rotation direction
                self.set_inside_direction('CCW')
                self.set_inside_angles(CCW_angles)
            else:
                self.set_inside_direction('CW')
                for i in range(len(CCW_angles)):
                    CCW_angles[i] = 2 * np.pi - CCW_angles[i]
                self.set_inside_angles(CCW_angles)

        def finish_area():

            # FIND AREA. integrate over dx.
            # 1. Find minimum and maximum x of polygon.
            # 2. Find intersections of x = x0
            # 3. If odd intersections, figure out singular
            # 3a. singular has rays pointing in opposite +/-
            # 3b. paired has rays pointing in either both + or both -
            # 3c. treat x = 0 as a pair.
            # 4. Sum between pairs. Add singulars.
            area = 0
            region_points = []
            min_x = canvas_width
            max_x = 0
            for i in region_rays:
                new_point = i.get_p0()
                region_points.append(new_point[0])
                if new_point[0] < min_x:
                    min_x = new_point[0]
                if new_point[0] > max_x:
                    max_x = new_point[0]

            x0_ray = ray()
            for x0 in range(min_x, max_x + 1):
                x0_ray.set_p0(np.array([x0, 0]))
                x0_ray.set_p1(np.array([x0, canvas_height]))
                x0_ray.finish_ray()
                intersections = canvas.find_intersections(x0_ray, region_rays)
                if intersections['number'] == 0:
                    pass
                elif intersections['number'] % 2 == 0:
                    for i in range(intersections['number'] // 2):
                        area += intersections['points'][2*i] - intersections['points'][2*i+1] + 1

            self.set_area(area)

        def finish_polygon():

            # Replace with a filled polygon
            draw_region_p0s = []
            for i in region_rays:
                draw_region_p0s.append([i.p0[0], canvas_height + 1 - i.p0[1]])

                canvas.delete(i.get_name())
            new_polygon = canvas.create_polygon(draw_region_p0s,
                                                fill=self.colors[len(canvas.all_regions)],
                                                outline='black',
                                                tags=self.name)
            self.polygon = new_polygon

        def finish_refractive_index():

            # Generate input window for refractive index
            def input_button_cmd(event=None):
                self.refractive_index = input_entry.get()
                n_input.destroy()

            n_input = tk.Toplevel(root)
            n_input.title('n Input')
            input_text = tk.Label(n_input, text='Input refractive index \n n for this feature:')
            input_text.grid()
            input_entry = tk.Entry(n_input, width=10)
            input_entry.grid()
            input_button = tk.Button(n_input, text='OK', command=input_button_cmd)
            input_button.grid()
            n_input.bind('<Return>', input_button_cmd)

            input_entry.focus()

            root.wait_window(n_input)

        def finish_layer_order():

            def test_vertices_in_ref(ref_region, test_region):

                ref_ray_0 = ref_region.rays[-1]
                ref_ray_1 = ref_region.rays[0]
                ref_point = ref_ray_1.get_p0()
                test_points_inside = []

                for test_region_ray in test_region.rays:
                    new_test_ray = ray()
                    new_test_ray.set_p0(ref_point)
                    new_test_ray.set_p1(test_region_ray.get_p0())
                    new_test_ray.finish_ray()

                    # See if test ray is between ref rays.
                    # get ref_angle_1 - ref_angle_0 % 2pi
                    # get test_angle - ref_angle_0 % 2pi
                    # if latter less than former, between True?
                    ref_angle = (ref_ray_1.angle - ref_ray_0.angle + np.pi) % (2 * np.pi)
                    test_angle = (new_test_ray.angle - ref_ray_0.angle + np.pi) % (2 * np.pi)
                    if test_angle < ref_angle:
                        # test ray between ref rays!
                        # The test ray starts inside the ref polygon
                        starts_inside = True
                    else:
                        starts_inside = False

                    test_intersections = canvas.find_intersections(new_test_ray, ref_region.get_all_rays())
                    # Delete intersections that happen at the initial ref point, t=0
                    # Test for t < 0.001
                    intersections_to_delete = []
                    for int_index in range(test_intersections['number']):
                        if np.abs(test_intersections['times'][int_index]) < 0.001:
                            intersections_to_delete.append(int_index)
                    for i in reversed(intersections_to_delete):
                        test_intersections['number'] -= 1
                        del(test_intersections['points'][i])
                        del(test_intersections['rays'][i])
                        del(test_intersections['times'][i])
                    num_intersections_odd = bool(test_intersections['number'] % 2)

                    # 4 conditions:
                    # starts_inside True AND test_intersections even: inside
                    # starts_inside True AND test_intersections odd: outside
                    # starts_inside False AND test_intersections even: outside
                    # starts_inside False AND test_intersections odd: inside
                    if (starts_inside and not num_intersections_odd) or \
                            (not starts_inside and num_intersections_odd):
                        # test point is inside ref region
                        test_points_inside.append(True)
                    else:
                        test_points_inside.append(False)

                return test_points_inside

            # Resolve top level rays for tracing!
            # Only necessary for polygons that the top (new) one overlaps with.
            # Find polygons that the top one overlaps (partially or completely) with.

            # Finishing region is new so just add rays
            canvas.top_rays += self.rays

            # check regions below top for partial or complete overlap
            for region_below in reversed(canvas.all_regions):
                # Do test_ray circuit for top and bottom.
                # Start test_point on top, then do test_point on bottom

                # Note that this gets boolean values for test vertices (arg 1) in ref polygon (arg 0)
                inside_flags_bottom_test = test_vertices_in_ref(self, region_below)
                inside_flags_top_test = test_vertices_in_ref(region_below, self)

                # Intersections. The rays here are top region rays (for visibility)
                regional_intersections = 0
                for bottom_ray in region_below.rays:
                    new_intersections = canvas.find_intersections(bottom_ray, self.get_all_rays())
                    regional_intersections += new_intersections['number']

                # Region below is completely inside region above if:
                # 1. All region below vertices are inside region above
                # 2. All region above vertices are outside region below
                if all(inside_flags_bottom_test) and not any(inside_flags_top_test):
                    # Region below is completely inside region above. Ignore it!
                    pass

                # Region below is completely outside region above if:
                # 1. All region below vertices are outside region above
                # 2. No intersection of region rays
                elif not any(inside_flags_bottom_test) and regional_intersections == 0:
                    pass

                # Region below is partially inside region above if:
                # 1. Mix of region below vertices inside/outside
                else:
                    pass

                test = 1

                pass

                # Overlap_all check?

                # Complete overlap: Ignore overlapped region. Add none to top_level
                # Partial overlap: Check intersections
                # No overlap: Add all.

                # All rays of -1 (current) region are valid. Add to top_level
                # Test -2 rays for intersection with -1
                # Test -3 rays for intersection with -2 and -1
                # ...  -n                       with (-n + 1) to -1

        # All that's needed is a region with all rays.
        self.name = 'region' + str(len(canvas.all_regions))
        region_rays = self.get_all_rays()

        finish_angles()

        finish_area()

        finish_polygon()

        finish_refractive_index()

        finish_layer_order()

        test = 1

class ray(object):

    def __init__(self):
        self.p0 = None
        self.p1 = None
        self.t0 = 0
        self.t1 = None
        self.v = None
        self.name = None
        self.angle = None
        pass

    def set_p0(self, p0_input):
        self.p0 = p0_input

    def set_p1(self, p1_input):
        self.p1 = p1_input

    def set_t0(self, t0_input):
        self.t0 = t0_input

    def set_t1(self, t1_input):
        self.t1 = t1_input

    def set_v(self, v_input):
        self.v = v_input

    def set_name(self, name_input):
        self.name = name_input

    def set_angle(self, angle_input):
        self.angle = angle_input

    def get_p0(self):
        return self.p0

    def get_p1(self):
        return self.p1

    def get_t0(self):
        return self.t0

    def get_t1(self):
        return self.t1

    def get_v(self):
        return self.v

    def get_name(self):
        return self.name

    def get_angle(self):
        return self.angle

    def finish_ray(self):
        v_new = self.get_p1() - self.get_p0()
        t1_new = np.linalg.norm(v_new)
        self.set_t1(t1_new)
        self.set_v(v_new / t1_new)
        self.set_angle(canvas.CCW_angle(np.array([1, 0]), self.get_v()))

def test_enter_cmd():
    test = 1
    pass

def setup_cmd():
    pass

def pause_cmd():
    test = 1
    pass

def start_cmd():
    pass

root = tk.Tk()
root.title('Ray Tracer')

canvas_width = 500
canvas_height = 500
canvas = ray_canvas(root, width=canvas_width, height=canvas_height, bd=0)

position_text = canvas.create_text(2, canvas_height, anchor=tk.SW, text='Hello')

canvas.grid(row=0, column=0, columnspan=4)

setup_button = tk.Button(root, text='Create shapes', command=setup_cmd)
pause_button = tk.Button(root, text='Pause', command=pause_cmd)
start_button = tk.Button(root, text='Start Raytracing', command=start_cmd)
quit_button = tk.Button(root, text='Quit', command=sys.exit)

setup_button.grid(row=1, column=0)
pause_button.grid(row=1, column=1)
start_button.grid(row=1, column=2)
quit_button.grid(row=1, column=3)

tk.mainloop()