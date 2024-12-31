import os

MAX_NAME_LENGTH = 50
MAX_DIAGNOSIS_LENGTH = 100
MAX_TREATMENT_LENGTH = 100
HEALTH_RECORD_FILE = "health_records.txt"
APPOINTMENT_FILE = "appointments.txt"
USER_FILE = "users.txt"
CLIENT_FILE = "client.txt"

class HealthRecord:
    def __init__(self, record_id, patient_name, diagnosis, treatment_plan, doctor_assigned):
        self.record_id = record_id
        self.patient_name = patient_name
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan
        self.doctor_assigned = doctor_assigned

class Appointment:
    def __init__(self, appointment_id, patient_name, doctor_name, date, time):
        self.appointment_id = appointment_id
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.date = date
        self.time = time

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Create a new health record")
        print("2. Update a health record")
        print("3. Display all health records")
        print("4. Search for a health record")
        print("5. Remove a health record")
        print("6. Add Appointment")
        print("7. Update Appointment")
        print("8. Cancel Appointment")
        print("9. Display Appointments")
        print("10. Export Health Records to CSV")
        print("11. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_health_record()
        elif choice == 2:
            update_health_record()
        elif choice == 3:
            display_health_records()
        elif choice == 4:
            search_health_record()
        elif choice == 5:
            remove_health_record()
        elif choice == 6:
            add_appointment()
        elif choice == 7:
            update_appointment()
        elif choice == 8:
            cancel_appointment()
        elif choice == 9:
            display_appointments()
        elif choice == 10:
            export_health_records_to_csv()
        elif choice == 11:
            break
        else:
            print("Invalid choice. Please try again.")

def doctor_menu():
    while True:
        print("\nDoctor Menu:")
        print("1. View Health Records")
        print("2. View Health Records")
        print("3. Update Health Record")
        print("4. Display Appointments")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            display_health_records()
        elif choice == 2:
            search_health_record()
        elif choice == 3:
            update_health_record()
        elif choice == 4:
            display_appointments()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

def receptionist_menu():
    while True:
        print("\nReceptionist Menu:")
        print("1. Add Appointment")
        print("2. Display Appointments")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_appointment()
        elif choice == 2:
            display_appointments()
        elif choice == 3:
            break
        else:
            print("Invalid choice. Please try again.")

def client_menu():
    while True:
        print("\nClient Menu:")
        print("1. View Health Record")
        print("2. Add Appointment")
        print("3. Cancel Appointment")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            view_health_record()
        elif choice == 2:
            add_appointment()
        elif choice == 3:
            cancel_appointment()
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

def user_login():
    username = input("Username: ")
    password = input("Password: ")

    with open(USER_FILE, "r", encoding="utf-8") as user_file:
        for line in user_file:
            file_username, file_password, role = line.strip().split()
            if username == file_username and password == file_password:
                return role
    return None

def client_login():
    username = input("Username: ")
    password = input("Password: ")

    with open(CLIENT_FILE, "r", encoding="utf-8") as client_file:
        for line in client_file:
            file_username, file_password = line.strip().split()
            if username == file_username and password == file_password:
                return True
    return False

def create_health_record():
    record_id = int(input("Enter record ID: "))
    patient_name = input("Enter patient name: ")
    diagnosis = input("Enter diagnosis: ")
    treatment_plan = input("Enter treatment plan: ")
    doctor_assigned = input("Enter doctor assigned: ")

    username = patient_name[:20]
    password = f"{patient_name[:3]}{record_id}"

    with open(CLIENT_FILE, "a", encoding="utf-8") as client_file:
        client_file.write(f"{username} {password}\n")

    with open(HEALTH_RECORD_FILE, "a", encoding="utf-8") as file:
        record = HealthRecord(record_id, patient_name, diagnosis, treatment_plan, doctor_assigned)
        file.write(f"{record.record_id},{record.patient_name},{record.diagnosis},{record.treatment_plan},{record.doctor_assigned}\n")
    
    print(f"Health record created successfully! Username: {username}, Password: {password}")

def display_health_records():
    print("\nHealth Records:")
    if os.path.exists(HEALTH_RECORD_FILE):
        with open(HEALTH_RECORD_FILE, "r", encoding="utf-8") as file:
            for line in file:
                record_id, patient_name, diagnosis, treatment_plan, doctor_assigned = line.strip().split(',')
                print(f"Record ID: {record_id}, Patient Name: {patient_name}, Diagnosis: {diagnosis}, Treatment Plan: {treatment_plan}, Doctor Assigned: {doctor_assigned}")
    else:
        print("No health records found.")

def search_health_record():
    choice = int(input("Search by:\n1. Record ID\n2. Patient Name\nEnter your choice: "))
    if choice == 1:
        record_id = int(input("Enter record ID: "))
        found = False
        with open(HEALTH_RECORD_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith(f"{record_id},"):
                    print(line.strip())
                    found = True
                    break
        if not found:
            print("Record not found.")
    elif choice == 2:
        patient_name = input("Enter patient name: ")
        found = False
        with open(HEALTH_RECORD_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if patient_name in line:
                    print(line.strip())
                    found = True
                    break
        if not found:
            print("Record not found.")

def update_health_record():
    record_id = int(input("Enter record ID to update: "))
    found = False
    lines = []
    with open(HEALTH_RECORD_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(HEALTH_RECORD_FILE, "w", encoding="utf-8") as file:
        for line in lines:
            if line.startswith(f"{record_id},"):
                found = True
                patient_name = input("Enter new patient name: ")
                diagnosis = input("Enter new diagnosis: ")
                treatment_plan = input("Enter new treatment plan: ")
                doctor_assigned = input("Enter new doctor assigned: ")
                file.write(f"{record_id},{patient_name},{diagnosis},{treatment_plan},{doctor_assigned}\n")
            else:
                file.write(line)

    if found:
        print("Health record updated successfully!")
    else:
        print("Record not found.")

def remove_health_record():
    record_id = int(input("Enter record ID to remove: "))
    found = False
    lines = []
    with open(HEALTH_RECORD_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(HEALTH_RECORD_FILE, "w", encoding="utf-8") as file:
        for line in lines:
            if not line.startswith(f"{record_id},"):
                file.write(line)
            else:
                found = True

    if found:
        print("Health record removed successfully!")
    else:
        print("Record not found.")

def add_appointment():
    appointment_id = int(input("Enter appointment ID: "))
    doctor_name = input("Enter doctor name: ")
    date = input("Enter date (DD/MM/YYYY): ")
    time = input("Enter time (HH:MM): ")

    patient_name = input("Enter patient name: ")

    with open(APPOINTMENT_FILE, "a", encoding="utf-8") as appointment_file:
        appointment = Appointment(appointment_id, patient_name, doctor_name, date, time)
        appointment_file.write(f"{appointment.appointment_id},{appointment.patient_name},{appointment.doctor_name},{appointment.date},{appointment.time}\n")

    print("Appointment added successfully!")

def display_appointments():
    print("\nAppointments:")
    if os.path.exists(APPOINTMENT_FILE):
        with open(APPOINTMENT_FILE, "r", encoding="utf-8") as file:
            for line in file:
                appointment_id, patient_name, doctor_name, date, time = line.strip().split(',')
                print(f"Appointment ID: {appointment_id}, Patient Name: {patient_name}, Doctor Name: {doctor_name}, Date: {date}, Time: {time}")
    else:
        print("No appointments found.")

def export_health_records_to_csv():
    if os.path.exists(HEALTH_RECORD_FILE):
        with open(HEALTH_RECORD_FILE, "r", encoding="utf-8") as file:
            with open("health_records.csv", "w", encoding="utf-8") as csv_file:
                csv_file.write("Record ID,Patient Name,Diagnosis,Treatment Plan,Doctor Assigned\n")
                for line in file:
                    csv_file.write(line)
        print("Health records exported to health_records.csv successfully!")
    else:
        print("No health records to export.")

def view_health_record():
    username = input("Enter your username: ")
    found = False
    with open(HEALTH_RECORD_FILE, "r", encoding="utf-8") as file:
        for line in file:
            record_id, patient_name, diagnosis, treatment_plan, doctor_assigned = line.strip().split(',')
            if username == patient_name[:20]:  # Match username with patient name
                print(f"Record ID: {record_id}, Patient Name: {patient_name}, Diagnosis: {diagnosis}, Treatment Plan: {treatment_plan}, Doctor Assigned: {doctor_assigned}")
                found = True
                break
    if not found:
        print("No health record found for this username.")

def cancel_appointment():
    appointment_id = int(input("Enter appointment ID to cancel: "))
    found = False
    lines = []
    with open(APPOINTMENT_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(APPOINTMENT_FILE, "w", encoding="utf-8") as file:
        for line in lines:
            if not line.startswith(f"{appointment_id},"):
                file.write(line)
            else:
                found = True

    if found:
        print("Appointment canceled successfully!")
    else:
        print("Appointment not found.")

def main():
    print("Welcome to the Hospital Management System")
    choice = int(input("1. User Login\n2. Client Login\n3. Register New Client\nEnter your choice: "))

    if choice == 1:
        role = user_login()
        if role == "admin":
            admin_menu()
        elif role == "doctor":
            doctor_menu()
        elif role == "receptionist":
            receptionist_menu()
        else:
            print("Invalid login. Exiting...")
    elif choice == 2:
        if client_login():
            client_menu()
        else:
            print("Invalid client login. Exiting...")
    elif choice == 3:
        register_client()

def register_client():
    username = input("Username: ")
    password = input("Password: ")

    with open(CLIENT_FILE, "a", encoding="utf-8") as client_file:
        client_file.write(f"{username} {password}\n")
    
    print("Client registered successfully!")

if __name__ == "__main__":
    main()