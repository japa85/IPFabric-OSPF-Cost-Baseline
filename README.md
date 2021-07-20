# IPFabric Configuration Comparison

Compares live OSPF Interface costs against a set of values in the "input.csv" file. 

The interface name must be the same as it appears in IPFabric. E.g. Eth Po etc...

The script strips off any domain names / firewall contexts etc... from the device name in IPFabric.

Email is sent with a list of interfaces where the actual cost is not compliant with the expected cost. 
