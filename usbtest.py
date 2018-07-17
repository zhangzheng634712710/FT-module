import usb.core
from PIL import Image
from PIL import ImageDraw


origin_image = Image.new("L", (192, 192), "white")
origin_image_draw = ImageDraw.Draw(origin_image)
# origin_histo = Image.new("L", (256, 256), "white")
nomalize_image = Image.new("L", (192, 192), "white")
nomalize_image_draw = ImageDraw.Draw(nomalize_image)
# nomalize_histo = Image.new("L", (256, 256), "white")
smooth_filter_image = Image.new("L", (192, 192), "white")
smooth_filter_image_draw = ImageDraw.Draw(smooth_filter_image)
# smooth_filter_histo = Image.new("L", (256, 256), "white")

# origin_image.show()
# nomalize_image.show()
# smooth_filter_image.show()

dev = usb.core.find(idVendor=0x28e9, idProduct=0x028a)
if dev is None:
    print("no usb connected!")
else:
    print("USB connected!")
#   print(dev)
    if dev.is_kernel_driver_active(0) is True:
        print("USB detach kernel driver")
        dev.detach_kernel_driver(0)
#    try:
#        dev.set_configuration()
#    except BaseException, e:
#        print(e)
#    else:
    senddata = [0x55, 0xaa]
    while(True):
        str = raw_input("Please Enter command : ")
#        print(str)
        if str == 'exit':
            break
#        print("send data start...")
        try:
            msg = dev.write(0x1, senddata, 1000)
#            print(msg)
        except BaseException, e:
            print(e)
            break
        print "data transmit start..."
        try:
            recivedata = dev.read(0x81, 192*192, 5000)
            print "data transmit over, %d data received" % len(recivedata)
            if len(recivedata) == 192*192:
                print("image data transmit over")
                if str == 'orig':
                    for column in range(0, 192):
                        for row in range(0, 192):
                            origin_image_draw.point(
                                    (column, row),
                                    fill=255 - recivedata[column*192+row]
                            )
                    print("show orignal image")
                    origin_image.save("originalimage.bmp")
                    origin_image.show()
                    pass
                elif str == 'noma':
                    for column in range(0, 192):
                        for row in range(0, 192):
                            nomalize_image_draw.point(
                                    (column, row),
                                    fill=255 - recivedata[column*192+row]
                            )
                    print("show nomalize image")
                    nomalize_image.save("nomalizeimage.bmp")
                    nomalize_image.show()
                    pass
                elif str == 'filt':
                    for column in range(0, 192):
                        for row in range(0, 192):
                            smooth_filter_image_draw.point(
                                    (column, row),
                                    fill=255 - recivedata[column*192+row]
                            )
                    print("show smooth filter image")
                    smooth_filter_image.save("smoothfilterimage.bmp")
                    smooth_filter_image.show()
                    pass
                else:
                    for column in range(0, 192):
                        for row in range(0, 192):
                            origin_image_draw.point(
                                    (column, row),
                                    fill=255 - recivedata[column*192+row]
                            )
                    print("show orignal image")
                    origin_image.show()
                    pass
                msg = dev.write(0x1, senddata, 1000)
            else:
                print("transmit data lenth wrong!")
                break
#                print(recivedata[0:20])
        except BaseException, e:
            print(e)
            break
#        print("\n\r")
    print("USB test over!")
