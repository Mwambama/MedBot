# import tkinter as tk
# import socket
# import matplotlib.pyplot as plt

# # Set the IP address and Port of the CyBot server
# HOST = "192.168.1.1"  # IP address of the CyBot server
# PORT = 288            # Port number for CyBot server

# Function to send a command to the CyBot server and receive data

        # testing with a for loop insteand of a while loop in order to handle the scan fucntion from scanning while not breaking

                                 
# def send_command(command):

#     try:

#         # Create a TCP socket and connect to the CyBot server

#         cybot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#         cybot_socket.connect((HOST, PORT))

#         # Send the command to the CyBot

#         cybot_socket.sendall(command.encode())

#         if command == 'h':

#             # Open the file to store scan data

#             with open("hello.txt", "w") as file:

#                 # Use a for loop to collect 180 data points

#                 for _ in range(180):

#                     # Receive a single line of scan data

#                     scan_data = cybot_socket.recv(1024).decode().strip()

#                     # Write valid data to the file

#                     if "Angle" in scan_data and "IR Distance" in scan_data:

#                         file.write(scan_data + "\n")

#             # Update feedback label

#             feedback_label.config(text="Scan completed. Press 'Display Graph' to view results.")

#         else:

#             # Handle other commands

#             feedback_label.config(text=f"Command '{command}' sent")

#         # Close the connection after communication

#         cybot_socket.close()

#     except Exception as e:

#         feedback_label.config(text=f"Connection failed: {e}")









         



















# this one removes the cappped distance and the scan button being displaed on the initial screen

#this is useless but scans some times 

#we can use this to display the objects detected like in putty, this is still needed but not for demo

# import tkinter as tk
# import socket
# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle
# from matplotlib.animation import FuncAnimation
# import math

# # Set the IP address and Port of the CyBot server
# HOST = "192.168.1.1"  # IP address of the CyBot server
# PORT = 288            # Port number for CyBot server

# # Global variables for scan data
# angles = []
# distances = []

# # Distance cap for filtering
# DISTANCE_CAP = 70

# # Function to calculate object positions for visualization
# def calculate_positions(angles, distances):
#     positions = []
#     for angle, distance in zip(angles, distances):
#         if distance < DISTANCE_CAP:  # Only include valid distances
#             x = distance * math.cos(math.radians(angle))
#             y = distance * math.sin(math.radians(angle))
#             positions.append((x, y))
#     return positions

# # Function to send a command to the CyBot server and receive data
# def send_command(command):
#     global angles, distances
#     try:
#         # Create a TCP socket and connect to the CyBot server
#         cybot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         cybot_socket.settimeout(10)  # Set a timeout to avoid indefinite hanging
#         cybot_socket.connect((HOST, PORT))

#         # Send the command to the CyBot
#         cybot_socket.sendall(command.encode())

#         if command == 'h':  # If the command is for scanning
#             print("Starting scan...")
#             feedback_label.config(text="Scanning in progress...")
            
#             angles.clear()
#             distances.clear()

#             buffer = ""
#             while True:
#                 try:
#                     # Receive data and append to the buffer
#                     data = cybot_socket.recv(1024).decode()
#                     buffer += data

#                     # Process each complete line in the buffer
#                     lines = buffer.split('\n')
#                     buffer = lines[-1]  # Save the last partial line (if any)

#                     for line in lines[:-1]:  # Process complete lines
#                         if "Angle" in line and "IR Distance" in line:
#                             try:
#                                 parts = line.split(',')
#                                 angle = int(parts[0].split(":")[1].strip())
#                                 distance = float(parts[1].split(":")[1].strip())
#                                 angles.append(angle)
#                                 distances.append(distance)
#                                 print(f"Angle: {angle}, Distance: {distance}")
#                             except (ValueError, IndexError):
#                                 print(f"Skipped malformed line: {line}")
#                                 continue

#                         # Update feedback on GUI
#                         feedback_label.config(text=f"Scanning... Last: {line}")

#                 except socket.timeout:
#                     print("Scan timed out.")
#                     feedback_label.config(text="Scan timed out.")
#                     break

#             feedback_label.config(text="Scan completed.")
#         else:
#             feedback_label.config(text=f"Command '{command}' sent.")

#         cybot_socket.close()

#     except Exception as e:
#         print(f"Connection failed: {e}")
#         feedback_label.config(text=f"Connection failed: {e}")

# # Function to update the live plot
# def update_plot(frame, ax, circles):
#     global angles, distances

#     if len(angles) > 0 and len(distances) > 0:
#         # Calculate positions
#         positions = calculate_positions(angles, distances)

#         # Remove existing circles
#         for circle in circles:
#             circle.remove()
#         circles.clear()

#         # Add circles for each detected object
#         for x, y in positions:
#             circle = Circle((x, y), 5, color="cyan", fill=False, linewidth=2)  # Circle radius = 5 cm
#             ax.add_patch(circle)
#             circles.append(circle)

