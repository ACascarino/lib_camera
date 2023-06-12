#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef __XC__
extern "C" {
#endif

#include "xscope_io_device.h"

void write_file(char * filename, uint8_t * data, const size_t size);
void write_image_file(
    char * filename, 
    uint8_t * image, 
    const size_t size, 
    const size_t height, 
    const size_t width);

#ifdef __XC__
}
#endif
