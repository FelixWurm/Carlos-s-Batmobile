import time
import VL53L0X

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
# I2C Address can change before tof.open()
# tof.change_address(0x32)
tof.open()
file = open("data.csv", 'a')
# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.GOOD)
loops = 1000
way = 0
mean = 0
maxi = tof.get_distance()
mind = tof.get_distance()
maxmean = 56
minmean = 56
allDist = 0
height = False
timing = tof.get_timing()
start_time = time.time()
if timing < 20000:
	timing = 20000
#print("Timing %d ms" % (timing/1000))

for count in range(1, loops+1):
	distance = tof.get_distance()
	allDist += distance
	if distance > 0:
		mean = allDist/count
		file.write(f"{time.time()-start_time},{distance}\n")
		#mean = allDist/count
		if distance > maxi:
			maxi = distance
		if distance < mind:
			mind = distance
		if mean > maxmean:
			maxmean = mean
		if mean < minmean:
			minmean = mean
		#if distance < (mean-(mean*0.1)):
		#	if(height == False):
		#		height = True
		#		way += 31.73
		#if distance > mean:
			height = False

	#time.sleep(timing/1000000.00)

tof.stop_ranging()
mean = allDist/loops
tof.close()
