from seispy.velocity import VelocityModel

vm = VelocityModel("/home/shake/malcolcw/products/velocity/FANG2016/interpolated/VpVs.dat",
                   topo="/home/shake/malcolcw/data/mapping/ANZA/anza.xyz")

#retrieve some velocity values at arbitrary locations inside the volume
print vm.get_Vp(34.12, -116.325, 5.76)
print vm.get_Vs(34.12, -116.325, 5.76)
print vm.get_Vp(33.87, -115.59, -10.0)

#make a very coarse plot, 25 samples along either axis
vm.plot_Vp(lon=-116.2, nx=25, ny=25)
#make a finer plot, 200 samples along either axis
vm.plot_Vp(lon=-116.2, nx=200, ny=200)