#         ax.figure.canvas.draw()

# # Create the main application window
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")  # Set window size
# root.configure(bg="#1f1f2e")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"), bg="#1f1f2e", fg="#00d1b2")
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root, bg="#1f1f2e")
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1, padx=10, pady=5)

# button_left = tk.Button(movement_frame, text="<", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0, padx=10, pady=5)

# button_right = tk.Button(movement_frame, text=">", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2, padx=10, pady=5)

# button_down = tk.Button(movement_frame, text="v", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1, padx=10, pady=5)

# mode_frame = tk.Frame(root, bg="#1f1f2e")
# mode_frame.pack(pady=20)

# def toggle_mode():
#     global current_mode
#     send_command('t')
#     if current_mode == "Manual":
#         current_mode = "Scan"
#         feedback_label.config(text="Switched to Scan Mode", fg="#00d1b2")
#         mode_button.config(text="Switch to Manual Mode", bg="#ff79c6")
#         movement_frame.pack_forget()
#         scan_button.pack(pady=10)
#     else:
#         current_mode = "Manual"
#         feedback_label.config(text="Switched to Manual Mode", fg="#00d1b2")
#         mode_button.config(text="Switch to Scan Mode", bg="#44475a")
#         movement_frame.pack(pady=20)
#         scan_button.pack_forget()

# current_mode = "Manual"

# mode_button = tk.Button(mode_frame, text="Switch to Scan Mode", font=("Helvetica", 16), bg="#44475a", fg="white", command=toggle_mode)
# mode_button.pack()

# scan_button = tk.Button(root, text="Scan", font=("Helvetica", 20), bg="#ff79c6", fg="white", command=lambda: send_command('h'))
# scan_button.pack_forget()  # Hide initially

# feedback_label = tk.Label(root, text="Manual Mode Active", font=("Helvetica", 16), bg="#1f1f2e", fg="#00d1b2")
# feedback_label.pack(pady=10)

# # Live Graph Visualization
# fig, ax = plt.subplots()
# ax.set_facecolor("#1f1f2e")
# ax.set_title("Scanned Area Visualization", color="white")
# ax.set_xlim(-150, 150)
# ax.set_ylim(-150, 150)
# ax.set_xlabel("X (cm)", color="white")
# ax.set_ylabel("Y (cm)", color="white")
# ax.tick_params(colors="white")

# circles = []
# ani = FuncAnimation(fig, update_plot, fargs=(ax, circles), interval=500)

# plt.show(block=False)

# root.mainloop()




                                                            #USE THIS CODE  FOR THE DISTANCES WHEN IMPLEMENTING THE LAST CODE i JUST USE  WHCIH WORKS GOOD





# display distance and allow multiple scans
# this has the display live after scanning

# this seems to work, this is the last one, the SAN WORKS HERE, use this one for demo #1


# import tkinter as tk
# import socket
# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle
# from matplotlib.animation import FuncAnimation
# import math

# # Set the IP address and Port of the CyBot server
# HOST = "192.168.1.1"  # IP address of the CyBot server
# PORT = 288            # Port number for CyBot server

# # Global variables for scan data
# angles = []
# distances = []

# # Distance cap for filtering
# DISTANCE_CAP = 70

# # Function to calculate object positions for visualization
# def calculate_positions(angles, distances):
#     positions = []
#     for angle, distance in zip(angles, distances):
#         if distance < DISTANCE_CAP:  # Only include valid distances
#             x = distance * math.cos(math.radians(angle))
#             y = distance * math.sin(math.radians(angle))
#             positions.append((x, y))
#     return positions

# # Function to identify and summarize detected objects
# def identify_objects(positions):
#     objects = []
#     for i, (x, y) in enumerate(positions):
#         objects.append(f"Object {i+1}: X = {x:.1f} cm, Y = {y:.1f} cm")
#     return objects

# # Function to calculate distances between detected objects
# def calculate_distances(positions):
#     distances = []
#     for i in range(len(positions) - 1):
#         x1, y1 = positions[i]
#         x2, y2 = positions[i + 1]
#         distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#         distances.append(distance)
#     return distances

# # Function to send a command to the CyBot server and receive data
# def send_command(command):
#     global angles, distances
#     try:
#         # Create a TCP socket and connect to the CyBot server
#         cybot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         cybot_socket.settimeout(10)  # Set a timeout to avoid indefinite hanging
#         cybot_socket.connect((HOST, PORT))

#         # Send the command to the CyBot
#         cybot_socket.sendall(command.encode())

#         if command == 'h':  # If the command is for scanning
#             print("Starting scan...")
#             feedback_label.config(text="Scanning in progress...")
            
#             angles.clear()
#             distances.clear()

#             buffer = ""
#             while True:
#                 try:
#                     # Receive data and append to the buffer
#                     data = cybot_socket.recv(1024).decode()
#                     if not data:  # Exit if no more data
#                         break
#                     buffer += data

