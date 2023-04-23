**Cell counter manual**

Nynke Oosterhof – July 2022


**CITATION**


doi: https://doi.org/10.1101/2023.04.18.537159



**REFERENCES**


Stringer, C., Wang, T., Michaelos, M., & Pachitariu, M. (2021). Cellpose: a generalist algorithm for cellular segmentation. Nature methods, 18(1), 100-106. [bibtex]

Pachitariu, M. & Stringer, C. (2022). Cellpose 2.0: how to train your own model. Nature methods.

napari contributors (2019). napari: a multi-dimensional image viewer for python.







**Introduction**

Counting cells, especially in 3D closely packed tissue structures, can be particularly challenging. The most straightforward way would be to count cell nuclei, which are clearly recognizable by eye and for which in most cases only one is present per cell. However, in image of closely packed 3D structures, nuclei are often (almost) touching their neighbors, display differences in pixel intensities and are not always distinguishable from the background in the deeper images slices. The combination of these factors makes it almost impossible to reliably count cells in 3D images of closely packed cells using standard thresholding techniques. In the last few years several machine learning algorithms (e.g. StarDist and Cellpose) have made it possible to properly segment nuclei in 3D images, which means it can also be used for analyzing cell numbers in for example the developing zebrafish brain.

The Python code explained in this manual allows for some data organization, image preprocessing and cell counting in (parts of ) 3D tissue structures using the Cellpose algorithm. The preprocessing functionality is mostly focused on the correction of drops in image intensity in the deeper z-slices compared to more superficial z-slices and on sharpening the outlines of the nuclei. The counting of cells is based on the output of the Cellpose algorithm. The output of the Cellpose algorithm used in this script is the label map, which is an image in which each nucleus has its own unique pixel value. These label maps can be used to count all cells in an image or subsets thereof based on regional position (by multiplying the label maps with image masks) or on pixel intensity values in one of the channels of the original image (using thresholds). 

![](image001.png)


**IMPORTANT: CHECK YOUR IMAGES AFTER EVERY STEP OF THE ANALYSIS TO MAKE SURE EVERYTHING HAS HAPPENED THE WAY YOU WANTED IT TO AND EVERYTHING HAS BEEN DONE CORRECTLY/ACCURATELY!!!!!**

**Setting up the working environment on the computer**

**Step 1:**

Install Python and an IDE (Integrated Development Environment) that allows you to write and run Python code. Examples of IDE’s that can be used are Visual Studio Code (VScode, explained in this manual) and Spyder. 

**NOTE: If Cellpose will not be run on a computer cluster, make sure to install Python 3.7. Later versions can cause unexplained errors while running Cellpose. With Python 3.7.8 there should not be any problems. Later Python 3.7 versions may work as well.**

Python:

<https://www.python.org/downloads/> 

![](image002.png)

To install that Python version, click on Python 3.7.8, scroll down and download the **Windows x86-64 executable installer** (windows) or the **macOS 64-bit installer** (Mac).

For windows, when executing the installer to install Python, make sure to tick the box saying ‘**Add Python to environment variables**’ in the advanced options. This will make it easier to follow the next step of the manual.

As extension, choose Python 3.7.8 as installed previously. To test installation of Python3, run “which python” in Terminal, which should give 3.7.8 as answer.


VScode:

<https://code.visualstudio.com/Download> --> Download page

<https://code.visualstudio.com/docs/python/python-tutorial> à instructions on how to set it up




**Step 2:**

To prevent the script from breaking, it is recommended to run it from a virtual environment. A virtual environment is a separate environment in which the required Python packages can be installed without them being influenced by versions of packages installed elsewhere. Sometimes it happens that different scripts or packages have different requirements regarding the versions of other packages that are required. By using virtual environments potential problems caused by different version requirements of packages can be prevented.

To set up a new virtual environment specific for this analysis, first create a new folder from which to run the analysis. It doesn’t matter where this folder is created or what name it is given. Then copy all the **.py** files necessary for the cell counting to this folder.

Next, start VScode and choose open folder, in either the starting screen or in the dropdown menu of file. Then pick the new folder that was created previously. When this folder is opened, there should be a terminal at the bottom of the screen.

![](image003.png)

If you ticked the box **Add Python to environment variables** in the Python installation wizard in step 1, make sure Python has been installed by typing **python** in the terminal and pressing ‘enter’. Python will be started in the terminal and it will look like this:

