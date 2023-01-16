import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sn
from dtw import dtw,accelerated_dtw
import glob
import math
import os


def run_euclidean(ori_val, gen_val):
    euclidean = []
    for gen_item in gen_val:
        dist = (np.linalg.norm(ori_val - gen_item))
        euclidean.append(dist)

    euclidean2 = np.array(euclidean)
    euclidean_max = euclidean2.max()
    euclidean2 = euclidean2 / euclidean_max
    return euclidean2


def run_dtw(ori_val, gen_val, metric, figure_path):
    fontsize = 22
    matplotlib.rcParams.update({'font.size': fontsize})
    fig, axs = plt.subplots(2, 3, figsize=(27, 18))
    fig.suptitle('Dynamic Time Warping for ' + metric)
    min_paths = []

    for i in range(len(gen_val)):
        y = math.floor(i / 3)
        x = i % 3

        d, cost_matrix, acc_cost_matrix, path = accelerated_dtw(ori_val, gen_val[i], dist='euclidean')  # similarity measure between temporal sequences
        min_paths.append(d)
        axs[y, x].imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
        axs[y, x].plot(path[0], path[1], 'w')
        #  axs[y,x].set_title(f'dtw min path distance: {np.round(d,2)}', fontsize=fontsize)
        axs[y, x].set(xlabel='generated data run 1', ylabel='original data run 1')

    for ax in axs.flat:
        ax.set(xlabel='generated data', ylabel='original data')

    for ax in axs.flat:
        ax.label_outer()

    plt.tight_layout()
    plt.savefig(f'{figure_path}/dtw-{metric}.png')
    plt.show()

    min_pathss = np.array(min_paths)
    min_paths_max = min_pathss.max()
    min_pathss = min_pathss / min_paths_max
    return min_pathss


def run_correlations(ori, gen, metric, evaluation_path):
    fontsize = 18
    matplotlib.rcParams.update({'font.size': fontsize})

    correlations = ['pearson', 'spearman', 'kendall']
    results = []

    for_latex = ''

    for_latex += '\\begin{table}[htb]\n'

    for_latex += '\t\\centering\n'
    for_latex += '\t\\begin{tabular}{|l|l|'
    for gen_item in gen:
        for_latex += 'l|'
    for_latex += '}\n'

    for_latex += '\t\t\\hline\n'
    for_latex += '\t\t'
    i = 0
    for gen_item in gen:
        for_latex += ' & run ' + str(i)
        i += 1

    for_latex += '& overall \\\\ \\hline\n'

    for correl in correlations:
        current_results = []
        for_latex += '\t\t'
        for_latex += correl + ' & '
        for gen_item in gen:
            # overall_r = gen_item.corr().iloc[0,1]
            overall_r = ori.corrwith(gen_item, method=correl).iloc[0]
            for_latex += str(np.round(overall_r, 4)) + ' & '
            current_results.append(overall_r)
        results.append(current_results)
        for_latex += str(np.round(np.mean(current_results), 3))
        for_latex += '\\\\'
        for_latex += '\n'

    for_latex += '\t\t\\hline\n'
    for_latex += '\t\\end{tabular}\n'
    for_latex += '\t\\caption{Correlations for generated data for ' + metric.replace('_',
                                                                                     '\_') + ' based on LSTM model}\n'
    for_latex += '\t\\label{tab:correlations_lstm}\n'
    for_latex += '\\end{table}\n'

    with open(f"{evaluation_path}/table_{metric}.txt", "w") as text_file:
        text_file.write(for_latex)

    d = {'': [1, 2], 'col2': [3, 4]}
    d = {}
    i = 0
    for correl in correlations:
        d[correl] = results[i]
        i += 1

    df = pd.DataFrame(data=d)
    df = df.T
    df['overall'] = df.mean(axis=1)
    df.loc['mean'] = df.mean()
    # df['mean'] = df.mean(axis=0)

    # df = df.style.set_properties(**{'font-size': '13pt',})

    for_latex_2 = df.to_latex()

    with open(f"{evaluation_path}/table_df_{metric}.txt", "w") as text_file:
        text_file.write(for_latex_2)

    return df


