from argparse import ArgumentParser
from matplotlib import pyplot as plt
import numpy as np


def build_tree_np(levels, angle_change, length, length_change, plot_tree):
    branches = initialise_tree_np(length, plot_tree)
    count = 0
    while count < levels:
        extend_tree_plus = extend_branch_np(branches, length, angle_change, plot_tree)
        extend_tree_minus = extend_branch_np(branches, length, -angle_change, plot_tree)
        branches = np.hstack((extend_tree_plus, extend_tree_minus))
        length *= length_change
        count += 1
    if plot_tree:
        plt.show()
        # plt.savefig('tree_np.png')


def initialise_tree_np(length, plot_tree):
    new_branches = np.array([0, length, 0], dtype=float)
    plot_branches_np(np.array([0, 0, 0]), new_branches, plot_tree)
    return new_branches


def extend_branch_np(branches, length, angle_change, plot_tree):
    new_branches = np.copy(branches)
    new_angle = branches[2::3] + angle_change
    new_branches[::3] = branches[::3] + length * np.sin(new_angle)
    new_branches[1::3] = branches[1::3] + length * np.cos(new_angle)
    new_branches[2::3] = new_angle
    plot_branches_np(branches, new_branches, plot_tree)
    return new_branches


def plot_branches_np(branches, new_branches, plot_tree):
    if plot_tree:
        branches_reshape = np.reshape(branches, (int(len(new_branches) / 3), 3))
        new_branches_reshape = np.reshape(new_branches, (int(len(new_branches) / 3), 3))
        for i in range(branches_reshape.shape[0]):
            plt.plot([branches_reshape[i][0], new_branches_reshape[i][0]],
                     [branches_reshape[i][1], new_branches_reshape[i][1]])


def parse_args_np():
    parser = ArgumentParser(description="Build a tree")
    parser.add_argument("--levels", help="Number of tree levels above trunk", default=5, type=int)
    parser.add_argument("--angle_change", help="Increment / decrement to angle of branches", default=0.2, type=float)
    parser.add_argument("--length", help="Tree branch length", default=1, type=float)
    parser.add_argument("--length_change", help="Change in branch length after each level", default=0.6, type=float)
    parser.add_argument("-p", "--plot_tree", help="Flag to turn plotting on/off", action='store_true')
    return parser.parse_known_args()[0]


def command_np(args):
    build_tree_np(args.levels, args.angle_change, args.length, args.length_change,args.plot_tree)


if __name__ == "__main__":
    command_np(parse_args_np())
