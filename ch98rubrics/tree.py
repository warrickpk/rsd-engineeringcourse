from math import sin, cos
from matplotlib import pyplot as plt
from argparse import ArgumentParser


def build_tree(levels, angle_change, length, length_change, plot_tree):
    branches = initialise_tree(length, plot_tree)
    count = 0
    while count < levels:
        branches = extend_tree(branches, length, angle_change, plot_tree)
        length *= length_change
        count += 1
    if plot_tree:
        plt.show()
        # plt.savefig('tree.png')


def initialise_tree(length, plot_tree):
    new_branch = [0, length, 0]
    plot_branches([0, 0, 0], new_branch, plot_tree)
    return [new_branch]


def extend_tree(branches, length, angle_change, plot_tree):
    new_branches = []
    for branch in branches:
        for angle in [-angle_change, angle_change]:
            new_branches.append(extend_branch(branch, length, angle, plot_tree))
    return new_branches


def extend_branch(branch, length, angle_change, plot_tree):
    x_coord = branch[0] + length * sin(branch[2] + angle_change)
    y_coord = branch[1] + length * cos(branch[2] + angle_change)
    new_angle = branch[2] + angle_change
    new_branch = [x_coord, y_coord, new_angle]
    plot_branches(branch, new_branch, plot_tree)
    return new_branch


def plot_branches(branch, new_branch, plot_tree):
    if plot_tree:
        plt.plot([branch[0], new_branch[0]], [branch[1], new_branch[1]])


def parse_args():
    parser = ArgumentParser(description="Build a tree")
    parser.add_argument("--levels", help="Number of tree levels above trunk", default=5, type=int)
    parser.add_argument("--angle_change", help="Increment / decrement to angle of branches", default=0.2, type=float)
    parser.add_argument("--length", help="Tree branch length", default=1, type=float)
    parser.add_argument("--length_change", help="Change in branch length after each level", default=0.6, type=float)
    parser.add_argument("-p", "--plot_tree", help="Flag to turn plotting on/off", action='store_true')
    return parser.parse_known_args()[0]


def command(args):
    build_tree(args.levels, args.angle_change, args.length, args.length_change, args.plot_tree)


if __name__ == "__main__":
    command(parse_args())
