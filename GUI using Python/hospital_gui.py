import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv

HEALTH_RECORD_FILE = "health_records.txt"
APPOINTMENT_FILE = "appointments.txt"
USER_FILE = "users.txt"
CLIENT_FILE = "client.txt"


# Utility functions
def write_to_file(filename, data):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n")


def read_file_lines(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    return []


def write_all_lines(filename, lines):
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(lines)


# GUI Functions
def user_login():
    username = username_entry.get()
    password = password_entry.get()
    for line in read_file_lines(USER_FILE):
        file_username, file_password, role = line.strip().split()
        if username == file_username and password == file_password:
            return role
    return None


def client_login():
    username = username_entry.get()
    password = password_entry.get()
    for line in read_file_lines(CLIENT_FILE):
        file_username, file_password = line.strip().split()
        if username == file_username and password == file_password:
            return True
    return False


# GUI Menus
def admin_menu():
    menu_window("Admin Menu", [
        ("Create Health Record", create_health_record),
        ("Display Health Records", display_health_records),
        ("Search for a Health Record", search_health_record),
        ("Add Appointment", add_appointment),
        ("Update Appointment", update_appointment),
        ("Display Appointments", display_appointments),
        ("Export Health Records to CSV", export_health_records_to_csv),
    ])


def doctor_menu():
    menu_window("Doctor Menu", [
        ("View Health Records", display_health_records),
        ("Search for a Health Record", search_health_record),
        ("Update Health Record", update_health_record),
        ("Display Appointments", display_appointments),
    ])


def receptionist_menu():
    menu_window("Receptionist Menu", [
        ("Add Appointment", add_appointment),
        ("Display Appointments", display_appointments),
        ("Search Health Record", search_health_record),
    ])


def client_menu():
    menu_window("Client Menu", [
        ("View Health Records", lambda: view_client_health_record(username_entry.get())),
        ("Cancel Appointment", lambda: cancel_client_appointment(username_entry.get())),
    ])


# GUI Components
def login_page():
    for widget in main_window.winfo_children():
        widget.destroy()

    global username_entry, password_entry
    tk.Label(main_window, text="Hospital Management System", font=("Arial", 20, "bold")).pack(pady=20)

    frame = ttk.Frame(main_window, padding=10)
    frame.pack(pady=10)

    ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    username_entry = ttk.Entry(frame, width=30)
    username_entry.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    password_entry = ttk.Entry(frame, width=30, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    ttk.Button(frame, text="User Login", command=user_login_button).grid(row=2, column=0, pady=10, sticky="w")
    ttk.Button(frame, text="Client Login", command=client_login_button).grid(row=2, column=1, pady=10, sticky="e")
    ttk.Button(main_window, text="Register Client", command=register_client).pack(pady=10)

def user_login_button():
    role = user_login()
    if role == "admin":
        admin_menu()
    elif role == "doctor":
        doctor_menu()
    elif role == "receptionist":
        receptionist_menu()
    else:
        tk.messagebox.showerror("Login Failed", "Invalid username or password.")


def client_login_button():
    if client_login():
        client_menu()
    else:
        tk.messagebox.showerror("Login Failed", "Invalid client login.")


def register_client():
    username = simpledialog.askstring("Register", "Enter Username:")
    password = simpledialog.askstring("Register", "Enter Password:")
    write_to_file(CLIENT_FILE, f"{username} {password}")
    messagebox.showinfo("Register", "Client registered successfully!")


def create_health_record():
    record_id = simpledialog.askstring("Health Record", "Enter Record ID:")
    patient_name = simpledialog.askstring("Health Record", "Enter Patient Name:")
    diagnosis = simpledialog.askstring("Health Record", "Enter Diagnosis:")
    treatment_plan = simpledialog.askstring("Health Record", "Enter Treatment Plan:")
    doctor_assigned = simpledialog.askstring("Health Record", "Enter Doctor Assigned:")
    write_to_file(HEALTH_RECORD_FILE, f"{record_id},{patient_name},{diagnosis},{treatment_plan},{doctor_assigned}")
    messagebox.showinfo("Success", "Health record created successfully!")


def display_health_records():
    records = read_file_lines(HEALTH_RECORD_FILE)
    if not records:
        messagebox.showinfo("Health Records", "No records found.")
        return
    records_window(records)


def search_health_record():
    search_query = simpledialog.askstring("Search Record", "Enter Record ID or Patient Name:")
    records = read_file_lines(HEALTH_RECORD_FILE)
    found_records = [line for line in records if search_query in line]
    if found_records:
        records_window(found_records)
    else:
        messagebox.showinfo("Search Result", "No matching records found.")


def add_appointment():
    appointment_id = simpledialog.askstring("Appointment", "Enter Appointment ID:")
    patient_name = simpledialog.askstring("Appointment", "Enter Patient Name:")
    doctor_name = simpledialog.askstring("Appointment", "Enter Doctor Name:")
    date = simpledialog.askstring("Appointment", "Enter Date (DD/MM/YYYY):")
    time = simpledialog.askstring("Appointment", "Enter Time (HH:MM):")
    write_to_file(APPOINTMENT_FILE, f"{appointment_id},{patient_name},{doctor_name},{date},{time}")
    messagebox.showinfo("Success", "Appointment added successfully!")


def update_health_record():
    record_id = simpledialog.askstring("Update Record", "Enter Record ID to update:")
    records = read_file_lines(HEALTH_RECORD_FILE)
    updated = False
    with open(HEALTH_RECORD_FILE, "w") as file:
        for line in records:
            if line.startswith(record_id):
                patient_name = simpledialog.askstring("Health Record", "Enter Patient Name:")
                diagnosis = simpledialog.askstring("Health Record", "Enter Diagnosis:")
                treatment_plan = simpledialog.askstring("Health Record", "Enter Treatment Plan:")
                doctor_assigned = simpledialog.askstring("Health Record", "Enter Doctor Assigned:")
                file.write(f"{record_id},{patient_name},{diagnosis},{treatment_plan},{doctor_assigned}\n")
                updated = True
            else:
                file.write(line)
    if updated:
        messagebox.showinfo("Success", "Health record updated successfully!")
    else:
        messagebox.showinfo("Error", "Record ID not found.")


def update_appointment():
    appointment_id = simpledialog.askstring("Update Appointment", "Enter Appointment ID to update:")
    appointments = read_file_lines(APPOINTMENT_FILE)
    updated = False
    with open(APPOINTMENT_FILE, "w") as file:
        for line in appointments:
            if line.startswith(appointment_id):
                patient_name = simpledialog.askstring("Appointment", "Enter Patient Name:")
                doctor_name = simpledialog.askstring("Appointment", "Enter Doctor Name:")
                date = simpledialog.askstring("Appointment", "Enter Date (DD/MM/YYYY):")
                time = simpledialog.askstring("Appointment", "Enter Time (HH:MM):")
                file.write(f"{appointment_id},{patient_name},{doctor_name},{date},{time}\n")
                updated = True
            else:
                file.write(line)
    if updated:
        messagebox.showinfo("Success", "Appointment updated successfully!")
    else:
        messagebox.showinfo("Error", "Appointment ID not found.")


def display_appointments():
    appointments = read_file_lines(APPOINTMENT_FILE)
    if not appointments:
        messagebox.showinfo("Appointments", "No appointments found.")
        return
    records_window(appointments)


def export_health_records_to_csv():
    csv_file = "health_records.csv"
    records = read_file_lines(HEALTH_RECORD_FILE)
    if records:
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Record ID", "Patient Name", "Diagnosis", "Treatment Plan", "Doctor Assigned"])
            for record in records:
                writer.writerow(record.strip().split(","))
        messagebox.showinfo("Success", f"Health records exported to {csv_file} successfully!")
    else:
        messagebox.showinfo("Export", "No health records to export.")


# Utility GUI Functions
def menu_window(title, options):
    for widget in main_window.winfo_children():
        widget.destroy()

    tk.Label(main_window, text=title, font=("Arial", 20, "bold")).pack(pady=20)
    frame = ttk.Frame(main_window, padding=10)
    frame.pack(pady=10)

    for option in options:
        ttk.Button(frame, text=option[0], command=option[1], width=30).pack(pady=5)

    ttk.Button(main_window, text="Back", command=login_page).pack(pady=20)


def records_window(records):
    records_win = tk.Toplevel(main_window)
    records_win.title("Records")
    records_win.geometry("600x400")

    text = tk.Text(records_win, font=("Courier", 12), wrap=tk.WORD)
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text.insert(tk.END, "\n".join(records))


# Initialize GUI
main_window = tk.Tk()
main_window.title("Hospital Management System")
main_window.geometry("600x400")
login_page()
main_window.mainloop()
