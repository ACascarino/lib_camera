/*
TODO add compatibility with XC

*/
#include <xs1.h>
#include <stdio.h>
#include <stdlib.h>
#include <platform.h>
#include <xcore/channel.h>
#include <xcore/port.h>
#include <xcore/parallel.h>
#include <xcore/hwtimer.h>
#include <xcore/select.h>
#include <xscope.h>
#include <platform.h>
#include <xcore/triggerable.h>

#include "i2c.h"
#include "main.hpp"

// #include "mipi.h"
// #include "mipi_main.h"

// I2C interface ports
port_t p_scl = XS1_PORT_1N;
port_t p_sda = XS1_PORT_1O;

i2c_master_t i2c_ctx;
i2c_master_t *i2c_ctx_ptr = &i2c_ctx;

void enable_mipi_ports()
{
    port_enable(p_scl);
    port_enable(p_sda);
}

DECLARE_JOB(i2c_job, (void));
void i2c_job(void)
{
    i2c_master_init(
        i2c_ctx_ptr,
        p_scl, p_scl_bit_pos, 0,
        p_sda, p_sda_bit_pos, 0,
        I2C_SPEED);
}

int main(void)
{
    enable_mipi_ports();
    PAR_JOBS(
        PJOB(i2c_job, ()));
    return 0;
}

// https://github.com/xmos/fwk_io/blob/develop/test/lib_i2c/i2c_master_test/src/main.c