



from L3Vpn.AutoShell3 import ChannelClass


obj1 = ChannelClass(user_name='cisco',password='cisco',enable_pass='cisco')
print(obj1.get_remote_sell_out())

obj1.set_remote_sell_out(8)

print(obj1.get_remote_sell_out())
