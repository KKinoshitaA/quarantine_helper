#ifndef __ble_master_h__
#define __ble_master_h__

#include <ArduinoBLE.h>

#define GATEWAY_SERVICE_UUID        "354d8340-289e-11ec-a32b-531c9f618227"
#define SETTING_CHARACTERISTIC_UUID "354d8343-289e-11ec-a32b-531c9f618227"

void setup_ble_master();
void loop_ble_master();

#endif
