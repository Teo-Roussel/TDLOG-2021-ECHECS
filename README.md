# TDLOG-2021-ECHECS
TDLOG Repository - Project by Antonin Boisneault, Hamza Zerhouni, Robin Boezennec and Teo Roussel

This repository contains everything you need in order to play our application. 
If you are under Windows 64 bits, please download our Application Installer which you can download by clicking on the link inside the folder named Application.
Sadly we did not produce an application that works under MAC-OS or Linux. 

Therefore, you're free to download all our codes in order to use it through python 3.7 and over. For that please download the folder Projects_Code.zip

**Under Win64**

Once it is done and you've extracted the files in your favorite repository, please open a terminal that is linked to your python environment. Then go into the moduleAI folder then turn-on your internet connexion and write :
```
python setup.py install
```
ATTENTION : Under Win64, you need to have Visual Studio (at least 2015) installed with both Python et C++ extensions to do so/.
Please wait until it is finished then you can go into your favorite python IDE and try to execute the file named test.py located inside the test folder :
If that works please continue; otherwise contact antonin.boisneault@eleves.enpc.fr

**Under MAC-Linux**

Since one of the modules we use does not work properly except under Win64, you will have to create a virtual environment to make sure the codes will be executed. All you need is then contained inside the requirements.txt located at the base of the Project_Codes folder.

The commands to create the virtual environnement are the following :
```
python -m pip install virtualenv #if you do not have the module
python -m virtualenv NAMEENVIRONMENT 
```
If you think it is not clear enough, please refer to the PDF file named Virtualenv_Explanations

Then to activate your virtual environment please go inside the folder named "NAMEENVIRONMENT" then "bin" then execute :
```
. activate
python -m pip install -r requirements.txt
```
Then please install moduleAI by following the instructions detailled in "Under Win64".

**Playing the game**

Once it works, you can freely use our programm with lauching our Initial_Window.py file as script (Please be careful. It is necessary to run it as script. In Pyzo, please do Run file as script or Ctrl+Shift+E. If you're a PyCharm User, you probably already know how to do it. If you use a command prompt there should not be any problem). 
ATTENTION : under Linux, please do not use your IDE, please use the prompt command linked to the virtual environnement.

To fully enjoy our game, please enter the mode you want to play then your name(s) and color if AI mode. Then please if it's your first time click on the Game menu (located in the menu bar of the playing window that has appeared) then on Rules and functionalities. It is a must to enjoy our game to the fullest with all its functionnalities

Good luck and have fun !

Respectfully, 

The Team

**Agknowledgements**

We truly thank Perceval Wolff, our favorite beta tester that drove our AI into a corner which allowed to bring to light many bugs that we had not discovered, and Robin Bidanchon that helped us resolve all problems related to Linux. Last, we thank Xavier Clerc and Louis Trezzini that helped us throughout the entire project.   

