# NammaAUTOSAR
This project repo is created to learn and also establish a free and open source AUTOSAR stack that enables the new engineers to learn it practically. This should create more quality engineers for the Industry that paid me Salary for the last 23 years.

<br>

What is NammaAUTOSAR?
---

NammaAUTOSAR is a intended to provide a free to use with no liability licensed (MIT) software, writen against AUTOSAR specification R2020-11. This is created to learn AUTOSAR standards practically. And therefore setting a path towards learning as well as teaching AUTOSAR core skills.

What is Namma? **Namma means "our" in Tamil and Kannada**. We used to say "Avan namma friendu" in Tamil. Which means "he is our friend". So, this is (y)our AUTOSAR stack, free to use, modify, learn but with no liability.

**Start date: 27 June 2021, Sunday**<br>
Motivation to create an OS came from Ashokkumar Narayanan (one of my best buddies in Visteon Chennai).


<br><br>

Getting Started
===

Prerequisites - SOFTWARE:
----
* Ubuntu 20.04 OS (either on Linux or on WSL2 inside Windows)
  * Install following packages inside Ubuntu
    * `apt install gcc-arm-none-eabi qemu-system-arm gdb-multiarch python3`
* Windows 10 + MSYS2
  * Follow the instructions given in "Installation" section in https://www.msys2.org/
  * Install following packages by starting the **MSYS2 MSYS** terminal:
    * `pacman -Suy` 
    * `pacman -S mingw-w64-x86_64-python mingw-w64-x86_64-tk mingw-w64-x86_64-python-pip`
    * `pip install colorama`
    * `pacman -S mingw-w64-x86_64-arm-none-eabi-gcc mingw-w64-x86_64-qemu`
   * Install the following package for Gtk and Glade
   *  `pacman -S mingw-w64-x86_64-python-gobject mingw-w64-x86_64-gtk3`
  * Create envirnomental variable with **VARIABLE NAME** as **MINGW_ROOT** and **VARIABLE VALUE** as **installation path** (e.g., C:\msys64\mingw64)

<br>

Development Setup - HARDWARE:
----
![Pi Pico Development Setup](docs/namma-autosar-dev-setup.png?raw=true "Title")

* Raspberry Pi Pico with pins soldered => [check this link](https://robocraze.com/products/raspberry-pi-pico-with-headers-and-micro-usb-cable)
* Cytron Maker Pi Pico Base => [check this link](https://robu.in/product/cytron-maker-pi-pico-base-without-pico/)
* DTech FTDI USB to TTL Serial Converter => [Amazon: PL2303TA chip](https://amzn.eu/d/eYsRoTC)
  * Note for Win11: Install driver from this link [prolific-driverinstaller-v1200](https://www.driverscloud.com/en/services/GetInformationDriver/72590-84992/delock-pl2303-prolific-driverinstaller-v1200zip)
* Any debugger with SWD pin interface support => [check this link](https://in.rsdelivers.com/product/segger/80800-j-link-base/segger-j-link-base-emulator/1311319)
  * Also planning to support ELF to UF2 image conversion so that developers can flash the image and use print statements to see the debug output.
  * For SWD, buy 20 pin JTAG cable and cut & crimp it for SWD => [check this link](https://robu.in/product/2-54mm-pitch-20-pin-jtag-isp-avr-cable/)
* 2 x Grove 4-pin => [check this link](https://www.fabtolab.com/grove-universal-cable?search=grove%204%20pin)
* ENC28J60 Ethernet LAN controller => [check this link](https://robocraze.com/products/enc28j60-ethernet-lan-module)

<br>

Cloning the Repo - Fresh Start
===
As NammaAUTOSAR uses git submodules, please use the following command to clone the main and submodules. 
* `git clone --recurse-submodules --branch v2.0.0 -j4 https://github.com/aananthcn/NammaAUTOSAR.git`
* To get latest:  `git clone --recurse-submodules -j4 https://github.com/aananthcn/NammaAUTOSAR.git`

<span style="color:red"> **Note**: Only v2.0.0 version or lesser will work on NammaAUTOSAR. Beyond the version v2.0.0, all submodules will be compatible to Car-OS.Zephyr. So the build will break! </span>

<br><br>

Getting / Pulling the latest changes
===
* Do the following to get the latest changes from the main and submodules
  * `git pull`
  * `git submodule update --recursive --remote`
* After this, do not forget to pull the applications (apps are loosely coupled) manually as below
  * `cd submodules/AL/NammaTestApp`
  * `git pull`

If all steps above are successfull you are now ready to continue your contribution.

<br>



Starting the NammaAUTOSAR GUI
===
* To start the NammaAUTOSAR Builder GUI, first open the **MSYS2 MINGW64** terminal
* Navigate to the cloned repository
* Run this command in the **MSYS2 MINGW64** terminal: `python tools/autosar-gui.py`
* **NammaAUTOSAR Builder** GUI will open


<br>

Importing ARXML
---
* To import ARXML, go to File --> Import ARXML File. It will give 3 different ARXML like below

![image](https://user-images.githubusercontent.com/61110156/201695803-adf3e135-035e-4a83-ad0b-58f7b60012d9.png)

* **NOTE:** It is advised to go with RaspberryPi-Pico.arxml for now, as it is tested and working well
* Select RaspberryPi-Pico.arxml and click on Open. AUTOSAR Layered Architecture view will open
* **NOTE:** Since this project in initial phase, only few modules are presented in the layered view


<br>

Configuration
----
* Click on the any AUTOSAR module (i.e., colored rectangle boxes; e.g., Spi), another window will open for configuration of various parameters
* Once all the configuration is done, the click on **Save Config** to update the changes and close the module specific window
* Repeat the steps for all the necessary modules

<br><br>

Importing NammaTestApp
===
* Click on **Applications** (1) and wait for the clone operation to complete.
* Mention how many number of applications you want to import. In this case, I have given as 1
* Provide the **NammaTestApp** repository path in the App 0 - `https://github.com/aananthcn/NammaTestApp.git`

![image](https://user-images.githubusercontent.com/61110156/201701405-ca438c64-213a-4328-83c3-a1bc4ccc4ead.png)

* This will automatically import the NammaTestApp into respective folder

<br><br>

Code Generation
===
* Once all the configuration is done, click on the **Generate --> Generate Source**
* If all the changes are proper, then a popup with this message will be shown **Code Generated Successfully!**

![image](https://user-images.githubusercontent.com/61110156/201702795-53388e7c-2f6d-419f-aefd-8f6f7f6b61b2.png)

* Close the NammaAUTOSAR Builder GUI

<br>

Generate the ELF File
===
* In the MSYS2 MINGW64 terminal, type **make**
* This process will take sometime as it needs to compile all the source files and link them to generate the ELF file

<br>

Test it on Real Hardware
===
* If you have real hardware *Raspberry Pi Pico*, then flash the generated *\*.elf* file and test it