#                     # Process each complete line in the buffer
#                     lines = buffer.split('\n')
#                     buffer = lines[-1]  # Save the last partial line (if any)

#                     for line in lines[:-1]:  # Process complete lines
#                         if "Angle" in line and "IR Distance" in line:
#                             try:
#                                 parts = line.split(',')
#                                 angle = int(parts[0].split(":")[1].strip())
#                                 distance = float(parts[1].split(":")[1].strip())
#                                 angles.append(angle)
#                                 distances.append(distance)
#                                 print(f"Angle: {angle}, Distance: {distance}")
#                             except (ValueError, IndexError):
#                                 print(f"Skipped malformed line: {line}")
#                                 continue

#                         # Update feedback on GUI
#                         feedback_label.config(text=f"Scanning... Last: {line}")

#                 except socket.timeout:
#                     print("Scan timed out.")
#                     feedback_label.config(text="Scan timed out.")
#                     break

#             # Process detected objects
#             positions = calculate_positions(angles, distances)
#             detected_objects = identify_objects(positions)
#             if detected_objects:
#                 print("\nDetected Objects:")
#                 for obj in detected_objects:
#                     print(obj)
#                 feedback_label.config(text=f"Detected {len(detected_objects)} objects.")
#             else:
#                 print("\nNo objects detected.")
#                 feedback_label.config(text="No objects detected.")

#         else:
#             feedback_label.config(text=f"Command '{command}' sent.")

#         cybot_socket.close()

#     except Exception as e:
#         print(f"Connection failed: {e}")
#         feedback_label.config(text=f"Connection failed: {e}")

# # Function to update the live plot
# def update_plot(frame, ax, circles, distances_texts):
#     global angles, distances

#     if len(angles) > 0 and len(distances) > 0:
#         # Calculate positions
#         positions = calculate_positions(angles, distances)

#         # Remove existing circles and texts
#         for circle in circles:
#             circle.remove()
#         circles.clear()

#         for text in distances_texts:
#             text.remove()
#         distances_texts.clear()

#         # Add circles for each detected object
#         for x, y in positions:
#             circle = Circle((x, y), 5, color="cyan", fill=False, linewidth=2)  # Circle radius = 5 cm
#             ax.add_patch(circle)
#             circles.append(circle)

#         # Calculate and display distances between objects
#         object_distances = calculate_distances(positions)
#         for i, distance in enumerate(object_distances):
#             x1, y1 = positions[i]
#             x2, y2 = positions[i + 1]
#             mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2  # Midpoint between objects
#             text = ax.text(mid_x, mid_y, f"{distance:.1f} cm", color="yellow", fontsize=8)
#             distances_texts.append(text)

#         ax.figure.canvas.draw()

# # Create the main application window
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")  # Set window size
# root.configure(bg="#1f1f2e")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"), bg="#1f1f2e", fg="#00d1b2")
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root, bg="#1f1f2e")
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1, padx=10, pady=5)

# button_left = tk.Button(movement_frame, text="<", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0, padx=10, pady=5)

# button_right = tk.Button(movement_frame, text=">", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2, padx=10, pady=5)

# button_down = tk.Button(movement_frame, text="v", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1, padx=10, pady=5)

# mode_frame = tk.Frame(root, bg="#1f1f2e")
# mode_frame.pack(pady=20)

# def toggle_mode():
#     global current_mode
#     send_command('t')
#     if current_mode == "Manual":
#         current_mode = "Scan"
#         feedback_label.config(text="Switched to Scan Mode", fg="#00d1b2")
#         mode_button.config(text="Switch to Manual Mode", bg="#ff79c6")
#         movement_frame.pack_forget()
#         scan_button.pack(pady=10)
#     else:
#         current_mode = "Manual"
#         feedback_label.config(text="Switched to Manual Mode", fg="#00d1b2")
#         mode_button.config(text="Switch to Scan Mode", bg="#44475a")
#         movement_frame.pack(pady=20)
#         scan_button.pack_forget()

# current_mode = "Manual"

# mode_button = tk.Button(mode_frame, text="Switch to Scan Mode", font=("Helvetica", 16), bg="#44475a", fg="white", command=toggle_mode)
# mode_button.pack()

# scan_button = tk.Button(root, text="Scan", font=("Helvetica", 20), bg="#ff79c6", fg="white", command=lambda: send_command('h'))
# scan_button.pack_forget()  # Hide initially

# feedback_label = tk.Label(root, text="Manual Mode Active", font=("Helvetica", 16), bg="#1f1f2e", fg="#00d1b2")
# feedback_label.pack(pady=10)



# # Live Graph Visualization
# fig, ax = plt.subplots()
# ax.set_facecolor("#1f1f2e")
# ax.set_title("Scanned Area Visualization", color="white")
# ax.set_xlim(-150, 150)
# ax.set_ylim(-150, 150)
# ax.set_xlabel("X (cm)", color="white")
# ax.set_ylabel("Y (cm)", color="white")
# ax.tick_params(colors="white")

