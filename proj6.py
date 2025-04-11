import tkinter as tk
from tkinter import ttk, messagebox
import time

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Sorting Algorithms Visualizer and Comparator")

# Dynamically adjust window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.6)
root.geometry(f"{window_width}x{window_height}")
root.configure(bg="#f0f0f0")

data = []
swap_count = 0

# Function to display step information in the Tkinter label
def update_step_label(step_label):
    time_label.config(text=step_label)
    root.update_idletasks()
    time.sleep(0.5)  # Slower to observe sorting

# Sorting Algorithm Implementations
def bubble_sort(data):
    global swap_count
    for i in range(len(data) - 1):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swap_count += 1
            update_step_label(f"Bubble Sort - Step: Swap {data[j]} and {data[j + 1]}")
            draw_data(data, "lightblue", j, j + 1)
    update_step_label("Bubble Sort Completed")

def selection_sort(data):
    global swap_count
    for i in range(len(data)):
        min_index = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_index]:
                min_index = j
        if i != min_index:
            data[i], data[min_index] = data[min_index], data[i]
            swap_count += 1
        update_step_label(f"Selection Sort - Step: Swap {data[i]} with min {data[min_index]}")
        draw_data(data, "lightgreen", i, min_index)
    update_step_label("Selection Sort Completed")

def insertion_sort(data):
    global swap_count
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
            swap_count += 1
        data[j + 1] = key
        update_step_label(f"Insertion Sort - Step: Insert {key} at position {j + 1}")
        draw_data(data, "orange", j + 1, i)
    update_step_label("Insertion Sort Completed")

def merge_sort(data):
    merge_sort_helper(data, 0, len(data) - 1)

def merge_sort_helper(data, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_helper(data, left, mid)
        merge_sort_helper(data, mid + 1, right)
        merge(data, left, mid, right)

def merge(data, left, mid, right):
    left_copy = data[left:mid + 1]
    right_copy = data[mid + 1:right + 1]
    left_cursor, right_cursor = 0, 0
    sorted_cursor = left

    while left_cursor < len(left_copy) and right_cursor < len(right_copy):
        if left_copy[left_cursor] <= right_copy[right_cursor]:
            data[sorted_cursor] = left_copy[left_cursor]
            left_cursor += 1
        else:
            data[sorted_cursor] = right_copy[right_cursor]
            right_cursor += 1
        update_step_label(f"Merging at position {sorted_cursor}")
        draw_data(data, "lightyellow", sorted_cursor, None)
        sorted_cursor += 1

    while left_cursor < len(left_copy):
        data[sorted_cursor] = left_copy[left_cursor]
        left_cursor += 1
        sorted_cursor += 1

    while right_cursor < len(right_copy):
        data[sorted_cursor] = right_copy[right_cursor]
        right_cursor += 1
        sorted_cursor += 1

def quick_sort(data):
    quick_sort_helper(data, 0, len(data) - 1)

def quick_sort_helper(data, low, high):
    if low < high:
        pivot_index = partition(data, low, high)
        quick_sort_helper(data, low, pivot_index - 1)
        quick_sort_helper(data, pivot_index + 1, high)

def partition(data, low, high):
    global swap_count
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            swap_count += 1
            update_step_label(f"Quick Sort - Step: Swap {data[i]} and {data[j]} with pivot {pivot}")
            draw_data(data, "pink", i, j)
    data[i + 1], data[high] = data[high], data[i + 1]
    swap_count += 1
    update_step_label(f"Quick Sort - Step: Move pivot {pivot} to position {i + 1}")
    draw_data(data, "lightcoral", i + 1, None)
    return i + 1

def start_sorting():
    global data, swap_count
    choice = sort_choice.get()
    swap_count = 0

    if choice == "Single Algorithm":
        algorithm = algorithm_menu.get()
        start_time = time.time()

        if algorithm == "Bubble Sort":
            bubble_sort(data)
        elif algorithm == "Selection Sort":
            selection_sort(data)
        elif algorithm == "Insertion Sort":
            insertion_sort(data)
        elif algorithm == "Merge Sort":
            merge_sort(data)
        elif algorithm == "Quick Sort":
            quick_sort(data)

        end_time = time.time()
        draw_data(data)
        time_label.config(text=f"{algorithm} Completed in {end_time - start_time:.4f} seconds")
        result_label.config(
            text=f"Sorted Array: {data}\nSwap Count: {swap_count if algorithm != 'Merge Sort' else 'N/A'}"
        )

    elif choice == "All Algorithms Comparison":
        algorithms = [
            ("Bubble Sort", bubble_sort),
            ("Selection Sort", selection_sort),
            ("Insertion Sort", insertion_sort),
            ("Merge Sort", merge_sort),
            ("Quick Sort", quick_sort)
        ]
        time_text = ""

        for name, algo in algorithms:
            temp_data = data.copy()
            swap_count = 0
            start_time = time.time()
            algo(temp_data)
            end_time = time.time()
            time_text += f"{name}: {end_time - start_time:.4f}s, Swaps: {swap_count if name != 'Merge Sort' else 'N/A'}\n"

        time_label.config(text=time_text)
        result_label.config(text=f"Final Sorted Array: {sorted(data)}")

def input_array():
    global data
    data_str = array_entry.get()
    try:
        data = list(map(int, data_str.split(',')))
        messagebox.showinfo("Input Successful", f"Array is set to: {data}")
        draw_data(data)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a comma-separated list of integers.")

def draw_data(data, highlight_color=None, highlight_idx1=None, highlight_idx2=None):
    canvas.delete("all")
    bar_width = window_width / len(data) * 0.8 if data else 1
    for i, value in enumerate(data):
        x0 = i * bar_width + (window_width - len(data) * bar_width) / 2
        y0 = window_height * 0.8 - value * 5
        x1 = x0 + bar_width
        y1 = window_height * 0.8

        color = "blue"
        if highlight_idx1 == i or highlight_idx2 == i:
            color = highlight_color if highlight_color else "red"

        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(value), font=("Arial", 10), fill="black")

