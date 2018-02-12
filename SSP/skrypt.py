import sys
import json
import re
from pprint import pprint
import request_provider

def main():
    srcAddres = sys.argv[1]
    dstAddres = sys.argv[2]
    #srcUdpPort = sys.argv[3]
	
    server = 'http://127.0.0.1:6666'
    postUrl = '/wm/staticflowpusher/json'

    deviceSrc = '/wm/device/?ipv4={}'.format(srcAddres)
    deviceDst = '/wm/device/?ipv4={}'.format(dstAddres)

    pusher = request_provider.StaticFlowPusher(server)
    switchesData = pusher.get(getSwitchesData)
    deviceSrcData = pusher.get(deviceSrc)
    deviceDstData = pusher.get(deviceDst)

    flows = createFlows(switchesData, deviceSrcData, deviceDstData)
    for flow in flows:
        pusher.set(postUrl, flow)

class Switch():
    def __init__(self, switchData):
        self.id = switchData[0]
        self.sortedPorts = getSortedPorts(switchData)
	
	self.best = self.sortedPorts[0]['portNumber']	
	if self.best == u'1':
		self.best = self.sortedPorts[1]['portNumber']

    def __str__(self):
        return "{}".format(self.id) + "\n" + \
               "{}".format(self.sortedPorts) + "\n" + \
               "{}".format(self.best)
			   
def getSortedPorts(switchData):
    list = []
    ports = switchData[1]['port_reply'][0]['port']
    for port in ports:
	pprint(port)
        if port['portNumber'] != 'local':
            item = {}
            for key, value in port.items():
                if key in ['transmitBytes', 'portNumber']:
                    item[key] = value
		    pprint(key)
		    pprint(value)
            list.append(item)
    return sorted(list, key=lambda x: int(x['transmitBytes']))
	
def parse(deviceData):
    pprint("---------------------------")
    pprint(deviceData)
    for device in deviceData:
	pprint("---------------------------")
	pprint(device)
        switchID = device['attachmentPoint'][0]['switchDPID']
        port = device['attachmentPoint'][0]['port']
        return switchID, port
		
def create_flow(switch, src, dst):
    flow = {}	
    flow['switch'] = switch.id
    flow['name'] = "flow_" + switch.id[-1] + "_from_" + str(src) + "_to_" + str(dst)
    flow['priority'] = "666"
    flow['in_port'] = str(src)
    flow['actions'] = "output=" + str(dst)
    flow['active'] = "true"
    return json.dumps(flow)
		
def createFlows(switchesData, deviceSrcData, deviceDstData):
    flows = []
    for switchData in switchesData.items():
        switch = Switch(switchData)

        dstSwitchID, dstPort = parse(deviceDstData)
        srcSwitchID, srcPort = parse(deviceSrcData)
		
	pprint("")
	pprint("src:")
	pprint(srcSwitchID)
	pprint("dst:")
	pprint(dstSwitchID)
	pprint("switch.id")
	pprint(switch.id)
	
	if switch.id == srcSwitchID:
	    pprint("jestem src")
	    flows.append(create_flow(switch, 1,switch.best))

	elif switch.id == dstSwitchID:
	    pprint("jestem dst")
	    flows.append(create_flow(switch, 3,1))
	    flows.append(create_flow(switch, 2,1))

	else:
	    pprint("jestem inter")
	    flows.append(create_flow(switch, 2,1))	
	    flows.append(create_flow(switch, 1,2))
	pprint("")
    pprint(flows)
    return flows
	
if __name__ == "__main__":
    main()