# circles = []
# distances_texts = []
# ani = FuncAnimation(fig, update_plot, fargs=(ax, circles, distances_texts), interval=500)

# plt.show(block=False)

# root.mainloop()









































# new changes  after implementing sending the lcd_manual to putty, these new changes did not work
# this works but not no gui, the scan works,  this shows no data in the terminal and the screen is white , we will use this testing #2


# import tkinter as tk
# import socket
# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle
# import math

# # Server Configuration
# HOST = "192.168.1.1"
# PORT = 288

# # Global Variables
# angles = []
# distances = []
# detected_objects = []

# # Distance Thresholds
# DISTANCE_THRESHOLD = 70  # cm
# ANGLE_GAP_THRESHOLD = 5  # degrees

# # Process Scanned Data into Objects
# def process_scan_data(angles, distances):
#     global detected_objects
#     detected_objects.clear()

#     current_object = {"start_angle": None, "end_angle": None, "distance": None}
#     in_object = False

#     for i, distance in enumerate(distances):
#         if distance < DISTANCE_THRESHOLD:
#             if not in_object:
#                 in_object = True
#                 current_object["start_angle"] = angles[i]
#                 current_object["distance"] = distance
#             current_object["end_angle"] = angles[i]
#         else:
#             if in_object:
#                 detected_objects.append(current_object.copy())
#                 in_object = False

#     # Finalize last object
#     if in_object:
#         detected_objects.append(current_object)

#     print("Detected Objects:")
#     for obj in detected_objects:
#         print(f"Start Angle: {obj['start_angle']}, End Angle: {obj['end_angle']}, Distance: {obj['distance']} cm")

# # Command to Server
# def send_command(command):
#     global angles, distances
#     try:
#         # Connect to the server
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cybot_socket:
#             cybot_socket.settimeout(10)
#             cybot_socket.connect((HOST, PORT))
#             cybot_socket.sendall(command.encode())

#             if command == 'h':  # Scan Command
#                 print("Scanning...")
#                 angles.clear()
#                 distances.clear()

#                 buffer = ""
#                 while True:
#                     try:
#                         data = cybot_socket.recv(1024).decode()
#                         if not data:
#                             break
#                         buffer += data
#                         lines = buffer.split('\n')
#                         buffer = lines[-1]

#                         for line in lines[:-1]:
#                             if "Angle" in line and "IR Distance" in line:
#                                 try:
#                                     parts = line.split(',')
#                                     angle = int(parts[0].split(":")[1].strip())
#                                     distance = float(parts[1].split(":")[1].strip())
#                                     angles.append(angle)
#                                     distances.append(distance)
#                                     print(line)
#                                 except ValueError:
#                                     continue

#                     except socket.timeout:
#                         print("Scan completed.")
#                         break

#                 process_scan_data(angles, distances)

#             else:
#                 print(f"Command '{command}' sent.")

#     except Exception as e:
#         print(f"Error: {e}")

# # GUI for Control
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"))
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root)
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1)

# button_left = tk.Button(movement_frame, text="<", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0)

# button_right = tk.Button(movement_frame, text=">", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2)

# button_down = tk.Button(movement_frame, text="v", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1)

# scan_button = tk.Button(root, text="Scan", command=lambda: send_command('h'))
# scan_button.pack(pady=10)

# root.mainloop()








  # scanning does not work
# import tkinter as tk
# import socket
# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle
# import math

# # Server Configuration
# HOST = "192.168.1.1"
# PORT = 288

# # Global Variables
# angles = []
# distances = []
# detected_objects = []

# # Distance Thresholds
# DISTANCE_THRESHOLD = 70  # cm
# ANGLE_GAP_THRESHOLD = 5  # degrees

# # Process Scanned Data into Objects
# def process_scan_data(angles, distances):
#     global detected_objects
#     detected_objects.clear()

#     current_object = {"start_angle": None, "end_angle": None, "distance": None}
#     in_object = False

#     for i, distance in enumerate(distances):
#         if distance < DISTANCE_THRESHOLD:
#             if not in_object:
#                 in_object = True
#                 current_object["start_angle"] = angles[i]
#                 current_object["distance"] = distance
#             current_object["end_angle"] = angles[i]
#         else:
#             if in_object:
#                 detected_objects.append(current_object.copy())
#                 in_object = False

#     # Finalize last object
#     if in_object:
#         detected_objects.append(current_object)

#     print("Detected Objects:")
#     for obj in detected_objects:
#         print(f"Start Angle: {obj['start_angle']}, End Angle: {obj['end_angle']}, Distance: {obj['distance']} cm")

# # Command to Server
# def send_command(command):
#     global angles, distances
#     try:
#         # Connect to the server
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cybot_socket:
#             cybot_socket.settimeout(10)
#             cybot_socket.connect((HOST, PORT))
#             cybot_socket.sendall(command.encode())

