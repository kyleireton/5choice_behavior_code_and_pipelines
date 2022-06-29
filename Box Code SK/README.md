# Getting started with pyOS5
## Requirements

python- 3.6

numpy

pandas

PyQt5

pyqtgraph

pyserial

Download the code zip or git clone from the link https://github.com/KaetzelLab/Operant-Box-Code. After Downloading Code, move required task files from task sub-folder (contains specific task files) to main task folder. GUI dropBox-menu shows task files only from main task folder.
## Operant-Box-Code
- #### gui  

       - GUI_Final.ui      # Qt Graphical user interface file 
       
       - Run_5CSRTT.py     # Graphical user interface for 5-choice serial reaction time test
      
       - Run_Ruleshift.py  # Graphical user interface for rule shift task

       - Run_DNMTP.py      # Graphical user interface for Delayed not matched to position
	    
       - Run_DMTP.py       # Graphical user interface for Delayed matched to position	
	    
       - Run_CPT.py        # Graphical user interface for Go or NoGo
- #### com           
       Serial communication and data logging
   
- #### config       
       Configuration files
   
- #### data         
       Behavioural data.   
    
- #### devices      
       pyControl hardware classes (uploaded to pyboard).
    
- #### pyControl    
       pyControl framework (uploaded to pyboard).
    
- #### tasks      

       - 5CSRTT     # Contains task protocol file for 5 choice serial reaction time test
      
       - Ruleshift  # Contains task protocol file for rule shift      

       - DNMTP      # Contains task protocol file for Delayed non-match to position test      
	    
       - DMTP       # Contains task protocol file for Delayed match to position test      	
	    
       - CPT        # Graphical user interface for Go or NoGo
               
### Controling task file using Graphical User Interface (GUI)
Opening GUI is straight forward, if python is added to PATH Environment variables simply double clicking on file, for example double click on "Run_5CSRTT.py" or open command prompt from the GUI folder type "python Run_5CSRTT.py" and enter.

<p align="left" width="100%">
    <img src="https://user-images.githubusercontent.com/71041273/112695379-3cb11e80-8e84-11eb-803f-27d213d97d6c.gif" width="800"/>
</p>



- Select the setup and connect all or connect individual box by clicking connect
- Click Config_all or config to upload frame work and hardware definition both files are located in config folder. For instance, assuming that all the hardware setups are similar to pyOS5 then press hardware definition and select “pyOS5_HardwareDefinition.py”.
- Select task file from the drop menu and upload, User can upload different task files to different box in same GUI individually or can Upload same task file to all connected box from common drop menu located at bottom left of the GUI.
- Typing experiment name, project and session are optional but subject id is important to store and save individual csv files (contains all events and timestamps), If you entered subject id, start button will turn to Record. One can change variables from the GUI by clicking variable button before Start/Record.
- Once experiment is done, export data and reset data table by clicking Reset table.
- If you are using multiple boxes it is more convenient to add com numbers to port_list.py file to specific box order and later, it can be called by clicking setup button. This can store upto 24 com serial numbers.




## Task Protocols

### 5-Choice Serial Reaction Time Test (5CSRTT)

<p align="center" width="100%">
    <img src="https://user-images.githubusercontent.com/71041273/112722935-775e9980-8f0c-11eb-8351-2931762a965a.gif" width="400"/> 
</p>









### 5-Choice Delayed non-match to position test (DNMTP)
<img src="https://user-images.githubusercontent.com/71041273/112693334-bf37df00-8e80-11eb-808b-83b1ce577970.jpg" width="800"/>






### 2-Choice Delayed match to position test (DMTP)
<img src="https://user-images.githubusercontent.com/71041273/112693471-f9a17c00-8e80-11eb-95a1-c2a62427503c.jpg" width="800"/>

### Forward learning and Ruleshift (RuleShift)
##### forward learning
<img src="https://user-images.githubusercontent.com/71041273/112697062-2789bf00-8e87-11eb-8235-190f3b580ae6.jpg" width="800"/>




##### 2-Choice Rule shift 
<img src="https://user-images.githubusercontent.com/71041273/112722977-a543de00-8f0c-11eb-8bf8-9e49a6c26180.jpg" width="800"/>






To learn more about pyControl hardware, framework and create more variety task files visit and download pyControl from https://github.com/pyControl

### Contributors
#### Operant box system
- Dennis Kaetzel - dennis.kaetzel@uni-ulm.de
#### pyControl
- Thomas Akam  - thomas.akam@psy.ox.ac.uk 
#### pyOS5 GUI, task files
- Sampath Kumar  - sampath.kapanaiah@uni-ulm.de




### Citations
- Teutsch, J. & Kätzel, D. Operant Assessment of DMTP Spatial Working Memory in Mice. Front. Behav. Neurosci. 13, (2019).
    
