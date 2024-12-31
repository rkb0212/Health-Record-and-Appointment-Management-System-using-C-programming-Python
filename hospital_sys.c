#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LENGTH 50
#define MAX_DIAGNOSIS_LENGTH 100
#define MAX_TREATMENT_LENGTH 100
#define HEALTH_RECORD_FILE "health_records.txt"
#define APPOINTMENT_FILE "appointments.txt"
#define USER_FILE "users.txt"  // New file for user credentials
#define CLIENT_FILE "client.txt"
#define ADMIN_USERNAME "admin"  // Hardcoded admin username & password
#define ADMIN_PASSWORD "admin123"

struct HealthRecord {
    int recordID;
    char patientName[MAX_NAME_LENGTH];
    char diagnosis[MAX_DIAGNOSIS_LENGTH];
    char treatmentPlan[MAX_TREATMENT_LENGTH];
    char doctorAssigned[MAX_NAME_LENGTH];
};

struct Appointment {
    int appointmentID;
    char patientName[MAX_NAME_LENGTH];
    char doctorName[MAX_NAME_LENGTH];
    char date[15];
    char time[10];
};

struct User {
    char username[20];
    char password[20];
    char role[20];  // New field for user role
};

// Function prototypes
void adminMenu();
void doctorMenu();
void receptionistMenu();
void clientMenu();
int userLogin(char *role);
int clientLogin();
void createHealthRecord(FILE **file);
void exportHealthRecordsToCSV(FILE **file);
void updateHealthRecord(FILE **file);
void displayHealthRecords(FILE **file);
void searchHealthRecord(FILE **file);
void viewHealthRecord(FILE **file);
void removeHealthRecord(FILE **file);
void addAppointment();
void updateAppointment();
void cancelAppointment();
void displayAppointments();
void handleFileError(const char *message);
int isAppointmentValid(struct Appointment *newAppointment);
void registerClient();

// Main function
int main() {
    char role[20];
    int choice;

    printf("Welcome to the Hospital Management System\n");
    printf("1. User Login\n");
    printf("2. Client Login\n");
    printf("3. Register New Client\n");
    printf("Enter your choice: ");
    scanf("%d", &choice);

    if (choice == 1) {
        if (userLogin(role)) {
            if (strcmp(role, "admin") == 0) {
                adminMenu();
            } else if (strcmp(role, "doctor") == 0) {
                doctorMenu();
            } else if (strcmp(role, "receptionist") == 0) {
                receptionistMenu();
            }
        } else {
            printf("Invalid login. Exiting...\n");
        }
    } else if (choice == 2) {
        if (clientLogin()) {
            clientMenu();
        } else {
            printf("Invalid client login. Exiting...\n");
        }
    } else if (choice == 3) {
        registerClient();
    }

    return EXIT_SUCCESS;
}
// Function to handle user login
int userLogin(char *role) {
    char username[20], password[20];
    FILE *userFile = fopen(USER_FILE, "r");

    if (userFile == NULL) {
        handleFileError("Error opening user file");
    }

    printf("User Login:\n");
    printf("Username: ");
    scanf("%s", username);
    printf("Password: ");
    scanf("%s", password);

    char fileUsername[20], filePassword[20];
    while (fscanf(userFile, "%s %s %s", fileUsername, filePassword, role) != EOF) {
        if (strcmp(username, fileUsername) == 0 && strcmp(password, filePassword) == 0) {
            fclose(userFile);
            return 1; // Successful login
        }
    }
    fclose(userFile);
    return 0; // Login failed
}

// Function to handle client login
int clientLogin() {
    char username[20], password[20];
    FILE *clientFile = fopen(CLIENT_FILE, "r");

    if (clientFile == NULL) {
        handleFileError("Error opening client file");
    }

    printf("Client Login:\n");
    printf("Username: ");
    scanf("%s", username);
    printf("Password: ");
    scanf("%s", password);

    char fileUsername[20], filePassword[20];
    while (fscanf(clientFile, "%s %s", fileUsername, filePassword) != EOF) {
        if (strcmp(username, fileUsername) == 0 && strcmp(password, filePassword) == 0) {
            fclose(clientFile);
            return 1; // Successful login
        }
    }
    fclose(clientFile);
    return 0; // Login failed
}

