from ncclient import manager
import xmltodict
from tabulate import tabulate



def get_request(xmlstring): 
    print("XML FILTER:") 
    print(xmlstring) 
    with manager.connect(host='10.10.20.177', port=830, 
        username='cisco', password='cisco', 
        hostkey_verify=False) as device:

        netconf_reply = device.get(('subtree', xmlstring))

    print("NETCONF RESPONSE:" )
    print("")
    node_object = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    node_interfaces = node_object["interfaces"]["interface"]
    
    headers = ["Interface", "Description", "Enabled", "IP", "Broadcast(IN)", "Unicast(IN)", "Multicast(IN)", "Broadcast(OUT)", "Unicast(OUT)", "Multicast(OUT)"]

    table = [] 

    print(" Node MAC Address: " + node_interfaces[0]["ethernet"]["state"].get("mac-address"))
    for idx, interface in enumerate(node_interfaces):
         inside_table = []
         table.append(inside_table)
         table[idx].append(interface["name"])
         table[idx].append(interface["config"]["description"])
         table[idx].append(interface["config"]["enabled"])
         table[idx].append(interface["subinterfaces"]["subinterface"]["ipv4"]["addresses"]["address"]["config"].get("ip"))
         table[idx].append(interface["state"]["counters"].get("in-broadcast-pkts"))
         table[idx].append(interface["state"]["counters"].get("in-unicast-pkts"))
         table[idx].append(interface["state"]["counters"].get("in-multicast-pkts"))
         table[idx].append(interface["state"]["counters"].get("out-broadcast-pkts"))
         table[idx].append(interface["state"]["counters"].get("out-unicast-pkts"))
         table[idx].append(interface["state"]["counters"].get("out-multicast-pkts"))


    print(tabulate(table, headers, tablefmt="fancy_grid"))

xml_filter = """
     <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                    <name>eth1/1</name>
                </interface>
                <interface>
                    <name>eth1/2</name>
                </interface>
                <interface>
                    <name>eth1/3</name>
                </interface>
                <interface>
                    <name>eth1/4</name>
                </interface>
                <interface>
                    <name>eth1/5</name>
                </interface>
                <interface>
                    <name>eth1/6</name>
                </interface>
                <interface>
                    <name>eth1/7</name>
                </interface>
                <interface>
                    <name>eth1/8</name>
               </interface>
            </interfaces>
     """

get_request(xml_filter) 