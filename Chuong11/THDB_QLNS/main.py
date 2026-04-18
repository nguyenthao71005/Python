import tkinter as tk
from tkinter import messagebox, ttk

from Chuong11.THDB_QLNS.database import connect_db


class QuanLyNhanSuApp:
    EMPLOYEE_ALIASES = {
        "empno": ["empno", "manv", "employee_id", "id"],
        "ename": ["ename", "hoten", "tennv", "employee_name", "name"],
        "job": ["job", "chucvu", "position", "role"],
        "mgr": ["mgr", "manager", "maql", "manager_id"],
        "hiredate": ["hiredate", "ngayvaolam", "ngaylamviec", "join_date"],
        "sal": ["sal", "salary", "luong"],
        "comm": ["comm", "commission", "phucap", "thuong"],
        "deptno": ["deptno", "maphong", "department_id"],
    }

    DEPARTMENT_ALIASES = {
        "deptno": ["deptno", "maphong", "department_id", "id"],
        "dname": ["dname", "tenphong", "department_name", "name"],
        "loc": ["loc", "diadiem", "location", "address"],
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Quan ly employee / department - SQL Server")
        self.root.geometry("1180x760")

        self.employee_columns = {}
        self.department_columns = {}

        self.department_vars = {
            "deptno": tk.StringVar(),
            "dname": tk.StringVar(),
            "loc": tk.StringVar(),
        }
        self.employee_vars = {
            "empno": tk.StringVar(),
            "ename": tk.StringVar(),
            "job": tk.StringVar(value="MANAGER"),
            "mgr": tk.StringVar(),
            "hiredate": tk.StringVar(),
            "sal": tk.StringVar(),
            "comm": tk.StringVar(),
            "deptno": tk.StringVar(),
        }

        self.build_ui()
        self.load_schema()
        self.load_all_employees()
        self.load_departments()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="THDB_QLNS - Employee / Department (Tkinter + SQL Server)",
            font=("Arial", 16, "bold"),
            pady=12,
        )
        title.pack()

        wrapper = tk.Frame(self.root, padx=12, pady=6)
        wrapper.pack(fill="both", expand=True)

        left_frame = ttk.LabelFrame(wrapper, text="Thong tin department")
        left_frame.pack(side="left", fill="y", padx=(0, 8))

        right_frame = ttk.LabelFrame(wrapper, text="Thong tin employee")
        right_frame.pack(side="left", fill="y", padx=(8, 0))

        self.add_labeled_entry(left_frame, "Ma phong", self.department_vars["deptno"], 0)
        self.add_labeled_entry(left_frame, "Ten phong", self.department_vars["dname"], 1)
        self.add_labeled_entry(left_frame, "Dia diem", self.department_vars["loc"], 2)

        department_hint = tk.Label(
            left_frame,
            text="Nut B se them thong tin phong ban ban nhap vao bang department.",
            wraplength=300,
            justify="left",
            fg="navy",
        )
        department_hint.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

        employee_labels = [
            ("Ma nhan vien", "empno"),
            ("Ho ten", "ename"),
            ("Chuc vu", "job"),
            ("Ma quan ly", "mgr"),
            ("Ngay vao lam", "hiredate"),
            ("Luong", "sal"),
            ("Hoa hong", "comm"),
            ("Ma phong", "deptno"),
        ]
        for row_index, (label_text, key) in enumerate(employee_labels):
            self.add_labeled_entry(right_frame, label_text, self.employee_vars[key], row_index)

        employee_hint = tk.Label(
            right_frame,
            text=(
                "Nhap thong tin ca nhan cua ban de dung cho C va D. "
                "Ngay vao lam nen theo dinh dang YYYY-MM-DD."
            ),
            wraplength=340,
            justify="left",
            fg="navy",
        )
        employee_hint.grid(
            row=len(employee_labels),
            column=0,
            columnspan=2,
            padx=10,
            pady=(0, 10),
            sticky="w",
        )

        action_frame = ttk.LabelFrame(self.root, text="Chuc nang")
        action_frame.pack(fill="x", padx=12, pady=6)

        buttons = [
            ("A. Lay danh sach MANAGER", self.show_managers),
            ("B. Insert department", self.insert_department),
            ("C. Insert employee", self.insert_employee),
            ("D. Update CLARK", self.update_clark),
            ("E. Delete MILLER", self.delete_miller),
            ("Tai lai employee", self.load_all_employees),
            ("Tai lai department", self.load_departments),
        ]
        for index, (text, command) in enumerate(buttons):
            tk.Button(
                action_frame,
                text=text,
                command=command,
                width=24,
                bg="#0b5ed7" if index < 5 else "#6c757d",
                fg="white",
            ).grid(row=index // 4, column=index % 4, padx=8, pady=8, sticky="ew")

        table_frame = ttk.LabelFrame(self.root, text="Ket qua employee")
        table_frame.pack(fill="both", expand=True, padx=12, pady=(6, 4))

        self.employee_table = ttk.Treeview(table_frame, show="headings")
        self.employee_table.pack(side="left", fill="both", expand=True)
        employee_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.employee_table.yview)
        employee_scroll.pack(side="right", fill="y")
        self.employee_table.configure(yscrollcommand=employee_scroll.set)

        dept_frame = ttk.LabelFrame(self.root, text="Du lieu department")
        dept_frame.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        self.department_table = ttk.Treeview(dept_frame, show="headings", height=6)
        self.department_table.pack(side="left", fill="both", expand=True)
        dept_scroll = ttk.Scrollbar(dept_frame, orient="vertical", command=self.department_table.yview)
        dept_scroll.pack(side="right", fill="y")
        self.department_table.configure(yscrollcommand=dept_scroll.set)

    @staticmethod
    def add_labeled_entry(parent, label_text, variable, row):
        tk.Label(parent, text=label_text, anchor="w", width=14).grid(
            row=row, column=0, padx=10, pady=6, sticky="w"
        )
        tk.Entry(parent, textvariable=variable, width=30).grid(
            row=row, column=1, padx=10, pady=6, sticky="ew"
        )

    def execute_query(self, query, params=None, fetch=False, commit=False):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            data = cursor.fetchall() if fetch else None
            columns = [item[0] for item in cursor.description] if cursor.description else []
            if commit:
                conn.commit()
            return data, cursor.rowcount, columns
        finally:
            conn.close()

    def load_schema(self):
        try:
            employee_rows, _, _ = self.execute_query(
                """
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'employee'
                ORDER BY ORDINAL_POSITION
                """,
                fetch=True,
            )
            department_rows, _, _ = self.execute_query(
                """
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'department'
                ORDER BY ORDINAL_POSITION
                """,
                fetch=True,
            )

            employee_names = [row[0] for row in employee_rows]
            department_names = [row[0] for row in department_rows]

            self.employee_columns = self.resolve_columns(employee_names, self.EMPLOYEE_ALIASES)
            self.department_columns = self.resolve_columns(department_names, self.DEPARTMENT_ALIASES)
        except Exception as exc:
            messagebox.showerror("Loi schema", str(exc))

    @staticmethod
    def resolve_columns(actual_columns, aliases):
        lookup = {column.lower(): column for column in actual_columns}
        resolved = {}

        for logical_name, candidates in aliases.items():
            for candidate in candidates:
                if candidate.lower() in lookup:
                    resolved[logical_name] = lookup[candidate.lower()]
                    break
        return resolved

    def require_columns(self, mapping, table_name, required_keys):
        missing = [key for key in required_keys if key not in mapping]
        if missing:
            raise ValueError(
                f"Bang {table_name} thieu cot can thiet: {', '.join(missing)}. "
                "Hay kiem tra lai schema SQL Server."
            )

    def get_employee_input(self):
        values = {key: variable.get().strip() for key, variable in self.employee_vars.items()}
        required = ["empno", "ename", "job", "hiredate", "sal", "deptno"]
        missing = [field for field in required if not values[field]]
        if missing:
            raise ValueError(f"Vui long nhap day du: {', '.join(missing)}.")
        return values

    def get_department_input(self):
        values = {key: variable.get().strip() for key, variable in self.department_vars.items()}
        required = ["deptno", "dname", "loc"]
        missing = [field for field in required if not values[field]]
        if missing:
            raise ValueError(f"Vui long nhap day du: {', '.join(missing)}.")
        return values

    def refresh_treeview(self, treeview, columns, rows):
        treeview.delete(*treeview.get_children())
        treeview["columns"] = columns

        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=130, anchor="center")

        for row in rows:
            treeview.insert("", "end", values=[row[index] for index in range(len(columns))])

    def load_all_employees(self):
        try:
            data, _, columns = self.execute_query("SELECT * FROM employee", fetch=True)
            columns = columns or self.read_columns("employee")
            self.refresh_treeview(self.employee_table, columns, data)
        except Exception as exc:
            messagebox.showerror("Loi tai employee", str(exc))

    def load_departments(self):
        try:
            data, _, columns = self.execute_query("SELECT * FROM department", fetch=True)
            columns = columns or self.read_columns("department")
            self.refresh_treeview(self.department_table, columns, data)
        except Exception as exc:
            messagebox.showerror("Loi tai department", str(exc))

    def read_columns(self, table_name):
        rows, _, _ = self.execute_query(
            """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """,
            (table_name,),
            fetch=True,
        )
        return [row[0] for row in rows]

    def show_managers(self):
        try:
            self.require_columns(self.employee_columns, "employee", ["job"])
            job_column = self.employee_columns["job"]
            query = f"SELECT * FROM employee WHERE UPPER({job_column}) = 'MANAGER'"
            rows, _, columns = self.execute_query(query, fetch=True)
            columns = columns or self.read_columns("employee")
            self.refresh_treeview(self.employee_table, columns, rows)
            messagebox.showinfo("Thanh cong", "Da lay danh sach nhan vien co chuc vu MANAGER.")
        except Exception as exc:
            messagebox.showerror("Loi A", str(exc))

    def insert_department(self):
        try:
            self.require_columns(self.department_columns, "department", ["deptno", "dname", "loc"])
            values = self.get_department_input()
            columns = [self.department_columns[key] for key in ["deptno", "dname", "loc"]]
            query = f"""
                INSERT INTO department ({', '.join(columns)})
                VALUES (?, ?, ?)
            """
            params = (values["deptno"], values["dname"], values["loc"])
            self.execute_query(query, params=params, commit=True)
            self.load_departments()
            messagebox.showinfo("Thanh cong", "Da them thong tin vao bang department.")
        except Exception as exc:
            messagebox.showerror("Loi B", str(exc))

    def insert_employee(self):
        try:
            self.require_columns(
                self.employee_columns,
                "employee",
                ["empno", "ename", "job", "mgr", "hiredate", "sal", "comm", "deptno"],
            )
            values = self.get_employee_input()
            columns = [
                self.employee_columns[key]
                for key in ["empno", "ename", "job", "mgr", "hiredate", "sal", "comm", "deptno"]
            ]
            query = f"""
                INSERT INTO employee ({', '.join(columns)})
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                values["empno"],
                values["ename"],
                values["job"],
                values["mgr"] or None,
                values["hiredate"],
                values["sal"],
                values["comm"] or None,
                values["deptno"],
            )
            self.execute_query(query, params=params, commit=True)
            self.load_all_employees()
            messagebox.showinfo("Thanh cong", "Da them thong tin vao bang employee.")
        except Exception as exc:
            messagebox.showerror("Loi C", str(exc))

    def update_clark(self):
        try:
            self.require_columns(
                self.employee_columns,
                "employee",
                ["ename", "job", "mgr", "hiredate", "sal", "comm", "deptno"],
            )
            values = self.get_employee_input()
            columns = self.employee_columns
            query = f"""
                UPDATE employee
                SET {columns['ename']} = ?,
                    {columns['job']} = ?,
                    {columns['mgr']} = ?,
                    {columns['hiredate']} = ?,
                    {columns['sal']} = ?,
                    {columns['comm']} = ?,
                    {columns['deptno']} = ?
                WHERE UPPER({columns['ename']}) = 'CLARK'
            """
            params = (
                values["ename"],
                values["job"],
                values["mgr"] or None,
                values["hiredate"],
                values["sal"],
                values["comm"] or None,
                values["deptno"],
            )
            _, rowcount, _ = self.execute_query(query, params=params, commit=True)
            self.load_all_employees()
            if rowcount > 0:
                messagebox.showinfo("Thanh cong", "Da cap nhat nhan vien CLARK theo thong tin cua ban.")
            else:
                messagebox.showwarning("Thong bao", "Khong tim thay nhan vien co ten CLARK.")
        except Exception as exc:
            messagebox.showerror("Loi D", str(exc))

    def delete_miller(self):
        try:
            self.require_columns(self.employee_columns, "employee", ["ename"])
            name_column = self.employee_columns["ename"]
            query = f"DELETE FROM employee WHERE UPPER({name_column}) = 'MILLER'"
            _, rowcount, _ = self.execute_query(query, commit=True)
            self.load_all_employees()
            if rowcount > 0:
                messagebox.showinfo("Thanh cong", "Da xoa nhan vien co ten MILLER.")
            else:
                messagebox.showwarning("Thong bao", "Khong tim thay nhan vien co ten MILLER.")
        except Exception as exc:
            messagebox.showerror("Loi E", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuanLyNhanSuApp(root)
    root.mainloop()
