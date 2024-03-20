import sys, json
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

frames = {}
trajectories = {}

def process_entire_frame(line, frame):
    entries = {}
    
    items = line[line.find(' '):].split(",")
    items.pop() # Remove empty entry
    
    for item in items:
        clean_item = item.strip()
        value_key = clean_item.split()
        if len(value_key) == 2:
            new_value = value_key[0];
            new_key = value_key[1];
            entries[new_key] = new_value
    
    frames[f"frame_{frame}"] = entries                       

def process_individual(key):
    if key not in trajectories:
        trajectories[key] = []
    
def process_trajectories(line, key):
    new_coordinate = line[line.find(':') + 2:].strip().strip("()")
    
    numbers = [num.strip() for num in new_coordinate.split(",")]
    new_tuple = tuple(map(int, numbers))
    
    coordinates = trajectories.get(key)
    
    coordinates.append(new_tuple)
    trajectories[key] = coordinates

if len(sys.argv) > 1:
    input_file = sys.argv[1]  
    output_file = input_file[:input_file.find('.')]

    with open(input_file, "r") as file:
        frame = 0
        key = 0
        for line in file:
            if "384x640" in line:
                frame += 1
                process_entire_frame(line, frame)
            elif "Center:" in line:  
                process_trajectories(line, key)
            else:
                key = line[:line.find(':')]
                if key != '':
                    process_individual(key)
else:
    print("No text file provided!")

# print(frames)
# print(trajectories)

print(f"\nOutputting frames to ./{output_file}_frames.json")
json_string = json.dumps(frames)
with open(f"{output_file}_frames.json", "w") as f:
  f.write(json_string)

print(f"Outputting trajectories to ./{output_file}_trajectories.json")
json_string = json.dumps(trajectories)
with open(f"{output_file}_trajectories.json", "w") as f:
  f.write(json_string)
  
cmap = plt.colormaps['inferno']  
norm = plt.Normalize(vmin=0, vmax=len(trajectories)-1)

plt.figure(figsize=(5500/600, 3000/600))
for i, (key, array) in enumerate(trajectories.items()):
  x, y = zip(*array)  # Unpack coordinates from the array
  color = cmap(norm(i))  # Get color based on index and normalization
  plt.plot(x, y, label=key, color=color)  # Use key for label

# Add labels and title
plt.title(output_file)

print(f"Outputting plot to ./{output_file}_plot.png")  
plt.savefig(f"{output_file}_plot.png")

print("\nFIN")

