import matplotlib.pyplot as plt

# File names (update with the correct paths)
client_file = 'd:/vs code/HRS/client.txt'
health_record_file = 'd:/vs code/HRS/health_records.txt'
appointment_file = 'd:/vs code/HRS/appointments.txt'
user_file = 'd:/vs code/HRS/users.txt'

# Function to read client data
def read_clients(filename):
    with open(filename, 'r') as file:
        clients = file.readlines()
    return len(clients)

# Function to read health records
def read_health_records(filename):
    with open(filename, 'rb') as file:
        records = []
        while True:
            record = file.read(128)  # Assuming each record is 128 bytes
            if not record:
                break
            records.append(record)
    return len(records)

# Function to read appointments
def read_appointments(filename):
    with open(filename, 'rb') as file:
        appointments = []
        while True:
            appointment = file.read(64)  # Assuming each appointment is 64 bytes
            if not appointment:
                break
            appointments.append(appointment)
    return len(appointments)

# Function to read user data
def read_users(filename):
    with open(filename, 'r') as file:
        users = file.readlines()
    return len(users)

# Read data
num_clients = read_clients(client_file)
num_health_records = read_health_records(health_record_file)
num_appointments = read_appointments(appointment_file)
num_users = read_users(user_file)

# Prepare data for visualizations
categories = ['Clients', 'Health Records', 'Appointments', 'Users']
values = [num_clients, num_health_records, num_appointments, num_users]

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Bar graph
ax1.bar(categories, values, color=['blue', 'orange', 'green', 'red'])
ax1.set_title('Counts of Clients, Health Records, Appointments, and Users')
ax1.set_xlabel('Categories')
ax1.set_ylabel('Count')
ax1.set_ylim(0, max(values) + 20)
ax1.grid(axis='y')

# Pie chart
labels = ['Clients', 'Health Records', 'Appointments', 'Users']
sizes = [num_clients, num_health_records, num_appointments, num_users]
colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']
explode = (0.1, 0, 0, 0)  # explode the first slice (Clients)

ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
ax2.set_title('Distribution of Clients, Health Records, Appointments, and Users')

# Show the combined plots
plt.tight_layout()
plt.show()