from sys import argv, exit

def center_of_gravity_1D(points):
    moments = []
    for point in points:
        moments.append(point[0]*point[1])
    moment_sum = sum(moments)
    weight_sum = sum([w for d,w in points])
    cg = moment_sum / weight_sum
    return cg

def center_of_gravity_3D(points):
    x_cg = center_of_gravity_1D([(x,w) for (x,y,z),w in points])
    y_cg = center_of_gravity_1D([(y,w) for (x,y,z),w in points])
    z_cg = center_of_gravity_1D([(z,w) for (x,y,z),w in points])
    return x_cg, y_cg, z_cg

def adjust_cg_with_obj_1D(curr_cg, curr_w, new_obj_w, desired_cg, desired_w):
    curr_m = curr_cg * curr_w
    want_m = (curr_w + new_obj_w) * desired_cg
    return (want_m - curr_m) / new_obj_w

def adjust_cg_with_obj_3D(curr_cg, curr_w, new_obj_w, desired_cg):
    desired_w = curr_w + new_obj_w
    x = adjust_cg_with_obj_1D(curr_cg[0], curr_w, new_obj_w, desired_cg[0], desired_w)
    y = adjust_cg_with_obj_1D(curr_cg[1], curr_w, new_obj_w, desired_cg[1], desired_w)
    z = adjust_cg_with_obj_1D(curr_cg[2], curr_w, new_obj_w, desired_cg[2], desired_w)
    return x, y, z

cg_points = ()
cg_val = ()
total_weight = 0

def load_csv_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()[1:]
        points = []
        total_w = 0
        for line in lines:
            values = line.strip().split(',')[1:]
            x = float(values[0])
            y = float(values[1])
            z = float(values[2])
            w = float(values[3])
            total_w += w
            points.append( ((x,y,z), w) )
        global cg_points
        cg_points = points
        global total_weight
        total_weight = total_w

from cmd import Cmd
from os import path
from glob import glob

#Changes delims to allow file autocomplete
import readline
readline.set_completer_delims(' \t\n')

def complete_path(filename):
    if path.isdir(filename):
        return glob(path.join(filename, '*'))
    else:
        return glob(filename+'*')

class Cli(Cmd):
    def do_load(self, line):
       try:
           load_csv_file(line)
           global cg_val
           cg_val = center_of_gravity_3D(cg_points)
       except Exception as e:
            print(e)

    def do_cg(self, line):
        print(cg_val)

    def do_adjust_cg_with_obj(self, line):
        params = line.split()
        if len(params) != 4:
            print('4 parmaters needed: [new_object weight] [desired cg_x] [desired cg_y] [desired cg_z]')
            return
        obj_w = float(params[0])
        new_cg = tuple(float(i) for i in params[1:])
        obj_pos = adjust_cg_with_obj_3D(cg_val, total_weight, obj_w, new_cg)
        print("The object should be placed at: " + str(obj_pos) + " to have a cg of " + str(new_cg))

    def complete_load(self, text, line, begidx, endidx):
        return complete_path(text)

    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return True

cli = Cli()
cli.prompt = '(cg-tool) '
cli.cmdloop()
