import nfc
import nfc.snep
import threading
import nfc.tag
import ndef
import nfc
import nfc.snep
import threading
import time
import mimetypes
from pathlib import Path
class DefaultSnepServer(nfc.snep.SnepServer):
    def __init__(self, llc):
        nfc.snep.SnepServer.__init__(self, llc, "urn:nfc:sn:snep")

    def process_put_request(self, ndef_message):
        print("client has put an NDEF message")
        for record in ndef_message:
            print(record)
        return nfc.snep.Success

def send_message(llc, message):
    t0 = time.time()
    if not nfc.snep.SnepClient(llc).put_records(message,19):
        print("failed to send message")
    if t0 is not None:
        transfer_time = time.time() - t0
        message_size = len(b''.join(ndef.message_encoder(message)))
        print("message sent in {0:.3f} seconds ({1} byte @ {2:.0f} byte/sec)"
              .format(transfer_time, message_size,
                      message_size / transfer_time))
def run_send_file_action(args, llc):
    with open(args, "rb") as f:

        type= 'unknown'
        mimetype = mimetypes.guess_type(args, strict=False)[0]
        if mimetype is not None:
            type = mimetype
        print(type)

        if "text" in type:
            while 1:
                read=f.read(200)
                if not read:
                    break
                record = ndef.Record(type, args, read)
                send_message(llc, [record])
                print("send {}".format(record))
        else:
            read = f.read()
            record = ndef.Record(type, args, read)
            print("send {}".format(record))
            send_message( llc, [record])
        f.close()
def send_ndef_message(llc):
    #with open("test_send.txt","w") as f:
     #   f.write("File: "+str(Path("imagetest.png").stat().st_size))
    #f.close()
    i = 0
    with open("receipts", "r") as f:
        i = int(f.read())
        f.close()
    run_send_file_action("test" + str(i) + ".txt",llc)
    #run_send_file_action("imagetest.png", llc)
    #run_send_file_action("nfc_test_end.txt", llc)

def startup(llc):
    global my_snep_server
    my_snep_server = DefaultSnepServer(llc)
    return llc

def connected(llc):
    my_snep_server.start()
    threading.Thread(target=send_ndef_message, args=(llc,)).start()
    return True


#clf.close()