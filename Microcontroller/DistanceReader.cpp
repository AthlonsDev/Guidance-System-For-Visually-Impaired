#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <distance_sensor.h>

int main() {
    DistanceSensor hcsr04(pio0, 22, 21); // trigger pin 21, echo pin 22, pio0 refers to PIO 0, state machine 0

    #define MAX_DISTANCE 200
    #define MIN_DISTANCE 20

    // trigger background distance sensing
    hcsr04.TriggerRead();

    while(hcsr04.is_sensing) {
        //wait for distance sensing to complete
        _sleep_us(100); // sleep for 100 microseconds
    }

    // get distance reading in centimeters
    uint32_t distance = hcsr04.distance;

    // print distance reading
    printf("Distance: %d cm\n", distance);

    return 0;
}


