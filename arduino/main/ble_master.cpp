#include "ble_master.h"

BLEDevice peripheral;
BLECharacteristic cmdCharacteristic;

static bool scan_peripheral() {  
  bool ret = false;
  
  BLE.scanForUuid("354d8340-289e-11ec-a32b-531c9f618227");
  
  // check if a peripheral has been discovered
  peripheral = BLE.available();

  if (!peripheral) {
    goto __fin;
  }

  if (peripheral.hasLocalName() != true) {
    goto __fin;
  }

  if (peripheral.localName() != "Gateway") {
    goto __fin;
  }

  Serial.print("Local Name: ");
  Serial.println(peripheral.localName());

  // print the advertised service UUIDs, if present
  if (peripheral.hasAdvertisedServiceUuid()) {
    Serial.print("Service UUIDs: ");
    for (int i = 0; i < peripheral.advertisedServiceUuidCount(); i++) {
      Serial.print(peripheral.advertisedServiceUuid(i));
      Serial.print(" ");
    }
    Serial.println();
  }

  // print the RSSI
  Serial.print("RSSI: ");
  Serial.println(peripheral.rssi());

  ret = true;

__fin:
  BLE.stopScan();
  return ret;
}

static bool connect_peripheral()
{
  if (peripheral.connect()) {
    Serial.println("Connected");
  } else {
    Serial.println("Failed to connect!");
    goto __error; 
  }

  // discover peripheral attributes
  Serial.println("Discovering attributes ...");
  if (peripheral.discoverAttributes()) {
    Serial.println("Attributes discovered");
  } else {
    Serial.println("Attribute discovery failed!");
    goto __error;
  }

  // retrieve the command characteristic
  cmdCharacteristic = peripheral.characteristic("354d8343-289e-11ec-a32b-531c9f618227");

  if (!cmdCharacteristic) {
    Serial.println("Peripheral does not have command characteristic!");
    goto __error;
  } else if (!cmdCharacteristic.canWrite()) {
    Serial.println("Peripheral does not have a writable command characteristic!");
    goto __error;
  } else {
    Serial.println("Peripheral is ready");
  }

  return true;

__error:
  peripheral.disconnect();
  return false;
}

static bool write_peripheral() {
  if (peripheral.connect()) {
    Serial.println("write_peripheral");
    cmdCharacteristic.writeValue((byte)0x01);
  } else {
    Serial.println("Failed to connect!");
    peripheral.disconnect();
    return false;
  }

  return true;
}

void setup_ble_master() {
  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }
  Serial.println("BLE Central scan");

  // wait for peripheral connection
  while(true) {
    if (scan_peripheral() != true) {
      continue;
    }
    if (connect_peripheral() != true){
      continue;
    }
    break;
  }
}

void loop_ble_master() {
  write_peripheral();
}
