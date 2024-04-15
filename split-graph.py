import os
import pandas as pd
import uuid
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, simpledialog

def select_csv_file():
    root = Tk()
    root.withdraw()
    csv_file = filedialog.askopenfilename(title="CSVファイルを選択", filetypes=[("CSVファイル", "*.csv")])
    root.destroy()
    return csv_file

def enter_folder_name():
    root = Tk()
    root.withdraw()
    folder_name = simpledialog.askstring("入力", "フォルダー名を入力してください:")
    root.destroy()
    return folder_name

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

def main():
    choice = simpledialog.askinteger("選択", "実行するプログラムを選択してください。\n1: ブロックごとにCSVファイルに保存\n2: ディレクトリの比較グラフをプロット")
    
    if choice == 1:
        # ユーザーにCSVファイルを選択してもらう
        csv_file = select_csv_file()
        if not csv_file:
            print("CSVファイルが選択されていません。")
            return

        # ユーザーにフォルダー名を入力してもらう
        folder_name = enter_folder_name()
        if not folder_name:
            print("フォルダー名が入力されていません。")
            return

        # 新しいフォルダーを作成し、保存先のパスを取得
        save_folder = os.path.join(os.getcwd(), folder_name)
        os.makedirs(save_folder, exist_ok=True)

        # CSVファイルを読み込む
        data = pd.read_csv(csv_file)

        # 最初のnの値でブロックを分割
        blocks = []
        current_block = []
        first_n_value = None
        for index, row in data.iterrows():
            if first_n_value is None:
                first_n_value = row['x']
            if row['x'] == first_n_value:
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            current_block.append(row)

        # 最後のブロックを追加
        if current_block:
            blocks.append(current_block)

        # ブロックごとにCSVファイルに保存
        for i, block in enumerate(blocks):
            block_df = pd.DataFrame(block)
            # UUIDを使用してファイル名を生成
            file_name = f'n_first_value_data_{uuid.uuid4()}.csv'
            file_path = os.path.join(save_folder, file_name)
            block_df.to_csv(file_path, index=False)

        print(f"フォルダー '{folder_name}' にファイルを保存しました。")

    elif choice == 2:
        directories = select_directories()

        x_label, y_label, title = get_user_input()

        if directories and x_label and y_label and title:
            plot_graph(directories, x_label, y_label, title, figsize=(12, 10), fontsize=24)
        else:
            print("有効な入力をしてください。")
    else:
        print("無効な選択です。")

def plot_graph(directories, x_label='x', y_label='y', title='ディレクトリの比較', figsize=(10, 8), fontsize=24):
    plt.figure(figsize=figsize)
    
    dfs_list = []
    for directory, _ in directories:
        file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
        dfs = [pd.read_csv(file) for file in file_paths]
        dfs_list.append(dfs)

    μ_averages = []
    for dfs in dfs_list:
        μ_values = [df['y'] for df in dfs]
        μ_average = sum(μ_values) / len(μ_values)
        μ_averages.append(μ_average)

    n_values = dfs_list[0][0]['x']

    for (directory, label), μ_average in zip(directories, μ_averages):
        plt.plot(n_values, μ_average, label=label)

    plt.xlabel(x_label, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)
    plt.title(title, fontsize=fontsize+4, fontweight='bold')  # タイトルのフォントサイズを大きくして太字に設定
    plt.ylabel(y_label, fontsize=fontsize, rotation=0, labelpad=20)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()