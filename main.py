from tkinter import *
from pathlib import Path
import cv2
from datetime import datetime
import csv
# from pyzbar.pyzbar import decode
import pyrebase

config = {
    "apiKey": "AIzaSyCZdVNPu7N_suXcaLlQLqNhNYrU3pk-hlU",
    "authDomain": "qr-scan-a55d9.firebaseapp.com",
    "databaseURL": "https://qr-scan-a55d9-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "qr-scan-a55d9",
    "storageBucket": "qr-scan-a55d9.appspot.com",
    "messagingSenderId": "861353015570",
    "appId": "1:861353015570:web:f04db8ebc9546290615bcb",
    "measurementId": "G-0B70BCHP7C"
}
firebase= pyrebase.initialize_app(config)
database = firebase.database()
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

window = Tk()
window.state ("zoomed")
window.title("QR Code Generator & Scanner")
window.geometry("1152x700")
window.configure(bg = "#FFFFFF")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def scanMyQR():
    button_2["state"]=DISABLED
    def scan_qr_code():
        global cap
        cap = cv2.VideoCapture(0)
        qr_code_detector = cv2.QRCodeDetector()
        while True:
            canvas.delete("scanned_text")
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to access webcam.")
                break
            decoded_objs = qr_code_detector.decode(frame)
            for obj in decoded_objs:
                data = obj.data.decode('utf-8')
                cap.release()
                cv2.destroyWindow("QR Code Scanner")
                button_2["state"]=NORMAL
                return data
            cv2.imshow('QR Code Scanner', frame)
            if cv2.waitKey(1) != -1:
                cap.release()
                cv2.destroyWindow("QR Code Scanner")
                button_2["state"]=NORMAL
                break
    cv2.destroyAllWindows()
    if __name__ == "__main__":
        qr_data = scan_qr_code()
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    current_date = now.strftime("%Y-%m-%d")
    OUTPUT_PAT = Path(__file__).parent
    path=OUTPUT_PAT / Path("./DATA/ENTRY.csv")
    f = open(path,'a',newline = '')
    g=open( path,'r',newline = '')
    if qr_data!=None:
        reading = database.child("ENTRY").child(f"{qr_data.split()[1]}").get()
        lnwriter = csv.writer(f)
        r=csv.reader(g)
        for i in r:
            if reading.val()==None:
                lnwriter.writerow(qr_data.split()+[current_date]+[current_time])
                database.child("ENTRY").child(f"{qr_data.split()[1]}").set(qr_data.split()+[current_date]+[current_time])
                canvas.create_text(
                558.5,
                536.0,
                anchor="nw",
                text=f"YOUR ENTRY IS MARKED \n Thank you {qr_data.split()[1]}",
                fill="#008000",
                font=("Martian Mono", 25 * -1),
                tag="scanned_text"
                )
                break
        else:
            canvas.create_text(
                    558.5,
                    550.0,
                    anchor="nw",
                    text="ALREADY DONE SCANNING",
                    fill="#FF0000",
                    font=("Martian Mono", 25 * -1),
                    tag="scanned_text"
            )
            cap.release()
    
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 700,
    width = 1152,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    487.0,
    700.0,
    fill="#C4C4C4",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    243.0,
    350.0,
    image=image_image_1
)

canvas.create_text(
    550.0,
    55.0,
    anchor="nw",
    text="MIR SCANNER",
    fill="#591E22",
    font=("Roboto Bold", 50 * -1)
)

canvas.create_text(
    740.0,
    617.0,
    anchor="nw",
    text="Made by MIRTTUL SIVAKUMAR",
    fill="#000000",
    font=("Roboto Bold", 15 * -1)
)


entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    758.5,
    566.0,
    image=entry_image_2
)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: scanMyQR(),
    relief="flat"
)
button_2.place(
    x=1058.5,
    y=536.0,
    width=161.0,
    height=49.0
)
window.resizable(True, True)
window.mainloop()