#             if command == 'h':  # Scan Command
#                 print("Scanning...")
#                 angles.clear()
#                 distances.clear()

#                 buffer = ""
#                 while True:
#                     try:
#                         data = cybot_socket.recv(1024).decode()
#                         if not data:
#                             break
#                         buffer += data
#                         lines = buffer.split('\n')
#                         buffer = lines[-1]

#                         for line in lines[:-1]:
#                             if "Angle" in line and "IR Distance" in line:
#                                 try:
#                                     parts = line.split(',')
#                                     angle = int(parts[0].split(":")[1].strip())
#                                     distance = float(parts[1].split(":")[1].strip())
#                                     angles.append(angle)
#                                     distances.append(distance)
#                                     print(line)
#                                 except ValueError:
#                                     continue

#                     except socket.timeout:
#                         print("Scan completed.")
#                         break

#                 process_scan_data(angles, distances)

#             else:
#                 print(f"Command '{command}' sent.")

#     except Exception as e:
#         print(f"Error: {e}")

# # GUI for Control
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"))
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root)
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1)

# button_left = tk.Button(movement_frame, text="<", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0)

# button_right = tk.Button(movement_frame, text=">", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2)

# button_down = tk.Button(movement_frame, text="v", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1)

# scan_button = tk.Button(root, text="Scan", command=lambda: send_command('h'))
# scan_button.pack(pady=10)

# root.mainloop()







# the command for manualos works good




# import tkinter as tk
# import socket
# import math

# # Set the IP address and Port of the CyBot server
# HOST = "192.168.1.1"  # IP address of the CyBot server
# PORT = 288            # Port number for CyBot server

# # Global variables for scan data
# angles = []
# distances = []
# detected_objects = []

# # Distance threshold for object detection
# DISTANCE_THRESHOLD = 70

# def calculate_positions(angles, distances):
#     """Convert polar coordinates (angle, distance) to Cartesian coordinates (x, y)."""
#     positions = []
#     for angle, distance in zip(angles, distances):
#         if distance < DISTANCE_THRESHOLD:
#             x = distance * math.cos(math.radians(angle))
#             y = distance * math.sin(math.radians(angle))
#             positions.append((x, y))
#     return positions

# def detect_objects(angles, distances):
#     """Identify objects based on sequential angles and distances."""
#     objects = []
#     current_object = None

#     for i, (angle, distance) in enumerate(zip(angles, distances)):
#         if distance < DISTANCE_THRESHOLD:
#             if not current_object:
#                 current_object = {"start_angle": angle, "end_angle": angle, "distance": distance}
#             else:
#                 current_object["end_angle"] = angle
#                 current_object["distance"] = max(current_object["distance"], distance)
#         elif current_object:
#             objects.append(current_object)
#             current_object = None

#     if current_object:
#         objects.append(current_object)
    
#     return objects

# def display_detected_objects(objects):
#     """Print details of detected objects and highlight the largest one."""
#     print("\nDetected Objects:")
#     print("Object\tStart Angle\tEnd Angle")
#     print("--------------------------------")
#     for i, obj in enumerate(objects):
#         print(f"{i+1}\t{obj['start_angle']}\t\t{obj['end_angle']}")

#     if objects:
#         largest_object = max(objects, key=lambda o: o["end_angle"] - o["start_angle"])
#         print("\nLargest object detected:")
#         print(f"Start Angle: {largest_object['start_angle']}, "
#               f"End Angle: {largest_object['end_angle']}, "
#               f"Distance: {largest_object['distance']} cm")
#         print("Press 'h' again to move towards the largest object.")

# def send_command(command):
#     """Send a command to the CyBot server and process the response."""
#     global angles, distances, detected_objects
#     try:
#         # Connect to the CyBot server
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cybot_socket:
#             cybot_socket.settimeout(10)
#             cybot_socket.connect((HOST, PORT))
#             cybot_socket.sendall(command.encode())

#             if command == 'h':  # Scan command
#                 print("Starting scan...")
#                 feedback_label.config(text="Scanning in progress...")
                
#                 angles.clear()
#                 distances.clear()
#                 buffer = ""

#                 while True:
#                     try:
#                         data = cybot_socket.recv(1024).decode()
#                         if not data:
#                             break
#                         buffer += data
#                         lines = buffer.split("\n")
#                         buffer = lines[-1]  # Preserve incomplete line

#                         for line in lines[:-1]:
#                             if "Angle" in line and "IR Distance" in line:
#                                 try:
#                                     parts = line.split(',')
#                                     angle = int(parts[0].split(":")[1].strip())
#                                     distance = float(parts[1].split(":")[1].strip())
#                                     angles.append(angle)
#                                     distances.append(distance)
#                                     print(f"Angle: {angle}, IR Distance: {distance}")
#                                 except (ValueError, IndexError):
#                                     continue

