import tkinter as tk
from tkinter import ttk


def show_edit_popup(entries):
    root = tk.Tk()
    root.title("Review & Edit Timesheet Entries")

    sample = entries[0]
    fields = list(vars(sample).keys())

    tree = ttk.Treeview(root, columns=fields, show="headings")

    for f in fields:
        tree.heading(f, text=f)
        tree.column(f, width=150)

    # Insert data
    for e in entries:
        tree.insert("", tk.END, values=[getattr(e, f) for f in fields])

    tree.pack(fill=tk.BOTH, expand=True)

    # -----------------------------
    # Editable Cell Logic
    # -----------------------------
    def on_double_click(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = tree.identify_row(event.y)
        col_id = tree.identify_column(event.x)

        col_index = int(col_id.replace("#", "")) - 1
        x, y, width, height = tree.bbox(row_id, col_id)

        value = tree.set(row_id, fields[col_index])

        editor = tk.Entry(root)
        editor.insert(0, value)
        editor.select_range(0, tk.END)
        editor.focus()

        editor.place(x=x, y=y + tree.winfo_y(), width=width, height=height)

        def save_edit(event):
            new_val = editor.get()
            tree.set(row_id, fields[col_index], new_val)
            editor.destroy()

        editor.bind("<Return>", save_edit)
        editor.bind("<FocusOut>", lambda e: editor.destroy())

    tree.bind("<Double-1>", on_double_click)

    # -----------------------------
    # Buttons
    # -----------------------------
    edited_entries = []

    def on_ok():
        for i, item in enumerate(tree.get_children()):
            values = tree.item(item)["values"]
            entry = entries[i]

            for idx, f in enumerate(fields):
                setattr(entry, f, values[idx])

            edited_entries.append(entry)

        root.destroy()

    def on_cancel():
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="OK", width=15, command=on_ok).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", width=15, command=on_cancel).pack(
        side=tk.LEFT, padx=5
    )

    root.mainloop()

    return edited_entries if edited_entries else None
