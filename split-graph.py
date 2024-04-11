import os
import pandas as pd
import uuid
from tkinter import Tk, filedialog, simpledialog

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

def split_function():
    # ユーザーにCSVファイルの数を入力してもらう
    num_files = simpledialog.askinteger("入力", "分割したいCSVファイルの数を入力してください:")
    if not num_files:
        print("数が入力されていません。")
        return

    # ユーザーにフォルダー名を入力してもらう
    folder_name = enter_folder_name()
    if not folder_name:
        print("フォルダー名が入力されていません。")
        return

    # 新しいフォルダーを作成し、保存先のパスを取得
    save_folder = os.path.join(os.getcwd(), folder_name)
    os.makedirs(save_folder, exist_ok=True)

    # ユーザーにCSVファイルを選択してもらう
    csv_files = select_csv_files(num_files)
    if not csv_files:
        print("CSVファイルが選択されていません。")
        return

    # 選択されたCSVファイルをそれぞれ分割して保存
    for csv_file in csv_files:
        # CSVファイルを読み込む際にn列のデータ型を整数型に指定して読み込む
        data = pd.read_csv(csv_file, dtype={'n': int})

        # nが0の行を検出して、ブロックごとに分割
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

        # 最後のブロックを追加
        if current_block:
            blocks.append(current_block)

        # ブロックごとにCSVファイルに保存
        for i, block in enumerate(blocks):
            block_df = pd.DataFrame(block)
            # UUIDを使用してファイル名を生成
            file_name = f'n_zero_data_{uuid.uuid4()}.csv'
            file_path = os.path.join(save_folder, file_name)
            block_df.to_csv(file_path, index=False)
    
    print(f"フォルダー '{folder_name}' にファイルが正常に保存されました。")

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

def graph_create_function():
    directories = select_directories()

    x_label, y_label, title = get_user_input()

    if directories and x_label and y_label and title:
        plot_graph(directories, x_label, y_label, title, figsize=(12, 10), fontsize=24)
    else:
        print("有効な入力をしてください.")

if __name__ == "__main__":
    split_function()
    graph_create_function()