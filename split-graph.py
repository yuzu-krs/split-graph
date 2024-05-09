import os
import pandas as pd
import uuid
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, simpledialog, Label, Entry, Button, END
import tkinter as tk

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
    plt.title(title, fontsize=fontsize+4, fontweight='bold')  
    plt.ylabel(y_label, fontsize=fontsize, rotation=0, labelpad=20)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.grid(True)
    plt.show()

def select_file(label):
    filepath = filedialog.askopenfilename()
    label.config(text=filepath)
    return filepath

def process_files(file1_label, file2_label, output_entry, result_text):
    file1_path = file1_label.cget("text")
    file2_path = file2_label.cget("text")
    output_filename = output_entry.get()

    if file1_path and file2_path and output_filename:
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        df1_data = df1.drop(columns=['x'])
        df2_data = df2.drop(columns=['x'])

        result_data = df1_data.div(df2_data)
        result_data = result_data.round(6)

        result_df = pd.concat([df1['x'], result_data], axis=1)
        result_df = result_df[['y', 'x']]

        output_path = os.path.join(os.getcwd(), output_filename)

        result_df.to_csv(output_path, index=False)
        result_text.set("処理が完了しました。")  
        
def main():
    choice = simpledialog.askinteger("選択", "実行するプログラムを選択してください。\n1: ブロックごとにCSVファイルに保存\n2: ディレクトリの比較グラフをプロット\n3: csvファイルの割り算\n4: 表の自動生成")

    if choice == 1:
        csv_file = select_csv_file()
        if not csv_file:
            print("CSVファイルが選択されていません。")
            return

        folder_name = enter_folder_name()
        if not folder_name:
            print("フォルダー名が入力されていません。")
            return

        save_folder = os.path.join(os.getcwd(), folder_name)
        os.makedirs(save_folder, exist_ok=True)

        data = pd.read_csv(csv_file)

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

        if current_block:
            blocks.append(current_block)

        for i, block in enumerate(blocks):
            block_df = pd.DataFrame(block)
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
    
    elif choice == 3:
        root = tk.Tk()
        root.title("CSVファイル割り算")

        file1_frame = tk.Frame(root)
        file1_frame.pack(pady=10)
        file1_label = tk.Label(file1_frame, text="ファイル1を選択してください")
        file1_label.pack(side=tk.LEFT, padx=(10, 5))
        file1_button = tk.Button(file1_frame, text="参照", command=lambda: select_file(file1_label))
        file1_button.pack(side=tk.LEFT)

        file2_frame = tk.Frame(root)
        file2_frame.pack(pady=10)
        file2_label = tk.Label(file2_frame, text="ファイル2を選択してください")
        file2_label.pack(side=tk.LEFT, padx=(10, 5))
        file2_button = tk.Button(file2_frame, text="参照", command=lambda: select_file(file2_label))
        file2_button.pack(side=tk.LEFT)

        output_frame = tk.Frame(root)
        output_frame.pack(pady=10)
        output_label = tk.Label(output_frame, text="出力ファイル名を入力してください")
        output_label.pack(side=tk.LEFT, padx=(10, 5))
        output_entry = tk.Entry(output_frame)
        output_entry.pack(side=tk.LEFT)

        result_text = tk.StringVar()
        result_label = tk.Label(root, textvariable=result_text)
        result_label.pack()

        process_button = tk.Button(root, text="処理実行", command=lambda: process_files(file1_label, file2_label, output_entry, result_text))
        process_button.pack(pady=10)

        root.mainloop()
            
    elif choice==4:
        # Function to calculate averages and generate compact table image
        def calculate_and_generate():
            # Get input values from entry fields
            input_directory = directory_entry.get()
            column_x = column_x_entry.get()
            column_y = column_y_entry.get()

            # Dictionary to store sums and counts
            sums_left = {}
            sums_right = {}
            counts = {}

            # Process all CSV files in the input directory
            for filename in os.listdir(input_directory):
                if filename.endswith(".csv"):
                    with open(os.path.join(input_directory, filename), 'r') as file:
                        reader = csv.reader(file)
                        for i, row in enumerate(reader, 1):
                            if i not in sums_left:
                                sums_left[i] = 0
                                sums_right[i] = 0
                                counts[i] = 0
                            # Update sums
                            left_value = float(row[1])  # Reverse left and right values
                            right_value = float(row[0])
                            sums_left[i] += left_value
                            sums_right[i] += right_value
                            counts[i] += 1

            # Calculate averages
            averages_left = {key: round(sums_left[key] / counts[key], 6) for key in sums_left}  # Round to 6 decimal places
            averages_right = {key: round(sums_right[key] / counts[key], 6) for key in sums_right}  # Round to 6 decimal places

            # Create DataFrame
            df = pd.DataFrame({column_x: list(averages_left.values()), column_y: list(averages_right.values())})

            # Create plot
            plt.figure(figsize=(8, 6))
            table = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=['lightgray'] * len(df.columns))
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1.2, 1.2)
            for key, cell in table.get_celld().items():
                if key[0] == 0:
                    cell.set_linewidth(2)
            plt.axis('off')

            # Save and display image
            plt.savefig('compact_table.png', bbox_inches='tight', pad_inches=0, transparent=True)
            plt.show()
            # Function body as provided in the code snippet

        # Create Tkinter window
        root = Tk()
        root.title("Average Calculator")

        # Label and entry for input directory
        directory_label = Label(root, text="Input Directory:")
        directory_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        directory_entry = Entry(root, width=40)
        directory_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        directory_entry.insert(END, "./input_file_csv")

        # Button to browse for directory
        def browse_directory():
            directory = filedialog.askdirectory()
            directory_entry.delete(0, END)
            directory_entry.insert(END, directory)
        browse_button = Button(root, text="Browse", command=browse_directory)
        browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Label and entry for X column
        column_x_label = Label(root, text="Column X:")
        column_x_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        column_x_entry = Entry(root, width=20)
        column_x_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Label and entry for Y column
        column_y_label = Label(root, text="Column Y:")
        column_y_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        column_y_entry = Entry(root, width=20)
        column_y_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Button to trigger calculations
        calculate_button = Button(root, text="Calculate and Generate", command=calculate_and_generate)
        calculate_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Run Tkinter main loop
        root.mainloop()

if __name__ == "__main__":
    main()