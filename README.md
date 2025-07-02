# tracer_pinned_clouds
Below is a description of the python and Matlab scripts to generate Figures 2-6 in manuscript "Pinned clouds over industrial sources of heat during TRACER" by R. Oktem, S. E. Giangrande, and D. M. Romps. Send email to rusenoktem@berkeley.edu for questions.

make_fig2.m: 
This matlab script uses data stored in Data/yearlong_pccp.mat to generate Figure 2. yearlong_pccp.mat can be arranged by using the output of collect_yearlong_pccp.py.

collect_yearlong_pccp.py:
This python script collects pccp data by going over all PCCP nc files stored in the ARM Data Center for TRACER (HOU). I executed this python script in ARM Jypiter hub, therefore data path names are arranged accordingly. You may need to download all PCCP files from the ARM Data Center (https://doi.org/10.5439/1531325) and modify the path names accordingly if you want to generate the output yourself.

make_fig3.m: 
This script uses images cropped from originals and the map obtained from Google Earth to generate Figure 3. The image and map files are located under the Data folder. Plant data are extracted from the EIData.xlsx file that is also under the Data folder. The file is provided by the Texas Commission on Environmental Quality upon our inquiry. 

make_fig4.m: 
This script generates Figure 4 using the algorithm explained in Section 3.c. The script uses the following data and script files:
- The cloud classification information is stored in Data/tracer_cloud_classes.mat. 
- LCL calculation code that is available at https://romps.berkeley.edu/papers/pubs-2016-lcl.html
- minbnd built-in Matlab function as the root solver.
- Radiosonde data that can be downloaded from the ARM data center https://doi.org/10.5439/1595321

make_fig5.py and make_fig5.py: 
The two scripts use PCPCP data that we generated using a modified version of the PCCP code. The data for each of the 14 days listed in Table 1 are placed under the Data folder. 