def get_data(resampled, generated, metric):

    resampled_files = os.listdir(resampled)

    resampled_file_name = [s for s in resampled_files if metric in s][0]

    ori = pd.read_csv(resampled + resampled_file_name, header=None).drop([0], axis=1)

    length = len(os.listdir(generated + metric))  # number of files in the generated folder of a metric
    gen = []
    gen_val = []

    for gen_file in os.listdir(generated+metric):
        gen.append(pd.read_csv(f'{generated}/{metric}/{gen_file}', header=None).drop([0], axis=1))


    min = ori.shape[0]  # min number of rows in resampled or generated files for a metric
    for gen_item in gen:
        if gen_item.shape[0] < min:
            min = gen_item.shape[0]

    ori = ori[0:min]  #  slice the original resampled metric files, so it contains the min number of rows.
    ori_val = ori.interpolate().values  # Fill NaN values using an interpolation method

    for i in range(length):
        gen[i] = gen[i][0:min]
        gen_val.append(gen[i].interpolate().values)

    return ori, ori_val, gen, gen_val


def eval(resampled_path, generated_path, evaluation_path, figure_path, metric):
    # metric = metric.replace('/', '_')
    print('--- EVALUATION FOR', metric, '---')
    ori, ori_val, gen, gen_val = get_data(resampled_path, generated_path, metric)

    # print(ori)
    # print(ori_val)
    # print(gen)
    # print("genval:", gen_val)

    euclidean_result = run_euclidean(ori_val, gen_val)
    print('euclidean:', euclidean_result)
    with open(evaluation_path + '/euclidean_result', 'a') as file:
         file.write(metric + ': ' + str(euclidean_result) + '\n')

    dtw_result = run_dtw(ori_val, gen_val, metric, figure_path)
    print('dynamic time warping:', dtw_result)
    with open(evaluation_path + '/dtw_result', 'a') as file:
         file.write(metric + ': ' + str(dtw_result) + '\n')

    with open(evaluation_path + '/status', 'w') as file:
        file.write(metric + ' - correlations')
    corr_result = run_correlations(ori.copy(), gen, metric, evaluation_path)

    df_all = corr_result.copy()
    df_all = df_all.drop(['mean'], axis=0)
    df_all = df_all.drop(['overall'], axis=1)
    df_all.loc['euclidean'] = euclidean_result
    df_all.loc['dtw'] = dtw_result
    df_all = df_all.T

    plot = df_all.plot(figsize=(26,8),  lw=6, xlabel='run index', ylabel='value')
    plot.set_ylim(0,1.1)
    fig = plot.get_figure()
    plt.title('Correlations for each Run for ' + metric)
    fig.savefig(f'{figure_path}/corr-{metric}.png')
    # fig.savefig(f'{figure_path}/corr-{metric}.pdf')
    fig.show()

    df_all_corr = df_all.corr(method='pearson')

    fig, ax = plt.subplots(figsize=(26,17))

    sn.heatmap(df_all_corr, annot=True, ax=ax)
    plt.title('Heatmap for ' +  metric)
    fig.savefig(f'{figure_path}/heatmap-{metric}.png')
    # fig.savefig(f'{figure_path}/heatmap-{metric}.pdf')
    plt.show()
    print('\n\n\n\n')


def evaluate_run(log_csv_file_name):
    print("evaluating...")

    resampled_path = 'data/csvs/' + log_csv_file_name + '/resampled/'
    generated_path = 'data/csvs/' + log_csv_file_name + '/generated/'
    evaluation_path = 'data/csvs/' + log_csv_file_name + '/evaluation/'
    figure_path = 'data/csvs/' + log_csv_file_name + '/figures/'
    if not os.path.exists(evaluation_path):
        os.makedirs(evaluation_path)

    metrics = [m.split('_')[0] for m in os.listdir(resampled_path)]

    # clearing files
    with open(evaluation_path + '/euclidean_result', 'w') as file:
         file.write("")

    with open(evaluation_path + '/dtw_result', 'w') as file:
         file.write("")

    for metric in metrics:
        eval(resampled_path, generated_path, evaluation_path, figure_path, metric)