![](image004.png)

Exit Python by typing **exit()** and pressing ‘enter’ in Python.

If you didn’t tick the box **Add Python to environment variables**, you can check whether Python has been installed as follows. Look up where Python has been installed and copy the file path (to the folder in which there is a python.exe file). Then enter the following in the terminal and press ‘enter‘:

**cd “file path to python installation”** 

To make sure it works properly, type **./python.exe** and press ‘enter’. This should result in python being started inside the terminal (as shown in the figure above). If that works, exit python by typing **exit()** and pressing ‘enter’.

For Mac, type "**python3**" in the terminal and press ‘enter’ to test whether it's installed properly. Close by exit() and pressing ‘enter’.

Next, create a virtual Python environment by using one of the following commands in the terminal:

If **Add Python to environment variables** ticked:

**python –m venv path\_to\_folder\_from\_which\_file\_will\_be\_run\.venv** 

If **Add Python to environment variables** NOT ticked.

**./python.exe –m venv path\_to\_folder\_from\_which\_file\_will\_be\_run\.venv**

For Mac (OS10.14 or higher), follow the VSCode tutorial to install necessary packages. Essentially, you open Terminal to install homebrew (if not yet installed), then install pyenv through "brew install pyenv" (to enable handling different types of Python versions),then replace the 'endogeneously" installed 2.6 Python version on your OS by "pyenv install 3.7.8". You may have to update your XCodes as prompted in the Terminal window. You may also have to install venv using "pip3 install virtualenv". Then go to VSCode, and install the Python extensions as described in the VScode python tutorial.

Now the virtual environment has been created. VScode may ask whether this new virtual environment should be used for this folder. If so, click **yes**. In windows the virtual environment folder will be added to your newly created folder. On mac, it will be a hidden folder that will not be visible in Finder, but it is there.

If VScode doesn’t ask whether the new virtual environment should be used, make sure that it will be used for your code. You can do this by pressing **shift + ctrl + P**. A dropdown menu will appear at the top of the screen. Either type or select: **Select Interpreter**. If you click on that, you should see a list of python installations/virtual environments. Pick the one you just created. It is probably called **.venv** and has the file path that starts with a **.**

**Step 3:**

Create a new file inside the newly created folder and call it **test.py**. Inside this new file type **print(“hello”)** and then click with the right mouse button and choose to run the file in the interactive window. If everything works as intended, there should be a pop-window asking to install the ipykernel package. Agree to install it. Without this package, there will be no interactive window in which single lines of code can be run.

**Step 4:**

Install the packages required for all the code to work properly. These packages can be installed by running the following command in the interactive window:

**pip install package\_name**

Type it and then either press the ‘**play**’ button or press **shift + enter**.

The packages that need to be installed are:

**scikit-image**, **cellpose** (if not using the computer cluster), **numpy**, **pandas**, **matplotlib**, **read\_lif**

![](image005.png)


**Step 5:**

Make a new folder somewhere (NOT inside the folder containing the python scripts) and copy the raw imaging data to this new folder. If starting from a later point in the analysis, check which data needs to be available in this data folder depending from which step the analysis will be done. Add the required data as described in the figure showing the data organization.

**How to use the cell counter script**

All functionality of the script can be accessed from the **main.py** file. This file consists of three parts; the part where the required packages and pieces of code are imported, the part where the required parameters are specified and the part where the code can be executed. The options provided in this code include the extraction of image z-stacks from microscopy files, image preprocessing, (cellpose), and the counting of cellular subsets based on image masks or pixel intensity values. For the script to be able to perform all these operations on a dataset it is very important that all the data and required information are saved in the location where the code will look for it. To access the functionality of main.py, copy the lines of code to the interactive window and run them by pressing the ‘**play**’ button or by pressing **shift + enter**. Before using any part of the script, always import the required packages first. These lines of code are usually at the top of the file and start with or contain the word **import**. The package can be imported by running these lines of code in the interactive window.

For each dataset the main folder the script works from is the data that contains the raw imaging data. It is assumed that each raw dataset has its own subfolder in the same folder. These subfolders can be generated manually or by the image extraction option in the code. Each dataset subfolder is supposed to contain several subfolders, each of which contains data or information on which the counting of cells or subsets thereof is based on. Some of these folders and their contents can be generated by specific functions of the code, whereas others may need to be generated manually (e.g. image masks**).** 

