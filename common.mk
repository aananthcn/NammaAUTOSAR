#/*
# * Created on Mon Aug 22 2022 9:35:20 PM
# *
# * The MIT License (MIT)
# * Copyright (c) 2022 Aananth C N
# *
# * Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# * and associated documentation files (the "Software"), to deal in the Software without restriction,
# * including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# * and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# * subject to the following conditions:
# *
# * The above copyright notice and this permission notice shall be included in all copies or substantial
# * portions of the Software.
# *
# * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# * TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# */

$(info compiling AUTOSAR Os Common source files)
ifeq ($(OS),Windows_NT)
	MINGW_BUILD = TRUE
else
	MINGW_BUILD = FALSE
endif	 

OBJS	:= $(CMN_OBJS) $(BRD_OBJS) $(ARCH_OBJS) $(LIBOBJS) $(SG_OBJS) \
	   $(MCU_OBJS) $(ECUM_OBJS)  $(PORT_OBJS) $(APP_OBJS)

.PHONY: all
.DEFAULT_GOAL := all

build_check:
	@if [ ${MINGW_BUILD} = TRUE ]; then\
		if [ -z "${MINGW_ROOT}" ]; then\
			printf "\nError: MINGW_ROOT is not defined! Please define it as a environmental variable!";\
			printf "\n[Hint: MINGW_ROOT should point to MSYS2 installation path (D:\msys64\mingw64)]\n";\
			exit 1;\
		fi;\
	fi

${TARGET}: ${OBJS}
	@echo LINKING OBJECTS...
	$(LD) $^ -o ${TARGET}.elf $(LDFLAGS) -Map=${TARGET}.map
	$(OBJCOPY) -O binary ${TARGET}.elf ${TARGET}.bin


all: build_check ${TARGET}


info:
	@echo make can be run with var ARCH=${ARCH}
	@echo By default ARCH=arm64


clean:
	rm -f ${OBJS}
	rm -f ${TARGET}.bin ${TARGET}.elf ${TARGET}.map