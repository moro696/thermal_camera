from flirpy.camera.lepton import Lepton
import matplotlib.pyplot as plt
import numpy as np

with Lepton() as camera:
    print("Camera On.")
    
    plt.ion() 
    fig, ax = plt.subplots(figsize=(10, 8), layout="constrained")
    fig.canvas.manager.set_window_title('FLIR Lepton - Dinamic scale deg/Celsius')
    
    # Reading the first frame to find out the sensor`s resolution (Lepton 3.5 has 160x120)
    img_raw = camera.grab()
    if img_raw is not None:
        h, w = img_raw.shape
        cx, cy = w // 2, h // 2 # Central point cordinates
        
        # Converting first frame for initialisation
        img_celsius = (img_raw / 100.0) - 273.15
        
        # Show initial image with limits based on the first frame 
        im_display = ax.imshow(img_celsius, cmap='inferno', vmin=img_celsius.min(), vmax=img_celsius.max()) 
        cbar = plt.colorbar(im_display, ax=ax)
        cbar.set_label('Temperature (°C)')
        
        # Draw the taget ( red dot and two small lines for the crosair)
        target_dot, = ax.plot(cx, cy, 'ro', markersize=4)
        target_line1, = ax.plot([cx-5, cx+5], [cy, cy], 'r-', linewidth=1)
        target_line2, = ax.plot([cx, cx], [cy-5, cy+5], 'r-', linewidth=1)
        
        # Add temperature text info above the crossair 
        temp_text = ax.text(cx, cy - 8, '', color='white', fontweight='bold',
                            ha='center', va='center', 
                            bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    while plt.fignum_exists(fig.number):
        img_raw = camera.grab()
        if img_raw is not None:
            # 1. Instant conversion all the matrice in deg Celsius
            img_celsius = (img_raw / 100.0) - 273.15
            
            # 2. Update the background image
            im_display.set_data(img_celsius)
            
            # Limits are automaticaly adjusted after min/max current values
            im_display.set_clim(vmin=img_celsius.min(), vmax=img_celsius.max()) 
            
            # 3. Read the converted value from the center point of the matrice
            celsius_temp = img_celsius[cy, cx]
            
            # 4. Update the text with the current value 
            temp_text.set_text(f"{celsius_temp:.1f}°C")
            
            # Refresh the video screen
            plt.draw()
            plt.pause(0.01)
