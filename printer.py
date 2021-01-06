import cups
from escpos.printer import Usb
def print_function():
    i=0
    with open("receipts", "r") as f:
        i = int(f.read())
        f.close()
    e=0
    try:
        with open("receipts_printed", "r") as f:
                e = int(f.read())
                f.close()
    except:
        e = -1
    if i==e:
        return False
    with open("receipts_printed", "w") as f:
        f.write(str(i))
        f.close()
    file_name_to_print = "test" + str(i) + ".txt"
    print("Printing file: ", file_name_to_print)
    try:
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = list(printers.keys())[1]
        print("Printing file: ", file_name_to_print, ", with printer: ", printer_name)
        conn.printFile(printer_name, file_name_to_print, "", {})
    except:
        print("No cup printer")
    try:
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
        p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
        #p.text(file_name_to_print)
        p.image(file_name_to_print)
        p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
        p.cut()
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T20II) """
        p = Usb(0x04b8, 0x0e15, 0, profile="TM-T20II")
        p.image(file_name_to_print)
        p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
        p.cut()
    except:

        print(" no ESCPOS printer")