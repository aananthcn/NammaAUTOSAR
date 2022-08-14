# Definitions
CWD := D:/_E/projects/oss/NammaAUTOSAR
ROOT_PATH := D:/_E/projects/oss/NammaAUTOSAR
MCU_BOARD_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/start-up/board
MCU_MICRO_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/start-up/board/rp2040
MCU_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu
OS_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/SL/Os
OS_BUILDER_PATH := D:/_E/projects/oss/NammaAUTOSAR/tools/os_builder

# Inclusions
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/start-up/board/rp2040/rp2040.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/start-up/arch/arm/cortex-m0/cortex-m0.mk

include D:/_E/projects/oss/NammaAUTOSAR/tools/os_builder/src/os-objs.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/SL/Os/os-common.mk

