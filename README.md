# FreeAUTOSAR
A project repo to create and learn AUTOSAR stack



What is NammaAUTOSAR?
---

NammaAUTOSAR is a intended to provide a free to use with no liability licensed (MIT) software, writen against AUTOSAR specification R2020-11. This is created to learn AUTOSAR standards practically. And therefore setting a path towards learning as well as teaching AUTOSAR core skills.

What is Namma? Namma means our in Tamil and Kannada. We used to say "Avan namma friendu" in Tamil. Which means "he is our friend". So, this is (y)our OSEK, free to use with no liability.

**Start date: 27 June 2021, Sunday**<br>
Motivation to create an OS came from Ashokkumar Narayanan (one of my best buddies in Visteon Chennai).


<br>

Getting Started
===

Prerequisites
----
* Ubuntu 20.04 OS (either on Linux or on WSL2 inside Windows)
  * Install following packages inside Ubuntu
    * `apt install gcc-arm-none-eabi qemu-system-arm gdb-multiarch python3`
* Windows 10 + MSYS2
  * Follow the instructions given in "Installation" section in https://www.msys2.org/
  * Install following packages:
    * `pacman -S mingw-w64-x86_64-python mingw-w64-x86_64-tk mingw-w64-x86_64-python-pip`
    * `pip install colorama`
    * `pacman -S mingw-w64-x86_64-arm-none-eabi-gcc mingw-w64-x86_64-qemu`
<br>

