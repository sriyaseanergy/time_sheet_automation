import tkinter as tk
from tkinter import ttk


def show_edit_popup(entries):
    root = tk.Tk()
    root.title("Timesheet Editor")

    # Modern color scheme
    BG_COLOR = "#f5f7fa"
    HEADER_BG = "#ffffff"
    PRIMARY_COLOR = "#2563eb"
    HOVER_COLOR = "#1e40af"
    BORDER_COLOR = "#e5e7eb"
    TEXT_PRIMARY = "#1f2937"
    TEXT_SECONDARY = "#6b7280"

    root.configure(bg=BG_COLOR)

    # --- Modern Theme Configuration ---
    style = ttk.Style()
    style.theme_use("clam")

    # Configure Treeview for modern look
    style.configure(
        "Modern.Treeview",
        background="#ffffff",
        foreground=TEXT_PRIMARY,
        fieldbackground="#ffffff",
        borderwidth=0,
        relief="flat",
        rowheight=40,
        font=("Segoe UI", 10),
    )

    style.configure(
        "Modern.Treeview.Heading",
        background=HEADER_BG,
        foreground=TEXT_SECONDARY,
        borderwidth=0,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
    )

    style.map(
        "Modern.Treeview",
        background=[("selected", "#eff6ff")],
        foreground=[("selected", TEXT_PRIMARY)],
    )

    # Modern button styles
    style.configure(
        "Primary.TButton",
        background=PRIMARY_COLOR,
        foreground="#ffffff",
        borderwidth=0,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padding=(20, 10),
    )

    style.configure(
        "Secondary.TButton",
        background="#ffffff",
        foreground=TEXT_PRIMARY,
        borderwidth=1,
        relief="flat",
        font=("Segoe UI", 10),
        padding=(20, 10),
    )

    # --- Window Size & Centering ---
    popup_width = 1200
    popup_height = 650
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x_pos = int((screen_w - popup_width) / 2)
    y_pos = int((screen_h - popup_height) / 2.5)
    root.geometry(f"{popup_width}x{popup_height}+{x_pos}+{y_pos}")
    root.minsize(900, 500)

    # --- Header Section ---
    header_frame = tk.Frame(root, bg=HEADER_BG, height=70)
    header_frame.pack(fill=tk.X, padx=0, pady=0)
    header_frame.pack_propagate(False)

    # Add subtle bottom border to header
    header_border = tk.Frame(header_frame, bg=BORDER_COLOR, height=1)
    header_border.pack(side=tk.BOTTOM, fill=tk.X)

    title_label = tk.Label(
        header_frame,
        text="Review & Edit Timesheet Entries",
        font=("Segoe UI", 16, "bold"),
        bg=HEADER_BG,
        fg=TEXT_PRIMARY,
        anchor="w",
    )
    title_label.pack(side=tk.LEFT, padx=30, pady=20)

    subtitle = tk.Label(
        header_frame,
        text=f"{len(entries)} entries • Double-click to edit",
        font=("Segoe UI", 10),
        bg=HEADER_BG,
        fg=TEXT_SECONDARY,
        anchor="w",
    )
    subtitle.pack(side=tk.LEFT, padx=(0, 30), pady=20)

    # --- Main Content Area ---
    content_frame = tk.Frame(root, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    # Card-like container for table
    table_container = tk.Frame(
        content_frame,
        bg="#ffffff",
        highlightbackground=BORDER_COLOR,
        highlightthickness=1,
    )
    table_container.pack(fill=tk.BOTH, expand=True)

    # Get fields from sample entry
    sample = entries[0]
    fields = list(vars(sample).keys())

    # Create frame for tree and scrollbar
    tree_frame = tk.Frame(table_container, bg="#ffffff")
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

    # Modern scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Horizontal scrollbar for wide content
    h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    tree = ttk.Treeview(
        tree_frame,
        columns=fields,
        show="headings",
        style="Modern.Treeview",
        yscrollcommand=scrollbar.set,
        xscrollcommand=h_scrollbar.set,
        selectmode="browse",
    )
    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=tree.yview)
    h_scrollbar.config(command=tree.xview)

    # Configure columns with better widths
    column_widths = {
        "tasktype": 100,
        "functionality": 250,
        "task": 250,
        "timespent": 120,
        "projectUID": 120,
    }

    for f in fields:
        display_name = f.replace("_", " ").title()
        tree.heading(f, text=display_name)

        width = column_widths.get(f, 150)
        tree.column(
            f,
            width=width,
            minwidth=80,
            anchor="w" if f in ["functionality", "task"] else "center",
        )

    # Insert rows with alternating colors effect
    for idx, e in enumerate(entries):
        values = [getattr(e, f) for f in fields]
        tree.insert(
            "", tk.END, values=values, tags=("evenrow" if idx % 2 == 0 else "oddrow",)
        )

    # Subtle alternating row colors
    tree.tag_configure("evenrow", background="#ffffff")
    tree.tag_configure("oddrow", background="#f9fafb")

    # --- Editable Cell Logic ---
    def on_double_click(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = tree.identify_row(event.y)
        col_id = tree.identify_column(event.x)

        if not row_id or not col_id:
            return

        col_index = int(col_id.replace("#", "")) - 1

        x, y, width, height = tree.bbox(row_id, col_id)

        value = tree.set(row_id, fields[col_index])

        # Modern entry widget
        editor = tk.Entry(
            tree_frame,
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=2,
            highlightthickness=2,
            highlightbackground=PRIMARY_COLOR,
            highlightcolor=PRIMARY_COLOR,
        )
        editor.insert(0, value)
        editor.select_range(0, tk.END)
        editor.focus()

        editor.place(x=x, y=y, width=width, height=height)

        def save_edit(event=None):
            new_val = editor.get()
            tree.set(row_id, fields[col_index], new_val)
            editor.destroy()

        def cancel_edit(event=None):
            editor.destroy()

        editor.bind("<Return>", save_edit)
        editor.bind("<Escape>", cancel_edit)
        editor.bind("<FocusOut>", lambda e: editor.destroy())

    tree.bind("<Double-1>", on_double_click)

    # --- Footer with Buttons ---
    footer_frame = tk.Frame(root, bg=BG_COLOR, height=80)
    footer_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
    footer_frame.pack_propagate(False)

    btn_container = tk.Frame(footer_frame, bg=BG_COLOR)
    btn_container.pack(side=tk.RIGHT)

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
        edited_entries.clear()
        root.destroy()

    # Modern buttons
    cancel_btn = tk.Button(
        btn_container,
        text="Cancel",
        command=on_cancel,
        bg="#ffffff",
        fg=TEXT_PRIMARY,
        font=("Segoe UI", 10),
        relief="flat",
        borderwidth=1,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        cursor="hand2",
        padx=25,
        pady=10,
    )
    cancel_btn.pack(side=tk.LEFT, padx=(0, 10))

    ok_btn = tk.Button(
        btn_container,
        text="Save Changes",
        command=on_ok,
        bg=PRIMARY_COLOR,
        fg="#ffffff",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=30,
        pady=10,
    )
    ok_btn.pack(side=tk.LEFT)

    # Hover effects
    def on_enter_ok(e):
        ok_btn.config(bg=HOVER_COLOR)

    def on_leave_ok(e):
        ok_btn.config(bg=PRIMARY_COLOR)

    def on_enter_cancel(e):
        cancel_btn.config(bg=BG_COLOR)

    def on_leave_cancel(e):
        cancel_btn.config(bg="#ffffff")

    ok_btn.bind("<Enter>", on_enter_ok)
    ok_btn.bind("<Leave>", on_leave_ok)
    cancel_btn.bind("<Enter>", on_enter_cancel)
    cancel_btn.bind("<Leave>", on_leave_cancel)

    root.mainloop()

    return edited_entries if edited_entries else None