**If parts of the data required for cell counting are added manually, make sure to put this data in the place where the script will be looking for it.**

![](image006.png)

**Extracting images**

The extraction of images from the raw data (called unpacking in the code) basically means that multi-channel z-stacks are separated into single-channel z-stacks, each of which will be saved as a .tif file in a newly created folder for that channel. Currently, this only works for .lif files. If the image format is .lsm, .czi, or .tif, this step needs to be done manually or new code needs to be written. In order for it to work with .czi (and possibly .lsm) or .tif, the new code can be written in the **czi\_unpacker.py** or the **tif\_unpacker.py** files, respectively.

**Automated extraction**

Using the cell counter script (**main.py**):

1. Import the required packages of main.py as described earlier.
1. Add the file path of the folder containing the raw data to the **RAW\_DATA\_FOLDER** variable in **main.py**. **Make sure to change the backslashes to forward slashes and to have the file path surrounded by these: ‘  !**
1. Run **unpack = ImageUnpacker(RAW\_DATA\_FOLDER)**
1. Run **unpack.unpack\_images()**

In order to get the channels detected using this script it is possible to run the following lines of code:

1. **dataset\_folders = unpack.get\_subfolders(unpack.folder)**
1. **channels = unpack.get\_subfolders(dataset\_folders[0])**

In case of .lif files, the unpacking module will separate the channels based on the color of the channels that it was given during imaging. Therefore, it will give the folders the names of the colors. These folder names can be changed manually, but make sure to use the new folder names in subsequent steps of the analysis. 

**Manual extraction**

Single-channel image z-stacks can also be extracted manually using other software, such as Fiji. In this case it is important manually create a dataset folder inside the **RAW\_DATA\_FOLDER**. Inside this dataset folder a new folder for each channel that will be used for the counting of cells needs to be created. The single-channel z-stacks should then be saved as .tif files (1 .tif per stack) in the appropriate folders.  The names of the folders don’t matter, as long as those names are provided to the script in the appropriate parameters. 

**Preprocessing of images**

In some cases it will be useful to preprocess the nuclear labelling channel to get better segmentation by the Cellpose algorithm. Especially for bigger z-stacks with clear differences in signal intensity between the most superficial and the deeper z-slices, as well as a significant drop in signal quality in the deeper slices preprocessing, can help a lot. This script allows for two different preprocessing options, namely contrast limited adaptive histogram equalization (CLAHE) and a standard median filter.

*CLAHE*

CLAHE is recommended when there are large differences in signal intensity between the different slices. This is especially the case with bigger stacks. This cell counter code allows for two different options, namely to do the CLAHE on the entire z-stack (**clahe\_total**) or to do it on each z-slice of the stack separately (**clahe\_per\_slice**). So far, it seems that the **clahe\_per\_slice** option works best. 

*Median filter*

The median filter can be particularly useful when the outline of the nuclei is a little fuzzy and/or when there is a lot of background signal. This is often the case in the deeper slices of bigger z-stacks.

**Automated preprocessing:**

1. Provide the folder names of the channels that need to be preprocessed as a Python list in the variable called: **CHANNELS\_TO\_PREPROCESS.** A list is basically an enumeration of different elements. In Python the entire list is enclosed by [ ] and the individual elements are separated by commas. 
1. Provide what type of preprocessing to do as a list in the variable called: **PREPROCESSING\_STEPS**. Options: ‘**clahe\_per\_slice**’, ‘**clahe\_total**’, ‘**median**’. Only provide those in the list that are necessary. If preprocessing is not necessary, provide an empty list or skip the entire preprocessing part.
1. Provide the parameters for the different preprocessing steps in the variables called: **CLIP\_LIMIT** (CLAHE), **NBINS** (CLAHE), **FOOTPRINT** (median filter). Sometimes tweaking them, especially for CLAHE is necessary to get optimal results. There is no definite guideline on what to tweak and how. It is probably no necessary to change the footprint. The other two is a bit of trial and error to find out what looks good and what would work best with cellpose. Use datasets analyzed before as a guide on how it should look.
1. Run **data\_preprocessor = DataPreprocessor(RAW\_DATA\_FOLDER, CHANNELS\_TO\_PREPROCESS)**
1. Optional à Run **data\_preprocessor.make\_composite()**. This function makes a separate folder containing the merged channels. **NOTE: This should be done before the actual preprocessing. Otherwise there may be errors**.
1. Run **data\_preprocessor.preprocess\_images(preprocessing\_steps=PREPROCESSING\_STEPS, clipLimit=CLIP\_LIMIT, nbins=NBINS, footprint=FOOTPRINT)** to preprocess the images.


