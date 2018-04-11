from matplotlib import pyplot as plt
from timeit import Timer
import tree
import tree_np
from argparse import ArgumentParser


def plot_performance(max_level, num_runs=5):
    tree_levels = range(max_level+1)
    tree_args = tree.parse_args()
    run_times = []
    run_times_np = []
    for level in tree_levels:
        tree_args.levels = level
        t = Timer(lambda: tree.command(tree_args))
        t_np = Timer(lambda: tree_np.command_np(tree_args))
        run_times.append(t.timeit(number=num_runs))
        run_times_np.append(t_np.timeit(number=num_runs))

    plt.plot(tree_levels, run_times, '-rx', tree_levels, run_times_np, '-bo')
    plt.legend(['Run times with .append implementation', 'Run times with numpy implementation'])
    plt.xlabel('Number of tree levels')
    plt.ylabel('Run time')
    plt.title('Run time performance comparison for building trees')
    plt.xlim(-1, max_level+1)
    plt.show()


if __name__ == "__main__":
    parser = ArgumentParser(description="Plot performance of tree building")
    parser.add_argument("-l", "--max_level", help="Highest tree level", default=12, type=int)
    parser.add_argument("-r", "--num_runs", help="Number of timeit runs to perform", default=5, type=int)
    args = parser.parse_args()
    plot_performance(args.max_level, args.num_runs)
