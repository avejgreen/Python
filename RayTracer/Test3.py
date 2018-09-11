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

    def find_intersections(self, test_ray, lines, first_only=False):

        intersection_times = []
        intersection_rays = []
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

                if (t[0] >= 0 and t[0] <= test_ray.get_t1()) and \
                        (-t[1] >= 0 and -t[1] <= test_line.get_t1()):
                    intersection_times.append(t[0])
                    intersection_rays.append(test_line_number)

        if len(intersection_times) > 0:
            if first_only:
                first_int_t = min(intersection_times)
                return test_ray.get_p0() + first_int_t * test_ray.get_v()
            else:
                intersection_points = []
                for t1 in intersection_times:
                    intersection_points.append(test_ray.get_p0() + t1 * test_ray.get_v())
                return [intersection_rays, intersection_times, intersection_points]
        else:
            return None

    def motion_func(self, event):

        started_flag = self.region_started_flag
        new_point = np.array([event.x, event.y])
        canvas.itemconfigure(position_text, text=str(event.x) + ',' + str(event.y))

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
                if first_intersection is not None:
                    canvas.coords(line_tag, p0[0], p0[1], first_intersection[0], first_intersection[1])
                elif t_node0 < self.node0_distance:
                    canvas.coords(line_tag, p0[0], p0[1], node0[0], node0[1])
                else:
                    canvas.coords(line_tag, p0[0], p0[1], event.x, event.y)

            if len(new_region_rays) < 2:
                first_intersection = None
            else:
                # If there's an intersection, only draw line up to it.
                temp_ray = new_region_rays[-1]
                temp_ray.set_p1(new_point)
                temp_ray.finish_ray()
                first_intersection = self.find_intersections(temp_ray, new_region_rays[:-2], True)

            draw_full_ray()

    def button_func(self, event):
        # Get the new point.
        started_flag = canvas.region_started_flag
        new_point = np.array([event.x, event.y])
        new_region_rays = []        # Just a holder for global user in make_new_ray. Will redefine
                                    # according to conditional.

        def make_new_ray(point):
            # Simple create ray. But need to know which number ray in which region
            # Once ray is created, draw it on the canvas and return it.
            new_ray = ray()
            new_ray.set_p0(point)
            new_ray.set_name('region' + str(len(self.all_regions)) +
                             '_ray' + str(len(new_region_rays)))
            canvas.create_line(event.x, event.y, event.x, event.y,
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
        # All that's needed is a region with all rays.

        self.name = 'region' + str(len(canvas.all_regions))

        # First, figure out inside/outside by checking angles
        # Inside has total angle sum(i) = 180*(n-2)
        # Outside has total angle sum(360-i) = 360*n - 180*(n-2)
        #                                    = 180*(n+2)
        # Get oriented angles with cross product:
        # sin(q) = cross(a,b)       because vectors are unit velocity
        # in 2D, no other complications needed - sign gives +CCW / -CW
        region_rays = self.get_all_rays()
        inside_angles = []
        inside_angles_helper = []
        sin_angles = []
        cos_angles = []

        for i in range(self.get_num_rays()):
            v_0 = region_rays[i].get_v()
            v_1 = region_rays[(i + 1) % self.get_num_rays()].get_v()

            new_cos_angle = np.dot(-v_0, v_1)
            new_cos_angle = np.arccos(new_cos_angle)
            cos_angles.append(new_cos_angle)

            new_sin_angle = np.cross(-v_0, v_1)
            new_sin_angle = np.arcsin(new_sin_angle)
            sin_angles.append(new_sin_angle)

            # Note: acos range is from 0 to pi
            # Note: asin range is from -pi/2 to pi/2
            # ---> Flipped because of coordinate system???
            if new_sin_angle > 0:
                inside_angles.append(2 * np.pi - new_cos_angle)
                inside_angles_helper.append((2 * np.pi - new_cos_angle) / np.pi)
            else:
                inside_angles.append(new_cos_angle)
                inside_angles_helper.append(new_cos_angle / np.pi)

        # Find inside. Check if sum within 1 degree of expected
        CCW_sum = sum(inside_angles) * 180 / np.pi
        inside_angle_sum = 180 * (self.get_num_rays() - 2)
        if CCW_sum > inside_angle_sum - 1 and CCW_sum < inside_angle_sum + 1:
            # CCW angles are inside
            # These angles are drawn from ray i to ray i+1 in the given rotation direction
            self.set_inside_direction('CCW')
            self.set_inside_angles(inside_angles)
        else:
            self.set_inside_direction('CW')
            for i in range(len(inside_angles)):
                inside_angles[i] = 2 * np.pi - inside_angles[i]
            self.set_inside_angles(inside_angles)

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
            if intersections is None:
                pass
            elif len(intersections[0]) % 2 == 0:
                for i in range(int(len(intersections[0])/2)):
                    area += intersections[1][2*i+1] - intersections[1][2*i] + 1

        self.set_area(area)

        # Replace with a filled polygon
        region_p0s = []
        for i in region_rays:
            region_p0s.append([i.p0[0], i.p0[1]])
            canvas.delete(i.get_name())
        new_polygon = canvas.create_polygon(region_p0s,
                                            fill=self.colors[len(canvas.all_regions)],
                                            outline='black',
                                            tags=self.name)
        self.polygon = new_polygon

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

class ray(object):

    def __init__(self):
        self.p0 = None
        self.p1 = None
        self.t0 = 0
        self.t1 = None
        self.v = None
        self.name = None
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

    def finish_ray(self):
        v_new = self.get_p1() - self.get_p0()
        t1_new = np.linalg.norm(v_new)
        self.set_t1(t1_new)
        self.set_v(v_new / t1_new)

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

# if __name__ == '__main__':

root = tk.Tk()
root.title('Ray Tracer')

canvas_width = 500
canvas_height = 500
canvas = ray_canvas(root, width=canvas_width, height=canvas_height)

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