**Manual preprocessing:**

In case preprocessing has been done beforehand or in another program like FIJI, make sure to create a subfolder called “preprocessed” inside the channel folder for which the images have been preprocessed. Save the preprocessed images for that channel inside that folder. In case composite images still need to be made, first run step 4 and 5 of the automated preprocessing part and then add the folders to save the preprocessed images in. Otherwise an error may occur.

***Optional: Change z-stack for cellpose***

Sometimes the stack that has been images is larger than what is required for counting the cells. In that case this script also provides an option to trim the z-stacks. This means that a range of slices can be selected that are going to be used for the counting of cells. This function in this cell counter code first detects for each image how many z-slices there are and then saves this as a .txt document in the each dataset’s folder. These z-slice numbers can be changed manually after which the script will apply these slice numbers to each image within every folder inside the dataset folder. The advantage of this would be that the running time of the Cellpose algorithm is most likely shorter.

**How to trim z-stack:**

1. Run **data\_preprocessor.get\_slice\_info()**
1. Manually provide starting slice and end slice number in the **slice\_dictionary.txt** file in the dataset folder (file will appear after step 1)
1. Run **data\_preprocessor.trim\_images()**


**Cellpose**

In this case segmentation of the images will be done using Cellpose. If a segmentation method other than Cellpose will be or has been used, make sure to save the required output in the appropriate folders. The required output consists of a 3D segmentation label map and a segmentation label map for which all slices of the z-stack have been segmented separately (called 2D label map hereafter). Segmentation will be done on the nuclear label channel (e.g. DAPI). Running Cellpose can take quite a while, so if the computer doesn’t have a gpu, it may be better to run it on google Colab or on the university computer cluster.

**Setting up the environment to run Cellpose on the computer cluster of the university**

Apply for access to the university computer cluster in the following link:

<https://www.rug.nl/society-business/centre-for-information-technology/research/services/hpc/facilities/request-peregrine-account>

It may be required to take the course (~4h) during which there will be an explanation on how to use the cluster and the rules. Documentation on how to use the cluster can be found here:

<https://wiki.hpc.rug.nl/peregrine/introduction/start>

One of the easiest ways to access the computer cluster is to use the MobaXterm software (windows, could be different for mac or linux). MobaXterm can be downloaded here:

<https://mobaxterm.mobatek.net/download.html>

The free version should suffice.