#                     except socket.timeout:
#                         print("Scan timed out.")
#                         feedback_label.config(text="Scan timed out.")
#                         break

#                 detected_objects = detect_objects(angles, distances)
#                 display_detected_objects(detected_objects)
#                 feedback_label.config(text="Scan completed. Check terminal for results.")

#             else:
#                 feedback_label.config(text=f"Command '{command}' sent.")

#     except Exception as e:
#         print(f"Connection failed: {e}")
#         feedback_label.config(text=f"Connection failed: {e}")

# # GUI Code
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")
# root.configure(bg="#1f1f2e")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"), bg="#1f1f2e", fg="#00d1b2")
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root, bg="#1f1f2e")
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1, padx=10, pady=5)

# button_left = tk.Button(movement_frame, text="<", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0, padx=10, pady=5)

# button_right = tk.Button(movement_frame, text=">", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2, padx=10, pady=5)

# button_down = tk.Button(movement_frame, text="v", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1, padx=10, pady=5)

# scan_button = tk.Button(root, text="Scan", font=("Helvetica", 20), bg="#ff79c6", fg="white", command=lambda: send_command('h'))
# scan_button.pack(pady=20)

# feedback_label = tk.Label(root, text="Manual Mode Active", font=("Helvetica", 16), bg="#1f1f2e", fg="#00d1b2")
# feedback_label.pack(pady=10)

# root.mainloop()








                                       # insteand of using the scanning the gui, I will use the command in putty as well but still recieve the feedback through poutty
                                                           #this does not have ther lcd_manual through, thus works okay




# import tkinter as tk
# import socket
# import math
# import threading

# # Set the IP address and Port of the CyBot server
# HOST = "192.168.1.1"  # Replace with your CyBot server IP
# PORT = 288            # Replace with your CyBot server Port

# # Global variables for scan data
# angles = []
# distances = []

# # Distance threshold for object detection
# DISTANCE_THRESHOLD = 70

# def calculate_positions(angles, distances):
#     """Convert polar coordinates (angle, distance) to Cartesian coordinates (x, y)."""
#     positions = []
#     for angle, distance in zip(angles, distances):
#         if distance < DISTANCE_THRESHOLD:
#             x = distance * math.cos(math.radians(angle))
#             y = distance * math.sin(math.radians(angle))
#             positions.append((x, y))
#     return positions

# def send_command(command):
#     """Send a command to the CyBot server and process the response."""
#     global angles, distances
#     try:
#         # Create a TCP socket
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cybot_socket:
#             cybot_socket.settimeout(10)
#             print(f"Connecting to {HOST}:{PORT}...")
#             cybot_socket.connect((HOST, PORT))
#             print("Connection established.")

#             # Send the command
#             cybot_socket.sendall(command.encode())
#             print(f"Command '{command}' sent.")

#             angles.clear()
#             distances.clear()

#             buffer = ""
#             while True:
#                 try:
#                     data = cybot_socket.recv(1024).decode()
#                     if not data:
#                         print("No more data from server.")
#                         break
#                     buffer += data

#                     # Process each complete line in the buffer
#                     lines = buffer.split("\n")
#                     buffer = lines[-1]  # Preserve the incomplete line

#                     for line in lines[:-1]:
#                         print(f"Received: {line}")  # Print received data to the terminal
#                         if "Angle" in line and "IR Distance" in line:
#                             try:
#                                 parts = line.split(',')
#                                 angle = int(parts[0].split(":")[1].strip())
#                                 distance = float(parts[1].split(":")[1].strip())
#                                 angles.append(angle)
#                                 distances.append(distance)
#                             except (ValueError, IndexError):
#                                 print(f"Skipped malformed line: {line}")
#                                 continue

#                         # Update feedback on GUI
#                         feedback_label.config(text=f"Last Received: {line}")

#                 except socket.timeout:
#                     print("Socket timeout reached.")
#                     break

#             print("Scan completed.")
#             print(f"Angles: {angles}")
#             print(f"Distances: {distances}")
#             feedback_label.config(text="Scan completed. Check terminal for results.")

#     except Exception as e:
#         print(f"Error: {e}")
#         feedback_label.config(text=f"Error: {e}")

# def handle_terminal_commands():
#     """Allow the user to input commands directly in the terminal."""
#     while True:
#         command = input("Enter command ('w', 'a', 's', 'd', 'h', etc.): ").strip()
#         if command:
#             send_command(command)

# # GUI Code
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")
# root.configure(bg="#1f1f2e")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"), bg="#1f1f2e", fg="#00d1b2")
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root, bg="#1f1f2e")
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1, padx=10, pady=5)

# button_left = tk.Button(movement_frame, text="<", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0, padx=10, pady=5)

# button_right = tk.Button(movement_frame, text=">", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2, padx=10, pady=5)

# button_down = tk.Button(movement_frame, text="v", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1, padx=10, pady=5)

