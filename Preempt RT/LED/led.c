/*
COPYRIGHT (C) 2009  Roberto Bucher (roberto.bucher@supsi.ch)

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
*/

#include <pyblock.h>
#include <linux/spi/spidev.h>
#include <stdlib.h>
#include <stdint.h>
#include <spiconfADC.h>
#include <commonFun.h>
#include <stdio.h>
#include <stdarg.h>
#include <unistd.h>

#include <pigpio.h>
int main(int argc, char *argv[])
{
   int i, rest, g, wave_id, mode, diff, tally;
   gpioPulse_t pulse[2];

   gpioInitialise();
   //gpioPWM(17, 255); // Sets GPIO17 full on.
   gpioPWM(17, 0); // Sets GPIO17 full on.
}