After starting MobaXterm, click on session in the top left corner. A pop-up screen will appear in which the SSH (top left corner) needs to be clicked on. This will open a screen in which the connection to the cluster can be made. In the text box for remote host type peregrine.hpc.rug.nl. For more detailed information on how to connect to the computer cluster, go to the peregrine documentation (<https://wiki.hpc.rug.nl/peregrine/connecting_to_the_system/windows>). The peregrine.hpc.rug.nl is one of the three possible login nodes. The other two are pg-interactive.hpc.rug.nl and pg-gpu.hpc.rug.nl. In these two nodes, it is possible to test code either with cpu or gpu, respectively. How to use these login nodes is clearly explained in the documentation. In general, the peregrine.hpc.rug.nl login node should be used to run the code as described below.

After starting the session, the RUG account password needs to be entered. When typing the password it looks as if nothing is being typed. Don’t worry about this. Just type the password and press ‘enter’ to access the cluster. 

All sessions will start in the home directory (**/home/p-number/**). The storage space in this directory is quite limited and not suitable for uploading or saving a lot of data such as images. In the home directory, it is possible to save small files like scripts.

![](image007.png)

Data can be uploaded and stored in the data directory. To navigate there type **/data/p-number/** in the box indicated by home directory in the figure above. Although this directory is not without limit, it should have more than enough space for uploading the data to that directory to run the Cellpose algorithm. Uploading data can be done by navigating to the folder where it needs to go in the box indicated by home directory or to just click on the folder and then to drag the images to that folder.

Before being able to run Cellpose, a virtual Python environment needs to be created in which to install the required packages including Cellpose. The virtual environment can be stored somewhere in the home directory or data directory. To create virtual environment it is important to first activate the correct Python module. This can be done by typing **module load Python/3.7.4-GCCcore-8.3.0** in the terminal window.

Then create the new virtual environment by running the following command in the terminal window:

**python3 –m venv /data/p-number/.envs/cellpose** 

Next, activate the new python environment by running this command in the terminal window:

**source /data/p-number/.envs/cellpose/bin/activate**

Now it is possible to install the required python packages. If this is the first time installing packages in this environment it would be best to start with updating pip (Python package installer) and wheel. This can be done by running the following commands:

**pip install --upgrade pip** 

**pip install --upgrade wheel**

Then install all the required packages using **pip install package\_name**.

The packages that should be installed are **cellpose**, **scikit-image**, **numpy**, **pandas**

Close the virtual environment by running the command **deactivate**.

Close the Python module by running the command **module purge**.

**Running Cellpose scripts**

To run scripts on the computer cluster, two scripts need to be prepared. One script for running the code, which would be the Cellpose code in this case, and the other is the script to tell the computer cluster what to do (job script). The job script includes instructions on which script to run, which programming language will be used, which resources will be required and how long it will take. The job script is a .sh script. When running this job script, it will be placed in a queue on the cluster, meaning it will only be run when the required resources are available. If it is very busy on the computer cluster, it may take a while for the script to start running. 

**Step 1:**

Make a new folder somewhere in the data folder on the cluster to upload the images that need to be segmented (input folder). Create two other folders in which to save the output from the cellpose algorithm (output folders). One folder will be for the slice-by-slice segmentation (2D) and the other will be for the segmentation in 3D. It doesn’t really matter where the input and output folders are made, as long as it is in the data folder and the path to the folders is known. Then upload the (preprocessed) images to the input folder. After the script has finished running the output can be downloaded from the output folders.

**Step 2:**

Prepare the Cellpose script and save it somewhere on the computer cluster. It doesn’t really matter where  it is saved (either in the home folder or the data folder), but it is important to know the file path to the location where it has been saved. Inside the Cellpose script indicate the path to the input folder (**PATH\_DATA**) and the output folders (**PATH\_RESULTS\_2D** and **PATH\_RESULTS\_3D**). Additionally, the parameters for the Cellpose algorithm need to be set. This can be done inside the **model.eval** functions, one of which is for the 2D segmentation, while the other is for the 3D segmentation. Information on how to set the parameters and which ones to use, the Cellpose documentation can be very helpful (<https://cellpose.readthedocs.io/en/latest/settings.html>).

The settings that result in the best possible segmentation can differ from dataset to dataset, so it is important to do a few trial runs to check what works best. Also, for each dataset write down or save somewhere which parameters have been used for the analysis of that particular dataset. The ones that may require some adjustment are **diameter**, **flow\_threshold**, **mask\_threshold** and **stitch\_threshold** (only for 3D segmentation). Leave the others as is. It is also possible to set **do\_3D** to **True**. In that case, the **stitch\_threshold** is not required. However, this mode is much slower and for these types of data (nuclei in zebrafish brain) the segmentation quality seems much lower.

**Step 3:**

Prepare the job script and save it somewhere on the computer cluster. To do this, take the standard job script provided with this manual and adjust it as needed. The **--jobname** can be changed, but has no influence on whether the script will be run and completed successfully. The **--time** is the time required for running the script. The time provided here will be the time reserved on the cluster. This means that if the running of the script takes longer than the time provided it will be aborted after the reserved amount of time has passed. The longer the time reserved, the longer it may take for the script to start running, especially if it is very busy on the cluster. Therefore it is recommended to make an accurate estimate on how much time needs to be reserved and then book a little bit more time to make sure the script won’t be killed before it has finished.

In **--partition**, it needs to be specified whether to run it on **gpu** or **cpu**. In the case of Cellpose gpu is recommended. In **--mem** the required amount of RAM memory is specified. In case of gpu a whole node of 128GB will be reserved, so it would be safest to ask for the maximum amount of memory for one node. In general 128GB should be more than enough for running Cellpose on standard z-stack images. In **--gres**, which the required node(s) needs to be specified. For more information on this, look at the documentation of the cluster (<https://wiki.hpc.rug.nl/peregrine/introduction/start>). For running scripts with the cpu, there are some other things that need to be specified, all of which can be found in the documentation.

The next two lines in the code are to make sure the correct Python version is used and that there are no other versions or anything interfering with running the scripts. The following line, starting with **source** is the one where the virtual environment in which Cellpose has been installed will be activated. Put here **path\_to\_virtual\_environment\_folder/bin/activate**. The last line of code before **deactivate** starts python and runs the script. This is where the path to the Cellpose script needs to be specified. 

**Step 4:**

To run both  use the terminal window to navigate to the folder in which the job script has been saved (you will NOT see any changes in the window showing all the folders).  This can be done by running the command **cd path\_to\_jobscript\_folder** in the terminal. To check whether this has worked as intended run the command **ls** (lowercase L, NOT capital i) in the terminal. This should result in a list of the files that are inside that folder, including the job script file. If the folder contains the job script file that needs to be run, run the command **sbatch jobscript\_filename.sh**. If everything works properly, the job number, which is the ID of the job in the cluster should be given in the terminal. This job ID can then be used to track what is going on with the job. Sometimes running the **sbatch** command will result in an error, which is most likely due to the job script not being saved in a UNIX format. To make sure it is, open the job script in MobaXterm (double click on the file), go to **format** in the bar at the top of the window of the MobaXterm text editor that has been opened, select **UNIX** and then save it again.



**Step 5:**

By entering **jobinfo job\_number**, it is possible to check what is going on with the script. This includes information on whether it is running, queued or completed, how much memory has been used, for how long it has been running, how long it took to complete it etc. In case the script didn’t complete for whatever reason, it may also indicate why it has stopped running (e.g. if the reserved amount of time was too short). To get a more detailed explanation on why the script has failed to complete (e.g. mistakes in Cellpose script), go to the folder in which the job script has been saved and open the file called **slurm-job\_number**. These slurm files are automatically generated whenever a job script will be run. This file always ends up in the same folder as the job script that was run and it contains a detailed report of what happened with the script.

**Step 6:**

Create two new folders inside the dataset folder (which is in the raw data folder) on the computer. Then download the results from the Cellpose segmentation (label maps) from the cluster (output folders) and save them in the newly created folders on the computer. It is important to randomly check some segmentations to make sure everything has been segmented properly, especially in the z-direction. This can be done by using FIJI for example. In order to see the label map as a multicolored image, install the MorpholibJ plugin, open the label map, go to **plugins à MorpholibJ à Label images à Labels to RGB**. 

**NOTE: Don’t call the file containing the cellpose script cellpose.py. This may result in an error, depending on where the script has been saved.**

**Cell counting**

**Manual generation of image masks for subsetting the cells to count**

In order to count only a subset of the cells in the image (e.g. all cell in the telencephalon, only neurons) this script has several options to select the appropriate subset. This can be done by using image masks (manually drawn or generated using thresholding) or based on image intensity levels in one of the channels. The manually drawn image masks are basically binary images in which the region containing the cells that need to be counted has a value of 1, whereas the regions in which the cells don’t have to be counted have a value of zero. These binary masks can then be multiplied with the label map result from the Cellpose algorithm, which will result in only the labels within the mask region with value 1 will be preserved, while all the others disappear into the background with value 0. Drawing these image masks can be done with software like Napari.

Install Napari from the following link:

<https://github.com/napari/napari/releases> 

There should be a drop down menu called “Assets” near the top of the screen. The download file can be found in there.

![](image008.png)

After opening the image, create a new labels layer in which the mask can be drawn. The easiest way to draw the mask, especially if the mask area is quite large, is to first draw an outline in the labels layer and then to fill the area enclosed by the outline. Do this for every slice in the z-stack.

![](image009.png)

After drawing the mask, select the label layer and save the image mask in the appropriate (newly created) folder inside the dataset folder. Provide the name of that folder as a Python string to the **NAME\_FOLDER\_MASKS\_TELENCEPHALON** or **NAME\_FOLDER\_MASKS\_NEURONS** variables in **main.py**. It is also possible to make additional variables, just make sure to also use those new variables as parameters in the functions described below. 

**Image masks generated in other image analysis software**

In some cases it may be more convenient to generate label masks using image analysis software like Fiji. In this case, it is important to save the image masks in the appropriate (newly created) folder inside the dataset folder and to provide the names of those folders to the appropriate variables as described above.

**Counting a subset of cells using image masks**

To get the proper subset of cells, the generated image masks will first be multiplied by the 2D label maps generated by the Cellpose algorithm. Most likely, this will result in a new label map that contains the subset of cells/labels that need to be counted as well as parts of cells/labels that are at the border of the area to count. To remove these partial labels, all labels in the new label map will be compared to those in the original one. All labels that have fewer than 300 pixels (**THRESHOLD\_SIZE**) or less than 80% of the surface area of the same label in the original image (**THRESHOLD\_RATIO**) will be removed. This will be done in a slice-by-slice manner to assure that large changes in the extracted pixel area before and after multiplication with the mask due to part of the cell not being included in one of the slices do not cause the removal of cells that should be counted. 

Next, this filtered label map will be transformed into  a new binary image mask that only contains the cells that need to be counted. Then, the newly generated image mask will be multiplied with the 3D label map generated by the Cellpose algorithm. This will result in a new label map for which the total number of labels will be extracted. 

To count the cells, first provide the names of the folders in which to find the label maps and the image masks to be used for the getting subsets cells. These variable are: 

**NAME\_FOLDER\_2D\_LABELMAPS**, **NAME\_FODLER\_3D\_LABELMAPS**, **NAME\_FOLDER\_MASKS\_TELENCEPHALON**, **NAME\_FOLDER\_MASKS\_NEURONS**.

Then run the following line of code:

**counter = DataCellCounter(RAW\_DATA\_FOLDER, NAME\_RESULTS\_FILE,** **NAME\_FOLDER\_2D\_LABELMAPS**, **NAME\_FODLER\_3D\_LABELMAPS**, **NAME\_FOLDER\_MASKS\_TELENCEPHALON**, **NAME\_FOLDER\_MASKS\_NEURONS)**

Followed by:

**Counter.analyze\_data()**

Running these lines of code will amongst other generate folders containing image z-stacks showing which exact cells have been counted as well as an excel document containing the cell counts inside the dataset folder.

**Counting a subset of cells using pixel intensity values**

In addition to counting a subset of cells using image masks, it is also possible to subset cells based on pixel intensity values in one of the recorded channels. Using this functionality, the maximum and mean intensity values in the region corresponding to each label in the Cellpose label maps will be extracted. Then only the labels having mean and/or maximum pixel intensity values above the user-specified threshold will be kept and counted. The results will be added to the results.xlsx file in the dataset folder. Additionally, folders containing images showing exactly which cells have been included in the count will be generated. 

To use this function, first provide the correct information to the required variables in **main.py**:

**NAME\_RESULTS\_FILE** = **‘results.json’**  à should not be changed, unless the name of the .json file in the dataset folder has been changed.

**NAME\_LABELMAP\_FOLDER** à name of the folder containing the 3D label maps to be used for counting the cells. This can be a folder with the Cellpose results or a folder containing label maps of a subset of cells.

**CHANNELS\_TO\_USE** à List of folder names of folders containing the data that should be used for getting the subsets of cells to count. The counting will be done for each provided channel separately.

**MODE** à **‘mean’**, **‘max’**, or **‘mean/max’**. Determines whether thresholds will be based on the mean pixel value, max pixel value or both.

**CHANNEL\_THRESHOLDS\_MEAN** = List of thresholds to use if the mean pixel value will be used for setting the threshold. The order corresponds to the order in the **CHANNELS\_TO\_USE** list. 

**CHANNEL\_THRESHOLDS\_MAX** = List of thresholds to use if the max pixel value will be used for setting the threshold. The order corresponds to the order in the **CHANNELS\_TO\_USE** list.

**PREPROCESSED** à True if the preprocessed images should be used for this analysis. Otherwise, put False. 



When all the variable values have been provided, run the following lines of code:

**intensity\_counter = DataIntensityCounter(RAW\_DATA\_FOLDER, NAME\_RESULTS\_FILE, NAME\_LABELMAP\_FOLDER, CHANNELS\_TO\_USE, MODE, CHANNEL\_THRESHOLDS\_MEAN, CHANNELS\_THRESHOLDS\_MAX, PREPROCESSED)**

**intensity\_counter.count\_cells()**

**intensity\_counter.save\_results()**