# feedback_label = tk.Label(root, text="Manual Mode Active", font=("Helvetica", 16), bg="#1f1f2e", fg="#00d1b2")
# feedback_label.pack(pady=10)

# # Start a background thread for handling terminal input
# terminal_thread = threading.Thread(target=handle_terminal_commands, daemon=True)
# terminal_thread.start()

# root.mainloop()






                                                            #    this is perfect\, do no delete this, the best progress since the testing from putty
                                                            # this works and scan works, works like putty, manual works , we just need to display the GUI to see where we need to go


# import tkinter as tk
# import socket
# import threading

# # Set the IP address and Port of the CyBot server
# HOST = "192.168.1.1"  # Replace with your CyBot server IP
# PORT = 288            # Replace with your CyBot server Port

# # Function to send commands and receive data
# def send_command(command):
#     """Send a command to the CyBot server and process the response."""
#     try:
#         # Create a TCP socket
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cybot_socket:
#             cybot_socket.settimeout(10)
#             print(f"Connecting to {HOST}:{PORT}...")
#             cybot_socket.connect((HOST, PORT))
#             print("Connection established.")

#             # Send the command
#             cybot_socket.sendall(command.encode())
#             print(f"Command '{command}' sent.")

#             # Process server responses
#             while True:
#                 data = cybot_socket.recv(1024).decode()
#                 if not data:
#                     break
#                 print(data)  # Print server responses to the terminal
#                 feedback_label.config(text=data)  # Update GUI feedback label
#     except Exception as e:
#         print(f"Error: {e}")
#         feedback_label.config(text=f"Error: {e}")

# # Thread function for handling terminal input
# def terminal_input():
#     """Allow the user to input commands directly in the terminal."""
#     while True:
#         command = input("Enter command ('w', 'a', 's', 'd', 'h', etc.): ").strip()
#         if command:
#             send_command(command)

# # GUI Code
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")
# root.configure(bg="#1f1f2e")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"), bg="#1f1f2e", fg="#00d1b2")
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root, bg="#1f1f2e")
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1, padx=10, pady=5)

# button_left = tk.Button(movement_frame, text="<", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0, padx=10, pady=5)

# button_right = tk.Button(movement_frame, text=">", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2, padx=10, pady=5)

# button_down = tk.Button(movement_frame, text="v", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1, padx=10, pady=5)

# scan_button = tk.Button(root, text="Scan", font=("Helvetica", 20), bg="#ff79c6", fg="white", command=lambda: send_command('h'))
# scan_button.pack(pady=20)

# feedback_label = tk.Label(root, text="Manual Mode Active", font=("Helvetica", 16), bg="#1f1f2e", fg="#00d1b2")
# feedback_label.pack(pady=10)

# # Start the terminal input thread
# terminal_thread = threading.Thread(target=terminal_input, daemon=True)
# terminal_thread.start()

# root.mainloop()







import tkinter as tk
import socket
import threading

# Set the IP address and Port of the CyBot server
HOST = "192.168.1.1"  # Replace with your CyBot server IP
PORT = 288            # Replace with your CyBot server Port

# Function to send commands and receive data
def send_command(command):
    """Send a command to the CyBot server and process the response."""
    try:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cybot_socket:
            cybot_socket.settimeout(10)
            print(f"Connecting to {HOST}:{PORT}...")
            cybot_socket.connect((HOST, PORT))
            print("Connection established.")

            # Send the command
            cybot_socket.sendall(command.encode())
            print(f"Command '{command}' sent.")

            # Process server responses
            scan_results_text.delete('1.0', tk.END)  # Clear previous results
            while True:
                data = cybot_socket.recv(1024).decode()
                if not data:
                    break
                print(data)  # Print server responses to the terminal
                feedback_label.config(text=data)  # Update GUI feedback label
                scan_results_text.insert(tk.END, data + "\n")  # Append to scan results
                scan_results_text.see(tk.END)  # Scroll to the latest entry
    except Exception as e:
        print(f"Error: {e}")
        feedback_label.config(text=f"Error: {e}")

# Thread function for handling terminal input
def terminal_input():
    """Allow the user to input commands directly in the terminal."""
    while True:
        command = input("Enter command ('w', 'a', 's', 'd', 'h', etc.): ").strip()
        if command:
            send_command(command)

# GUI Code
root = tk.Tk()
root.title("MedBot Controller")
root.geometry("800x600")
root.configure(bg="#1f1f2e")

header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"), bg="#1f1f2e", fg="#00d1b2")
header_label.pack(pady=20)

movement_frame = tk.Frame(root, bg="#1f1f2e")
movement_frame.pack(pady=20)

button_up = tk.Button(movement_frame, text="^", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('w'))
button_up.grid(row=0, column=1, padx=10, pady=5)

button_left = tk.Button(movement_frame, text="<", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('a'))
button_left.grid(row=1, column=0, padx=10, pady=5)

button_right = tk.Button(movement_frame, text=">", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('d'))
button_right.grid(row=1, column=2, padx=10, pady=5)

