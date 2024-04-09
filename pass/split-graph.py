import os
import pandas as pd
import uuid
import matplotlib.pyplot as plt
from tkinter import Tk, simpledialog, filedialog

def select_directories():
    root = Tk()
    root.withdraw()
    num_directories = simpledialog.askinteger("入力", "読み込むディレクトリの数を入力してください:")
    directories = []
    for i in range(num_directories):
        directory = filedialog.askdirectory(title=f"ディレクトリ{i+1}を選択")
        if directory:
            directories.append((directory, os.path.basename(directory)))
    root.destroy()
    return directories

def get_user_input():
    root = Tk()
    root.withdraw()
    x_label = simpledialog.askstring("入力", "x軸のラベルを入力してください:")
    y_label = simpledialog.askstring("入力", "y軸のラベルを入力してください:")
    title = simpledialog.askstring("入力", "グラフのタイトルを入力してください:")
    root.destroy()
    return x_label, y_label, title

def select_csv_files(num_files):
    root = Tk()
    root.withdraw()
    csv_files = []
    for i in range(num_files):
        csv_file = filedialog.askopenfilename(title=f"CSVファイル{i+1}を選択してください", filetypes=[("CSV files", "*.csv")])
        if csv_file:
            csv_files.append(csv_file)
    root.destroy()
    return csv_files

def enter_folder_name():
    root = Tk()
    root.withdraw()
    folder_name = simpledialog.askstring("入力", "フォルダー名を入力してください:")
    root.destroy()
    return folder_name

def main():
    operation_type = simpledialog.askinteger("選択", "行いたい操作を選択してください（1: CSVファイルの分割, 2: グラフのプロット）:")
    if operation_type not in [1, 2]:
        print("無効な操作が選択されました。")
        return

    if operation_type == 1:
        # CSVファイルの分割を行う
        num_files = simpledialog.askinteger("入力", "分割したいCSVファイルの数を入力してください:")
        if not num_files:
            print("数が入力されていません。")
            return

        folder_name = enter_folder_name()
        if not folder_name:
            print("フォルダー名が入力されていません。")
            return

        save_folder = os.path.join(os.getcwd(), folder_name)
        os.makedirs(save_folder, exist_ok=True)

        csv_files = select_csv_files(num_files)
        if not csv_files:
            print("CSVファイルが選択されていません。")
            return

        for csv_file in csv_files:
            data = pd.read_csv(csv_file, dtype={'n': int})

            blocks = []
            current_block = []
            for index, row in data.iterrows():
                if row['n'] == 0:
                    if current_block:
                        blocks.append(current_block)
                        current_block = []
                    current_block.append({'μ': row['μ'], 'n': row['n']})
                else:
                    current_block.append(row)

            if current_block:
                blocks.append(current_block)

            for i, block in enumerate(blocks):
                block_df = pd.DataFrame(block)
                file_name = f'n_zero_data_{uuid.uuid4()}.csv'
                file_path = os.path.join(save_folder, file_name)
                block_df.to_csv(file_path, index=False)

        print(f"フォルダー '{folder_name}' にファイルが正常に保存されました。")

    elif operation_type == 2:
        # グラフのプロットを行う
        directories = select_directories()

        x_label, y_label, title = get_user_input()

        if directories and x_label and y_label and title:
            plot_graph(directories, x_label, y_label, title, figsize=(12, 10), fontsize=24)
        else:
            print("有効な入力をしてください。")

def plot_graph(directories, x_label='n', y_label='μ', title='ディレクトリの比較', figsize=(10, 8), fontsize=24):
    plt.figure(figsize=figsize)
    
    dfs_list = []
    for directory, _ in directories:
        file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
        dfs = [pd.read_csv(file) for file in file_paths]
        dfs_list.append(dfs)

    μ_averages = []
    for dfs in dfs_list:
        μ_values = [df['μ'] for df in dfs]
        μ_average = sum(μ_values) / len(μ_values)
        μ_averages.append(μ_average)

    n_values = dfs_list[0][0]['n']

    for (directory, label), μ_average in zip(directories, μ_averages):
        plt.plot(n_values, μ_average, label=label)

    plt.xlabel(x_label, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)
    plt.title(title, fontsize=fontsize+4, fontweight='bold')
    plt.ylabel(y_label, fontsize=fontsize, rotation=0, labelpad=20)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()