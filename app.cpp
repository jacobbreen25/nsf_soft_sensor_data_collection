#include <iostream>


#include "simpleble/SimpleBLE.h"


int main(int argc, char* argv[]) {
    SimpleBLE::Adapter adpt;
    adpt.bluetooth_enabled();
/*  if (!SimpleBLE::Adapter::bluetooth_enabled()) {
      std::cout << "Bluetooth is not enabled" << std::endl;
      return 1;
   }
    std::cout << "Bluetooth Enabled" << std::endl;
    auto adapters = SimpleBLE::Adapter::get_adapters();

   // Use the first adapter
   auto adapter = adapters[1];

   adapter.set_callback_on_scan_found([](SimpleBLE::Peripheral peripheral) {
        std::cout << "Found device: " << peripheral.identifier() << " [" << peripheral.address() << "] "
                  << peripheral.rssi() << " dBm" << std::endl;
    });

    adapter.set_callback_on_scan_updated([](SimpleBLE::Peripheral peripheral) {
        std::cout << "Updated device: " << peripheral.identifier() << " [" << peripheral.address() << "] "
                  << peripheral.rssi() << " dBm" << std::endl;
    });

    adapter.set_callback_on_scan_start([]() { std::cout << "Scan started." << std::endl; });

    adapter.set_callback_on_scan_stop([]() { std::cout << "Scan stopped." << std::endl; });


   // Do something with the adapter
   for (auto& adapter : adapters) {
        std::cout << "Adapter: " << adapter.identifier() << " [" << adapter.address() << "]" << std::endl;
    }

    adapter.scan_for(5000);
*/
    //std::vector<SimpleBLE::Peripheral> peripherals = adapter.scan_get_results();

    return 0;
}
    /*std::ofstream file;
    file.open("test.csv");
    std::cout << "Test" << std::endl;
    file << "1,2,3,4,5,6" << std::endl;
    file.close();
    return 0;*/