button_down = tk.Button(movement_frame, text="v", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('s'))
button_down.grid(row=2, column=1, padx=10, pady=5)

scan_button = tk.Button(root, text="Scan", font=("Helvetica", 20), bg="#ff79c6", fg="white", command=lambda: send_command('h'))
scan_button.pack(pady=20)

feedback_label = tk.Label(root, text="Manual Mode Active", font=("Helvetica", 16), bg="#1f1f2e", fg="#00d1b2")
feedback_label.pack(pady=10)

# Text widget to display scan results
scan_results_frame = tk.Frame(root, bg="#1f1f2e")
scan_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scan_results_label = tk.Label(scan_results_frame, text="Scan Results:", font=("Helvetica", 16, "bold"), bg="#1f1f2e", fg="#00d1b2")
scan_results_label.pack(anchor="w")

scan_results_text = tk.Text(scan_results_frame, wrap=tk.WORD, font=("Helvetica", 12), bg="#2b2b3b", fg="white", height=15)
scan_results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Start the terminal input thread
terminal_thread = threading.Thread(target=terminal_input, daemon=True)
terminal_thread.start()

root.mainloop()







# import tkinter as tk
# import socket
# import threading

# # Set the IP address and Port of the CyBot server
# HOST = "192.168.1.1"  # Replace with your CyBot server IP
# PORT = 288            # Replace with your CyBot server Port

# # Function to send commands and receive data
# def send_command(command):
#     """Send a command to the CyBot server and process the response."""
#     try:
#         # Create a TCP socket
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cybot_socket:
#             cybot_socket.settimeout(10)
#             print(f"Connecting to {HOST}:{PORT}...")
#             cybot_socket.connect((HOST, PORT))
#             print("Connection established.")

#             # Send the command
#             cybot_socket.sendall(command.encode())
#             print(f"Command '{command}' sent.")

#             # Process server responses
#             scan_results_text.delete('1.0', tk.END)  # Clear previous results
#             while True:
#                 data = cybot_socket.recv(1024).decode()
#                 if not data:
#                     break
#                 print(data)  # Print server responses to the terminal
#                 feedback_label.config(text=data)  # Update GUI feedback label
#                 scan_results_text.insert(tk.END, data + "\n")  # Append to scan results
#                 scan_results_text.see(tk.END)  # Scroll to the latest entry
#     except Exception as e:
#         print(f"Error: {e}")
#         feedback_label.config(text=f"Error: {e}")

# # Thread function for handling terminal input
# def terminal_input():
#     """Allow the user to input commands directly in the terminal."""
#     while True:
#         command = input("Enter command ('w', 'a', 's', 'd', 'h', etc.): ").strip()
#         if command:
#             send_command(command)

# # GUI Code
# root = tk.Tk()
# root.title("MedBot Controller")
# root.geometry("800x600")
# root.configure(bg="#1f1f2e")

# header_label = tk.Label(root, text="MedBot Controller", font=("Helvetica", 24, "bold"), bg="#1f1f2e", fg="#00d1b2")
# header_label.pack(pady=20)

# movement_frame = tk.Frame(root, bg="#1f1f2e")
# movement_frame.pack(pady=20)

# button_up = tk.Button(movement_frame, text="^", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('w'))
# button_up.grid(row=0, column=1, padx=10, pady=5)

# button_left = tk.Button(movement_frame, text="<", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('a'))
# button_left.grid(row=1, column=0, padx=10, pady=5)

# button_right = tk.Button(movement_frame, text=">", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('d'))
# button_right.grid(row=1, column=2, padx=10, pady=5)

# button_down = tk.Button(movement_frame, text="v", font=("Helvetica", 20), bg="#44475a", fg="white", command=lambda: send_command('s'))
# button_down.grid(row=2, column=1, padx=10, pady=5)

# scan_button = tk.Button(root, text="Scan", font=("Helvetica", 20), bg="#ff79c6", fg="white", command=lambda: send_command('h'))
# scan_button.pack(pady=20)

# feedback_label = tk.Label(root, text="Manual Mode Active", font=("Helvetica", 16), bg="#1f1f2e", fg="#00d1b2")
# feedback_label.pack(pady=10)

# # Text widget to display scan results
# scan_results_frame = tk.Frame(root, bg="#1f1f2e")
# scan_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# scan_results_label = tk.Label(scan_results_frame, text="Scan Results:", font=("Helvetica", 16, "bold"), bg="#1f1f2e", fg="#00d1b2")
# scan_results_label.pack(anchor="w")

# scan_results_text = tk.Text(scan_results_frame, wrap=tk.WORD, font=("Helvetica", 12), bg="#2b2b3b", fg="white", height=15)
# scan_results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# # Start the terminal input thread
# terminal_thread = threading.Thread(target=terminal_input, daemon=True)
# terminal_thread.start()

# root.mainloop()



















