# TDLOG-2021-ECHECS
TDLOG Repository - Project by Antonin Boisneault, Hamza Zerhouni, Robin Boezennec and Teo Roussel

This repository contains everything you need in order to play our application. 
If you are under Windows 64 bits, please download our Application Installer which you can download by clicking on the link inside the folder named Application.
Sadly we did not produce an application that works under MAC-OS or Linux. 

Therefore, you're free to download all our codes in order to use it through python 3.7 and over. For that please download the folder Projects_Code.zip

**Under Win64**

Once it is done and you've extracted the files in your favorite repository, please open a terminal that is linked to your python environment. Then go into the Install-Module-Pybind folder then turn-on your internet connexion and write :
```
python setup.py install
```
ATTENTION : Under Win64, you need to have Visual Studio (at least 2015) installed with both Python et C++ extensions to do so/.
Please wait until it is finished then you can go into your favorite python IDE and try to execute the file named test.py located inside the test folder :
If that works please continue; otherwise contact antonin.boisneault@eleves.enpc.fr

**Under Linux**

Since one of the modules we use does not work properly except under Win64, you will have to create a virtual environment to make sure the codes will be executed. We have created that environment for you. It is at your disposition inside the folder named venvChess. Go inside that folder then inside the Script folder, trigger a command prompt linked to python then tap :
```
activate
```
Then navigate and returns to the aforementionned moduleAI folder and execute the commands listed in the previous section.

If you do not want to use our virtual environnement, it probably means that you're familiar with virtual environnements. All you need is then contained inside the requirements.txt located at the base of the Project_Codes folder. Then please install moduleAI by following the previous instructions.

In case you do not remember, the commands to create the virtual environnement are the following :
```
python -m pip install virtualenv #if you do not have the module
python -m virtualenv NAMEENVIRONMENT 
python -m pip install -r requirements.txt
```


**Playing the game**

Once it works, you can freely use our programm with lauching our Initial_Window.py file as script (Please be careful. It is necessary to run it as script. In Pyzo, please do Run file as script or Ctrl+Shift+E. If you're a PyCharm User, you probably already know how to do it. If you use a command prompt there should not be any problem). 
ATTENTION : under Linux, please do not use your IDE, please use the prompt command linked to the virtual environnement.

To fully enjoy our game, please enter the mode you want to play then your name(s) and color if AI mode. Then please if it's your first time click on the Game menu (located in the menu bar of the playing window that has appeared) then on Rules and functionalities. It is a must to enjoy our game to the fullest with all its functionnalities

Good luck and have fun !

Respectfully, 

The Team
