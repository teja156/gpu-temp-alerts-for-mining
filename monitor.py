import clr
from discord_integration import sendMessage
import time

clr.AddReference(r'D:\\TempMonitorPython\\OpenHardwareMonitor\\OpenHardwareMonitorLib.dll')
# clr.AddReference("OpenHardwareMonitor")

from OpenHardwareMonitor.Hardware import Computer

CPU = 'amd'
# CPU = 'intel'

GPU = 'nvidia'
# GPU = 'amd'

INTERVAL = 1 #In minutes


def getGPUTemp():
	
	c = Computer()
	c.CPUEnabled = True # get the Info about CPU
	c.GPUEnabled = True # get the Info about GPU
	c.Open()


	# Get number of GPUs
	# Starts from Hardware[1]
	gpu_count = 0

	k=1
	while 1:
		try:
			curr_Hardware = c.Hardware[k]
			if str(curr_Hardware)=="OpenHardwareMonitor.Hardware.Nvidia.NvidiaGPU":
				gpu_count+=1

		except Exception as e:
			break
		k+=1

	print("GPU count: ",gpu_count)

	info = []


	for i in range(1,gpu_count+1):
		gpu_name = c.Hardware[i].Name
		gpu_temp = ""

		for a in range(0, len(c.Hardware[i].Sensors)):
			# print(c.Hardware[1].Sensors[a].Identifier)
			idstring_cpu = ""
			idstring_gpu = ""
			if CPU=='amd':
				idstring_cpu = "/amdcpu/0/temperature"
			else:
				idstring_cpu = "/intelcpu/0/temperature"


			if GPU=='amd':
				idstring_gpu = "/amdgpu/%d/temperature"
			else:
				idstring_gpu = "/nvidiagpu/%d/temperature"

			# if idstring in str(c.Hardware[0].Sensors[a].Identifier):
			#     print(c.Hardware[0].Sensors[a].get_Value())
			#     c.Hardware[0].Update()


			if idstring_gpu%(i-1) in str(c.Hardware[i].Sensors[a].Identifier):
				gpu_temp = str(c.Hardware[i].Sensors[a].get_Value())
				break

		gpu_info = {"Name":gpu_name,"Temp":gpu_temp}
		info.append(gpu_info)

	return info
    

def check(info):
	status = []
	for i in info:
		curr_name = i["Name"]
		curr_temp = i["Temp"]

		if float(curr_temp) < 60:
			curr_status = {"Name":curr_name, "Temp":curr_temp, "Status": "Great"}
		if float(curr_temp) >= 60 and float(curr_temp) < 68:
			curr_status = {"Name":curr_name, "Temp":curr_temp, "Status": "Normal"}
		if float(curr_temp) >= 68 and float(curr_temp) < 80:
			curr_status = {"Name":curr_name, "Temp":curr_temp, "Status": "Attention"}
		if float(curr_temp) >= 80:
			curr_status = {"Name":curr_name, "Temp":curr_temp, "Status": "Critical"}

		status.append(curr_status)
	return status


if __name__ == "__main__":
	while 1:
		info = getGPUTemp()
		print("\n==============================================")
		for i in info:
			print(f"GPU Name: {i['Name']}\nGPU Temp: {i['Temp']}")

		status = check(info)

		sent = sendMessage(1, content=status)

		time.sleep(INTERVAL*60)

	# sent = sendMessage(lastSent=1,content=[{"Name":"test gtx 1111", "Temp":"78", "Status":"Attention"},{"Name":"test gtx 2222", "Temp":"78", "Status":"Attention"}])