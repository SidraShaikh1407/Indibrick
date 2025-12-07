import tkinter as tk
from tkinter import *
from tkinter import messagebox

def label_example():
    root = tk.Tk()
    tk.Label(root, text="Hello Tkinter!").pack()
    root.mainloop()

def image_label_example():
    root = tk.Tk()
    logo = tk.PhotoImage(file="python_logo_small.gif")
    tk.Label(root, image=logo).pack(side="right")
    explanation = """At present, only GIF and PPM/PGM formats are supported."""
    tk.Label(root, justify=tk.LEFT, padx=10, text=explanation).pack(side="left")
    root.mainloop()

def button_example():
    def write_slogan():
        print("Tkinter is easy to use!")

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    button = tk.Button(frame, text="QUIT", fg="red", command=root.quit)
    button.pack(side=tk.LEFT)
    slogan = tk.Button(frame, text="Hello", command=write_slogan)
    slogan.pack(side=tk.LEFT)
    root.mainloop()

def radio_button_example():
    root = tk.Tk()
    v = tk.IntVar()
    v.set(1)
    languages = [("Python", 1), ("Java", 2), ("C++", 3), ("C", 4)]
    
    def show_choice():
        print(f"Selected: {v.get()}")
    
    tk.Label(root, text="Choose your language:", padx=20).pack()
    
    for text, value in languages:
        tk.Radiobutton(root, text=text, padx=20, variable=v, command=show_choice, value=value).pack(anchor=tk.W)
    
    root.mainloop()

def checkbox_example():
    master = Tk()
    var1 = IntVar()
    var2 = IntVar()
    
    Checkbutton(master, text="Male", variable=var1).grid(row=0, sticky=W)
    Checkbutton(master, text="Female", variable=var2).grid(row=1, sticky=W)
    
    Button(master, text='Quit', command=master.quit).grid(row=2, sticky=W, pady=4)
    master.mainloop()

def show_menu():
    while True:
        print("\n1. Label Example")
        print("2. Image in Label Example")
        print("3. Button Example")
        print("4. Radio Button Example")
        print("5. Checkbox Example")
        print("6. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            label_example()
        elif choice == 2:
            image_label_example()
        elif choice == 3:
            button_example()
        elif choice == 4:
            radio_button_example()
        elif choice == 5:
            checkbox_example()
        elif choice == 6:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    show_menu()
