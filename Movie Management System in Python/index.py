"""
MASA CineVault: Desktop Motion Picture & Film Catalog Manager
Developer: MASA
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MasaCineVault(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MASA CineVault Pro - Movie Catalog")
        self.geometry("780x560")
        self.resizable(False, False)
        self.configure(fg_color="#0A0E17")

        self.db_path = "movies_vault.db"
        self._init_db()
        self._build_ui()
        self._refresh_table()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    director TEXT,
                    year INTEGER,
                    rating REAL
                )
            """)
            # Seed default demo entries if empty
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM movies")
            if cur.fetchone()[0] == 0:
                demo_movies = [
                    ("Inception", "Christopher Nolan", 2010, 8.8),
                    ("The Matrix", "Lana & Lilly Wachowski", 1999, 8.7),
                    ("Interstellar", "Christopher Nolan", 2014, 8.7),
                    ("Blade Runner 2049", "Denis Villeneuve", 2017, 8.0)
                ]
                cur.executemany("INSERT INTO movies (title, director, year, rating) VALUES (?, ?, ?, ?)", demo_movies)
                conn.commit()

    def _build_ui(self):
        top_card = ctk.CTkFrame(self, fg_color="#121826", corner_radius=14)
        top_card.pack(fill="x", padx=20, pady=(15, 10))

        title = ctk.CTkLabel(
            top_card,
            text="MASA CINEVAULT MANAGER",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#F59E0B"
        )
        title.pack(side="left", padx=20, pady=12)

        subtitle = ctk.CTkLabel(
            top_card,
            text="Cinematic Database & Review Archive",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8"
        )
        subtitle.pack(side="right", padx=20, pady=12)

        main_content = ctk.CTkFrame(self, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Left input panel
        form_panel = ctk.CTkFrame(main_content, fg_color="#121826", corner_radius=14, width=280)
        form_panel.pack(side="left", fill="y", padx=(0, 10))
        form_panel.pack_propagate(False)

        lbl_form = ctk.CTkLabel(form_panel, text="RECORD MANAGEMENT", font=ctk.CTkFont(size=12, weight="bold"), text_color="#94A3B8")
        lbl_form.pack(pady=(15, 10))

        self.entry_title = self._create_input(form_panel, "Movie Title")
        self.entry_director = self._create_input(form_panel, "Director")
        self.entry_year = self._create_input(form_panel, "Year (e.g. 2024)")
        self.entry_rating = self._create_input(form_panel, "Rating (0.0 - 10.0)")

        btn_add = ctk.CTkButton(
            form_panel,
            text="Add Movie",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#D97706",
            hover_color="#B45309",
            corner_radius=8,
            command=self._add_movie
        )
        btn_add.pack(fill="x", padx=16, pady=(12, 6))

        btn_del = ctk.CTkButton(
            form_panel,
            text="Delete Selected",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            corner_radius=8,
            command=self._delete_movie
        )
        btn_del.pack(fill="x", padx=16, pady=(0, 15))

        # Right table view
        table_panel = ctk.CTkFrame(main_content, fg_color="#121826", corner_radius=14)
        table_panel.pack(side="right", fill="both", expand=True)

        search_bar = ctk.CTkFrame(table_panel, fg_color="transparent")
        search_bar.pack(fill="x", padx=16, pady=(15, 8))

        self.search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search movie by title...",
            font=ctk.CTkFont(size=12),
            height=34,
            corner_radius=8
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda _: self._refresh_table())

        # Treeview setup
        tree_frame = tk.Frame(table_panel, bg="#121826")
        tree_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0A0E17", foreground="#F8FAFC", fieldbackground="#0A0E17", rowheight=28)
        style.configure("Treeview.Heading", background="#1E293B", foreground="#38BDF8", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#D97706")])

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Director", "Year", "Rating"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Director", text="Director")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Rating", text="Rating")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Title", width=160)
        self.tree.column("Director", width=130)
        self.tree.column("Year", width=60, anchor="center")
        self.tree.column("Rating", width=60, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _create_input(self, parent, placeholder):
        e = ctk.CTkEntry(parent, placeholder_text=placeholder, font=ctk.CTkFont(size=12), height=34, corner_radius=8)
        e.pack(fill="x", padx=16, pady=4)
        return e

    def _refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        q = self.search_entry.get().strip()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            if q:
                cur.execute("SELECT id, title, director, year, rating FROM movies WHERE title LIKE ? ORDER BY id DESC", (f"%{q}%",))
            else:
                cur.execute("SELECT id, title, director, year, rating FROM movies ORDER BY id DESC")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)

    def _add_movie(self):
        t = self.entry_title.get().strip()
        d = self.entry_director.get().strip()
        y = self.entry_year.get().strip()
        r = self.entry_rating.get().strip()

        if not t:
            messagebox.showwarning("Warning", "Title is mandatory")
            return

        try:
            year_val = int(y) if y else None
            rate_val = float(r) if r else None
        except ValueError:
            messagebox.showwarning("Warning", "Invalid Year or Rating format")
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO movies (title, director, year, rating) VALUES (?, ?, ?, ?)", (t, d, year_val, rate_val))
            conn.commit()

        self.entry_title.delete(0, "end")
        self.entry_director.delete(0, "end")
        self.entry_year.delete(0, "end")
        self.entry_rating.delete(0, "end")
        self._refresh_table()

    def _delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Select a record to delete")
            return

        rec_id = self.tree.item(selected[0])["values"][0]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM movies WHERE id = ?", (rec_id,))
            conn.commit()
        self._refresh_table()


if __name__ == "__main__":
    app = MasaCineVault()
    app.mainloop()