font_size = int(window_height * 0.03)
button_font = ("Arial", int(window_height * 0.025), "bold")

greeting_label = tk.Label(root, text="Hello! Enter an array to sort and choose sorting options below.", font=("Arial", font_size), bg="#f0f0f0")
greeting_label.grid(row=0, column=0, columnspan=3, pady=int(window_height * 0.02), sticky="ew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)

array_entry = tk.Entry(root, width=int(window_width * 0.9), font=("Arial", int(window_height * 0.035)))
array_entry.grid(row=1, column=0, padx=int(window_width * 0.01), pady=int(window_height * 0.02), sticky="ew")

input_button = tk.Button(root, text="Set Array", command=input_array, width=15, height=2, font=button_font)
input_button.grid(row=1, column=1, padx=int(window_width * 0.01))

sort_choice = tk.StringVar(value="Single Algorithm")
sort_frame = tk.Frame(root, bg="#f0f0f0")
sort_frame.grid(row=2, column=0, columnspan=3, pady=int(window_height * 0.02), sticky="ew")

single_algo_radio = tk.Radiobutton(sort_frame, text="Single Algorithm", variable=sort_choice, value="Single Algorithm", bg="#f0f0f0")
single_algo_radio.pack(side="left", padx=(0, 10))

all_algo_radio = tk.Radiobutton(sort_frame, text="All Algorithms Comparison", variable=sort_choice, value="All Algorithms Comparison", bg="#f0f0f0")
all_algo_radio.pack(side="left")

algorithm_menu = ttk.Combobox(root, values=["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"], state="readonly")
algorithm_menu.set("Choose Sorting Algorithm")
algorithm_menu.grid(row=3, column=0, padx=int(window_width * 0.01), pady=int(window_height * 0.02), sticky="ew")

start_button = tk.Button(root, text="Start Sorting", command=start_sorting, width=15, height=2, font=button_font)
start_button.grid(row=3, column=1, padx=int(window_width * 0.01))

time_label = tk.Label(root, text="", font=("Arial", int(window_height * 0.025)), bg="#f0f0f0")
time_label.grid(row=4, column=0, columnspan=3, pady=int(window_height * 0.02), sticky="ew")

result_label = tk.Label(root, text="", font=("Arial", int(window_height * 0.025)), bg="#f0f0f0")
result_label.grid(row=5, column=0, columnspan=3, pady=int(window_height * 0.02), sticky="ew")

canvas = tk.Canvas(root, width=window_width, height=int(window_height * 0.9), bg="#ffffff")
canvas.grid(row=6, column=0, columnspan=3, pady=int(window_height * 0.02), sticky="ew")

root.mainloop()
