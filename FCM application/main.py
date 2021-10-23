from tkinter import *
import pandas as pd
from tkinter import filedialog
import fcm



def addData():
    root.filename = filedialog.askopenfilename()
    fcm.loadData(root.filename)


def addSubject(entry):
    return





root = Tk()
root.title('FCM')
root.resizable(0, 0)

# Label Frame 1
frame1 = LabelFrame(root, text="Label1", padx=5, pady=5, width=650, height=250)
frame1.grid(row=0, column=0, sticky='nw')
# add excel data Button
addDataButton = Button(frame1, text="Add Data (csv)", padx=10, pady=10, command=addData)
addDataButton.grid(row=0)
# add subject
addSubjectTitle = Label(frame1, text="Mã HP").grid(row=1,columnspan=3)
entrySubject = Entry(frame1, text="Mã_HP")
entrySubject.grid(row=2, columnspan=2)
addSubjectButton = Button(frame1, text="Add", command=lambda:addSubject(str(entrySubject.get())))
addSubjectButton.grid(row=2, column=2)
# addDataButton.pack()


frame2 = LabelFrame(root, text="Label2", padx=5, pady=5, width=650, height=250)
frame3 = LabelFrame(root, text="Label3", padx=5, pady=5, width=1300, height=400)
frame2.grid(row=0, column=1)
frame3.grid(row=1, column=0, columnspan=2)

root.mainloop()
