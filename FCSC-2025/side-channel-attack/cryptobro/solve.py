import numpy as np
import matplotlib.pyplot as plt

# Path to the folder containing trace files
folder_path = './traces'

# Number of files, assuming the pins go from 0001 to 9999
pin_range = [9460, 9461, 9462, 9463, 9464, 9465, 9466, 9467, 9468, 9469]  # Pin numbers from 0001 to 9999

# Prepare a figure for plotting
plt.figure(figsize=(10, 6))

# Loop through each pin number and load the corresponding file
for pin in pin_range:
    # Format the pin number as a 4-digit string (e.g., 1 -> '0001', 100 -> '0100')
    pin_str = f"{pin:04d}"
    
    # Construct the filename using the pin number
    file_path = f'{folder_path}/trace_{pin_str}.npy'
    
    try:
        # Load the numpy array from the file
        data = np.load(file_path)
        
        # Plot the data and use the pin number as the label
        plt.plot(data, label=f'Pin {pin_str}')
    except FileNotFoundError:
        # If the file doesn't exist, skip it
        print(f"File {file_path} not found, skipping.")

# Add labels and title to the plot
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Trace Data from All Files')
plt.legend(loc='upper right', bbox_to_anchor=(1.05, 1))

# Display the plot
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent clipping of the legend
plt.show()