// ADMIN MENU
void adminMenu() {
    FILE *file = fopen(HEALTH_RECORD_FILE, "r+b");
    if (file == NULL) {
        file = fopen(HEALTH_RECORD_FILE, "w+b");
        if (file == NULL) {
            perror("Error creating health records file");
            return;
        }
    }

    int choice;
    while (1) {
        printf("\nAdmin Menu:\n");
        printf("1. Create a new health record\n");
        printf("2. Update a health record\n");
        printf("3. Display all health records\n");
        printf("4. Search for a health record\n");
        printf("5. Remove a health record\n");
        printf("6. Add Appointment\n");
        printf("7. Update Appointment\n");
        printf("8. Cancel Appointment\n");
        printf("9. Display Appointments\n");
        printf("10. Export Health Records to CSV\n"); // New option
        printf("11. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                createHealthRecord(&file);
                break;
            case 2:
                updateHealthRecord(&file);
                break;
            case 3:
                displayHealthRecords(&file);
                break;
            case 4:
                searchHealthRecord(&file);
                break;
            case 5:
                removeHealthRecord(&file);
                break;
            case 6:
                addAppointment();
                break;
            case 7:
                updateAppointment();
                break;
            case 8:
                cancelAppointment();
                break;
            case 9:
                displayAppointments();
                break;
            case 10:
                exportHealthRecordsToCSV(&file); 
                break;
            case 11:
                fclose(file);
                return;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}

// DOCTOR MENU
void doctorMenu() {
    int choice;
    while (1) {
        printf("\nDoctor Menu:\n");
        printf("1. View Health Records\n");
        printf("2. Search Record\n");
        printf("3. Update Health Record\n");
        printf("4. Display Appointments\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                displayHealthRecords(NULL);  // Display all records
                break;
            case 2:
                searchHealthRecord(&file);  // Search a specific record
                break;
            case 3:
                updateHealthRecord(NULL);   // Update health record
                break;
            case 4:
                displayAppointments();   // Display appointments
                break;
            case 5:
                return;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}

// RECEPTIONIST MENU
void receptionistMenu() {
    int choice;
    while (1) {
        printf("\nReceptionist Menu:\n");
        printf("1. Add Appointment\n");
        printf("2. Display Appointments\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                addAppointment();  // Add appointment
                break;
            case 2:
                displayAppointments(); // Display appointments
                break;
            case 3:
                return;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}

// CLIENT MENU
void clientMenu() {
    int choice;
    FILE *file = fopen(HEALTH_RECORD_FILE, "r+b");
    if (file == NULL) {
        file = fopen(HEALTH_RECORD_FILE, "w+b");
        if (file == NULL) {
            handleFileError("Error creating health records file");
            return;
        }
    }
    while (1) {
        printf("\nClient Menu:\n");
        printf("1. view health record\n");
        printf("2. Add Appointment\n");
        printf("3. Cancel Appointment\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {  
            case 1:
                viewHealthRecord(&file); //View Health Record
                break;
            case 2:
                addAppointment();  // Add appointment
                break;
            case 3:
                cancelAppointment(); // Cancel appointment
                break;
            case 4:
                return;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}

// Function to handle file errors
void handleFileError(const char *message) {
    perror(message);
    exit(EXIT_FAILURE);
}

// Create a new health record
void createHealthRecord(FILE **file) {
    struct HealthRecord newRecord;
    FILE *clientFile = fopen(CLIENT_FILE, "a+"); // Open client file to append

    if (clientFile == NULL) {
        handleFileError("Error opening client file");
    }

    printf("Enter record ID: ");
    scanf("%d", &newRecord.recordID);
    printf("Enter patient name: ");
    scanf(" %[^\n]s", newRecord.patientName);
    printf("Enter diagnosis: ");
    scanf(" %[^\n]s", newRecord.diagnosis);
    printf("Enter treatment plan: ");
    scanf(" %[^\n]s", newRecord.treatmentPlan);
    printf("Enter doctor assigned: ");
    scanf(" %[^\n]s", newRecord.doctorAssigned);

    // Generate username and password
    char username[20];
    char password[24]; // Enough space for the password
    strncpy(username, newRecord.patientName, 20);
    username[19] = '\0'; // Ensure null-terminated

    // Create password using first 3 letters of the patient's name + record ID for the client's login
    snprintf(password, sizeof(password), "%.3s%d", newRecord.patientName, newRecord.recordID);

    // Save username and password to client file
    fprintf(clientFile, "%s %s\n", username, password);
    fclose(clientFile);

    // Save the health record
    fseek(*file, 0, SEEK_END);
    if (fwrite(&newRecord, sizeof(struct HealthRecord), 1, *file) != 1) {
        handleFileError("Error writing to health records file");
    }
    printf("Health record created successfully! Username: %s, Password: %s\n", username, password);
}
// Export health record to csv file
void exportHealthRecordsToCSV(FILE **file) {
    struct HealthRecord record;
    FILE *csvFile = fopen("health_records.csv", "w");

    if (csvFile == NULL) {
        handleFileError("Error creating CSV file");
    }

    // Write CSV header
    fprintf(csvFile, "Record ID,Patient Name,Diagnosis,Treatment Plan,Doctor Assigned\n");

    fseek(*file, 0, SEEK_SET);
    while (fread(&record, sizeof(struct HealthRecord), 1, *file)) {
        fprintf(csvFile, "%d,%s,%s,%s,%s\n", 
                record.recordID, 
                record.patientName, 
                record.diagnosis, 
                record.treatmentPlan, 
                record.doctorAssigned);
    }

    fclose(csvFile);
    printf("Health records exported to health_records.csv successfully!\n");
}

// Update a health record
void updateHealthRecord(FILE **file) {
    int recordID;
    struct HealthRecord record;

    printf("Enter record ID to update: ");
    scanf("%d", &recordID);

    fseek(*file, 0, SEEK_SET);
    while (fread(&record, sizeof(struct HealthRecord), 1, *file)) {
        if (record.recordID == recordID) {
            printf("Record found. Enter new details:\n");
            printf("Enter new diagnosis: ");
            scanf(" %[^\n]s", record.diagnosis);
            printf("Enter new treatment plan: ");
            scanf(" %[^\n]s", record.treatmentPlan);

            fseek(*file, -(long long)sizeof(struct HealthRecord), SEEK_CUR);
            if (fwrite(&record, sizeof(struct HealthRecord), 1, *file) != 1) {
                handleFileError("Error updating health records file");
            }
            printf("Record updated successfully!\n");
            return;
        }
    }
    printf("Record not found.\n");
}

// Display all health records
void displayHealthRecords(FILE **file) {
    struct HealthRecord record;

    if (file != NULL) {
        fseek(*file, 0, SEEK_SET);
    }

    printf("\nHealth Records:\n");
    FILE *tempFile = (file == NULL) ? fopen(HEALTH_RECORD_FILE, "rb") : *file;
    while (fread(&record, sizeof(struct HealthRecord), 1, tempFile)) {
        printf("Record ID: %d\n", record.recordID);
        printf("Patient Name: %s\n", record.patientName);
        printf("Diagnosis: %s\n", record.diagnosis);
        printf("Treatment Plan: %s\n", record.treatmentPlan);
        printf("Doctor Assigned: %s\n", record.doctorAssigned);
        printf("--------------------------\n");
    }

    if (file == NULL) fclose(tempFile);
}

// Search for a health record
void searchHealthRecord(FILE **file) {
    int choice, recordID;
    char patientName[MAX_NAME_LENGTH];
    struct HealthRecord record;

    printf("Search by:\n");
    printf("1. Record ID\n");
    printf("2. Patient Name\n");
    printf("Enter your choice: ");
    scanf("%d", &choice);

    fseek(*file, 0, SEEK_SET);
    if (choice == 1) {
        printf("Enter record ID: ");
        scanf("%d", &recordID);

        while (fread(&record, sizeof(struct HealthRecord), 1, *file)) {
            if (record.recordID == recordID) {
                printf("Record found:\n");
                printf("Record ID: %d\n", record.recordID);
                printf("Patient Name: %s\n", record.patientName);
                printf("Diagnosis: %s\n", record.diagnosis);
                printf("Treatment Plan: %s\n", record.treatmentPlan);
                printf("Doctor Assigned: %s\n", record.doctorAssigned);
                return;
            }
        }
    } else if (choice == 2) {
        printf("Enter patient name: ");
        scanf(" %[^\n]s", patientName);

        while (fread(&record, sizeof(struct HealthRecord), 1, *file)) {
            if (strcmp(record.patientName, patientName) == 0) {
                printf("Record found:\n");
                printf("Record ID: %d\n", record.recordID);
                printf("Patient Name: %s\n", record.patientName);
                printf("Diagnosis: %s\n", record.diagnosis);
                printf("Treatment Plan: %s\n", record.treatmentPlan);
                printf("Doctor Assigned: %s\n", record.doctorAssigned);
                return;
            }
        }
    }
    printf("Record not found.\n");
}

void viewHealthRecord(FILE **file) {
    int recordID;
    struct HealthRecord record;

    printf("Enter record ID: ");
    scanf("%d", &recordID);

    fseek(*file, 0, SEEK_SET);
    while (fread(&record, sizeof(struct HealthRecord), 1, *file)) {
        if (record.recordID == recordID) {
            printf("Record found:\n");
            printf("Record ID: %d\n", record.recordID);
            printf("Patient Name: %s\n", record.patientName);
            printf("Diagnosis: %s\n", record.diagnosis);
            printf("Treatment Plan: %s\n", record.treatmentPlan);
            printf("Doctor Assigned: %s\n", record.doctorAssigned);
            return;
        }
    }
    printf("Record not found.\n");
}


// Function to remove a health record
void removeHealthRecord(FILE **file) {
    int recordID, found = 0;
    struct HealthRecord record;
    FILE *tempFile = fopen("temp_health_records.txt", "wb");

    if (tempFile == NULL) {
        handleFileError("Error creating temporary file");
    }

    printf("Enter record ID to remove: ");
    scanf("%d", &recordID);

    fseek(*file, 0, SEEK_SET);
    while (fread(&record, sizeof(struct HealthRecord), 1, *file)) {
        if (record.recordID == recordID) {
            found = 1;
            continue;
        }
        fwrite(&record, sizeof(struct HealthRecord), 1, tempFile);
    }

    fclose(*file);
    fclose(tempFile);

    remove(HEALTH_RECORD_FILE);
    rename("temp_health_records.txt", HEALTH_RECORD_FILE);

    *file = fopen(HEALTH_RECORD_FILE, "r+b");
    if (*file == NULL) {
        handleFileError("Error reopening health records file");
    }

    if (found) {
        printf("Health record removed successfully!\n");
    } else {
        printf("Record not found.\n");
    }
}

// Add appointment
void addAppointment() {
    struct Appointment appointment;
    char choice;  // Changed to char for menu selection
    int recordID;
    struct HealthRecord record;
    FILE *appointmentFile = fopen(APPOINTMENT_FILE, "ab");
    FILE *healthFile = fopen(HEALTH_RECORD_FILE, "rb");

    if (appointmentFile == NULL || healthFile == NULL) {
        handleFileError("Error opening file");
    }

    printf("Select patient type:\n");
    printf("a) New patient\n");
    printf("b) Existing patient\n");
    printf("Enter choice: ");
    scanf(" %c", &choice);

    printf("Enter appointment ID: ");
    scanf("%d", &appointment.appointmentID);
    printf("Enter doctor name: ");
    scanf(" %[^\n]s", appointment.doctorName);
    printf("Enter date (DD/MM/YYYY): ");
    scanf(" %[^\n]s", appointment.date);
    printf("Enter time (HH:MM): ");
    scanf(" %[^\n]s", appointment.time);

    if (choice == 'b') {
        printf("Enter record ID for the existing patient: ");
        scanf("%d", &recordID);

        int found = 0;
        fseek(healthFile, 0, SEEK_SET);
        while (fread(&record, sizeof(struct HealthRecord), 1, healthFile)) {
            if (record.recordID == recordID) {
                found = 1;
                strcpy(appointment.patientName, record.patientName); // Copy patient's name
                break;
            }
        }

        if (!found) {
            printf("Record ID not found. Please try again.\n");
            fclose(appointmentFile);
            fclose(healthFile);
            return;
        }
    } else {
        printf("Enter patient name: ");
        scanf(" %[^\n]s", appointment.patientName);
    }

    // Validity check for appointment, as to confirm the slot availability
    if (isAppointmentValid(&appointment)) {
        if (fwrite(&appointment, sizeof(struct Appointment), 1, appointmentFile) != 1) {
            handleFileError("Error writing to appointment file");
        }
        printf("Appointment added successfully!\n");
    } else {
        printf("Appointment time is not available.\n");
    }

    fclose(appointmentFile);
    fclose(healthFile);
}

// Check appointment validity
int isAppointmentValid(struct Appointment *newAppointment) {
    struct Appointment appointment;
    FILE *file = fopen(APPOINTMENT_FILE, "rb");

    if (file == NULL) {
        handleFileError("Error opening appointment file");
    }

    while (fread(&appointment, sizeof(struct Appointment), 1, file)) {
        if (strcmp(appointment.doctorName, newAppointment->doctorName) == 0 &&
            strcmp(appointment.date, newAppointment->date) == 0 &&
            strcmp(appointment.time, newAppointment->time) == 0) {
            fclose(file);
            return 0; //  Meaning Appointment is not valid
        }
    }

    fclose(file);
    return 1; // Appointment is valid
}

// Update appointment
void updateAppointment() {
    int appointmentID, found = 0;
    struct Appointment appointment;
    FILE *file = fopen(APPOINTMENT_FILE, "rb+");

    if (file == NULL) {
        handleFileError("Error opening appointment file");
    }

    printf("Enter appointment ID to update: ");
    scanf("%d", &appointmentID);

    while (fread(&appointment, sizeof(struct Appointment), 1, file)) {
        if (appointment.appointmentID == appointmentID) {
            printf("Appointment found. Enter new details:\n");
            printf("Enter new date (DD/MM/YYYY): ");
            scanf(" %[^\n]s", appointment.date);
            printf("Enter new time (HH:MM): ");
            scanf(" %[^\n]s", appointment.time);

            fseek(file, -(long long)sizeof(struct Appointment), SEEK_CUR);
            if (fwrite(&appointment, sizeof(struct Appointment), 1, file) != 1) {
                handleFileError("Error updating appointment file");
            }
            found = 1;
            printf("Appointment updated successfully!\n");
            break;
        }
    }

    if (!found) {
        printf("Appointment not found.\n");
    }

    fclose(file);
}

// Cancel appointment
void cancelAppointment() {
    int appointmentID, found = 0;
    struct Appointment appointment;
    FILE *tempFile = fopen("temp_appointments.txt", "wb");
    FILE *file = fopen(APPOINTMENT_FILE, "rb");

    if (tempFile == NULL || file == NULL) {
        handleFileError("Error opening appointment file");
    }

    printf("Enter appointment ID to cancel: ");
    scanf("%d", &appointmentID);

    while (fread(&appointment, sizeof(struct Appointment), 1, file)) {
        if (appointment.appointmentID == appointmentID) {
            found = 1; // Appointment found, skip writing it to the temp file
            continue;
        }
        fwrite(&appointment, sizeof(struct Appointment), 1, tempFile);
    }

    fclose(file);
    fclose(tempFile);

    remove(APPOINTMENT_FILE);
    rename("temp_appointments.txt", APPOINTMENT_FILE);
    
    if (found) {
        printf("Appointment canceled successfully!\n");
    } else {
        printf("Appointment not found.\n");
    }
}

// Display appointments
void displayAppointments() {
    struct Appointment appointment;
    FILE *file = fopen(APPOINTMENT_FILE, "rb");

    if (file == NULL) {
        handleFileError("Error opening appointment file");
    }

    printf("\nAppointments:\n");
    while (fread(&appointment, sizeof(struct Appointment), 1, file)) {
        printf("Appointment ID: %d\n", appointment.appointmentID);
        printf("Patient Name: %s\n", appointment.patientName);
        printf("Doctor Name: %s\n", appointment.doctorName);
        printf("Date: %s\n", appointment.date);
        printf("Time: %s\n", appointment.time);
        printf("--------------------------\n");
    }

    fclose(file);
}

// Register a new client
void registerClient() {
    char username[20], password[20];
    FILE *clientFile = fopen(CLIENT_FILE, "a");

    if (clientFile == NULL) {
        handleFileError("Error opening client file");
    }

    printf("Register New Client:\n");
    printf("Username: ");
    scanf("%s", username);
    printf("Password: ");
    scanf("%s", password);

    fprintf(clientFile, "%s %s\n", username, password);
    fclose(clientFile);
    printf("Client registered successfully!\n");
}

