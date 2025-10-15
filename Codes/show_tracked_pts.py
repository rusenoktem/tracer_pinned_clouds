import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import time
import sys

#set paths
path_pic = '../Data/Pics_Figs_6_7/houstereocamaS5.a1.'
path_data = '../Data/track'
    

def seconds_to_hhmmss(total_seconds):
    """
    Converts an integer number of seconds from midnight into an 'hhmmss' string.

    Args:
        total_seconds (int): The number of seconds elapsed since midnight.

    Returns:
        str: The time in 'HHMMSS' format.
    """

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the components with leading zeros and concatenate
    return f"{hours:02}{minutes:02}{seconds:02}"
    
    
def display_figs(date_str, tmI, data, fig, ax):
    for i in range(len(tmI)):
        try:
            tmstr = seconds_to_hhmmss(int(tmI[i]))
            img = plt.imread(path_pic+ date_str +"."+tmstr+".jpg")
            

            
            ax.clear()
            ax.imshow(img)
            ax.axis('off') 
            ax.set_xlim(400, 2000)
            ax.set_ylim(1600, 1000) 

            # Overlay the 'X' sign at (x, y)
            x = data[i, 0]
            y = data[i, 1]
            
            ax.scatter(x, y, marker='x', 
                       s=20,      # size of the marker
                       color='white', linewidths=2)
            # Display tmstr as title of the plot
            ax.set_title(date_str+"-"+tmstr, fontsize=14)

            # Draw the updated plot
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.show()

            print(f"Displaying frame {i+1}/{len(tmI)}: {tmstr}")
            #Pause for 1 second
            time.sleep(1)

        except FileNotFoundError:
            print(f"Skipping frame {i+1}: Image not found at {tmstr}")
            continue # Move to the next iteration
        except Exception as e:
            print(f"An error occurred at frame {i+1}: {e}")
            break 
    

##################################################################
def main():
    #check input arguments
    if (len(sys.argv)<2):
        print('Usage: show_tracked_pts.py <YYYYMMDD>')
        print('e.g. python show_tracked_pts.py 20220622')
        sys.exit();
               
   
    #load data
    date_str = sys.argv[1]  # date, for example 20220622
    mat = scipy.io.loadmat(path_data+date_str+'.mat')  
    data = mat['data']
    tmI = mat['tmI']

    # Setup figure
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.ion() 
    display_figs(date_str, tmI, data, fig, ax)
    plt.ioff() # Turn off interactive mode
    plt.close(fig) # Close the figure 
    
main()
