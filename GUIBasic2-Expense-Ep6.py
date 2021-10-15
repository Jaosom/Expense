#GUIBasic12-Expense.py
from tkinter import *
from tkinter import ttk, messagebox #ttk is theme of TK
import csv
from datetime import datetime


GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Tong')
GUI.geometry('700x700+1000+500')#รันแบบบแรนด้อม ถ้าอยาก fix ให้กด+ใส่ค่าแกนx+y


# B1 = Button(GUI,text='Hello')#สร้างปุ่ม ใส่ใน GUI สร้าง Text
# B1.pack(ipadx=50,ipady=20) # .pack() ติดปุ่มเข้ากับ GUI หลัก
#ipadx=20 คือกำหนดขนาดปุ่มตามแกน x

######## Menu Bar ##############
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)#ทำกล่องเมนูบาร์
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')
# Help
def About():
    messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ขอแค่ 1 BTC ก็พอแล้ว\nBTC Address: abc')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)#ทำกล่องเมนูบาร์
helpmenu.add_command(label='About',command=About) #command=About เป็นการผูกข้อมูล
# Donate
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)#ทำกล่องเมนูบาร์donatemenu


################################

#----------วิธีการสร้าง Tab---------
Tab = ttk.Notebook(GUI)
#T1 = Frame(Tab,width=400,hight=400) #ใส่ความกว้าง สูง ได้ fix size 
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1) #X มาจาก import * expand ใช้คู่กับ fill เพื่อขยาย BOTH คือขยายทั้งแกน X,Y

icon_t1 = PhotoImage(file='adde.png').subsample(2) # subsample ให้กับการย่อภาพให้ย่อลงมากี่เท่า ใช้ได้กับ png 
icon_t2 = PhotoImage(file='listp.png').subsample(2)

# ใส่ f' เพื่อกำหนดขนาด Tab ให้เท่ากัน ^ คือการให้ข้อความอยู่ตรงกลาง > ชิดขวา < ชิดซ้าย
Tab.add(T1, text=f'{"เพิ่มค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top') 
#Tab คือ notebook add เข้าไปใน frame T1 image เอารูปใส่ใน tab compound กำหนดให้รูปอยู่ตรงไหน
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top') #add เข้าไปใน frame T2

# Download icon ได้ ที่ IconArchive




#-----------------------------------

F1 = Frame(T1)
#F1.place(x=100,y=50) #.place ติดเข้าไปใน frame กำหนดค่า x,y
F1.pack()

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทติย์'}


def Save(event=None):
    expense = v_expense.get()#.get คือการถึงข้อมูล (ดึงค่ามาจาก v_expense = StringVar())
    price = v_price.get()
    amount = v_amount.get()

    if expense == '':
        print('No Data')
        messagebox.showerror('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showerror('Error','กรุณากรอกราคา')
        return
    elif amount == '':
        amount = 1

    total = float(price)*float(amount)
    try:
        total = float(price) * float(amount)
        print('รายการ: {} ราคา: {}'.format(expense,price))
        print('จำนวน: {} รวมเป็นเงิน: {}'.format(amount,total))
        # clear ข้อมูลเก่า ใช้ .set
        text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
        text = text + 'จำนวน {} รวมเป็นเงิน {} บาท'.format(amount,total)
        v_result.set(text)
        v_expense.set('')
        v_price.set('')
        v_amount.set('')

        today = datetime.now().strftime('%a')
        print (today)
        dt = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        dt = days[today]+'-' + dt

        #บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
        with open('savedata.csv','a',encoding='utf8',newline='') as f: #utf8 เพื่อให้พิมพ์ภาษาไทยได้
            # with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
            # 'a' การบันทึกเรื่อยๆ เป็นการเพิ่มข้อมูลต่อจากข้อมูลเก่า
            # newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) # สร้างฟังชั่นสำหรับเขียนข้อมูล
            data = [dt,expense,price,amount,total]
            fw.writerow(data)

        #ทำให้ เคอเซอร์กลับไปตำแหน่งช่องกรอก E1 พิมพ์ให้ตรงกับ with 
        E1.focus()
        update_table()
#-----------------------------
        #update_table()
        #update_record()
#-----------------------------
    except Exception as e: # Exception as e คือการทำให้รู้ว่า error คืออะไร 

        print('ERROR',e)
        messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        #messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        #messagebox.showeinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        v_expense.set('')
        v_price.set('')
        v_amount.set('') 

#ทำให้สามารถถกด enter ได้
GUI.bind('<Return>',Save) # ต้องเพิ่มใน def save(event=None) ด้วย
#.bind คือการเช็คว่ามีการกดปุ่มหรือไม่ Return คือ Enter
        

FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New' ก็ได้ เปลี่ยนตามชื่อ Font

#----------------- Image ------------

main_icon = PhotoImage(file='sp.png').subsample(30)

Mainicon = Label(F1,image=main_icon)
Mainicon.pack(ipady=40)


#-----------text1----------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#ttk.Entry คือ ช่องกรอกข้อความ textvariable คือ ข้อความแบบพิเศษ ต้องมีการประกาศตัวแปร    
#---------------------------

#-----------text2----------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#ttk.Entry คือ ช่องกรอกข้อความ textvariable คือ ข้อความแบบพิเศษ ต้องมีการประกาศตัวแปร    
#---------------------------

#-----------text3----------
L = ttk.Label(F1,text='จำนวน',font=FONT1).pack()
v_amount = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_amount,font=FONT1)
E3.pack()
#ttk.Entry คือ ช่องกรอกข้อความ textvariable คือ ข้อความแบบพิเศษ ต้องมีการประกาศตัวแปร    
#---------------------------



icon_b1 = PhotoImage(file='sv.png').subsample(2)

B2 = ttk.Button(F1,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Save)
#สร้างปุ่ม ใส่ใน F1 สร้าง Text

#ipad ขยายภายใน แกน x,y pad ขยายภายนอก แกน x,y
B2.pack(ipadx=50,ipady=10,pady=20) 

v_result = StringVar()
v_result.set('---------ผลลัพธ์--------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1)
#result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)


######################## TAB2 #########################

def read_csv(): #สร้างโปรแกรมอ่าน csv
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr) #ทำให้ fr เป็น list data
    return data

        #print(data)
        #print('-----')
        #print(data[0][0])
        #for a,b,c,d,e in data:
        #    print(d)

#------------table------------#

L = ttk.Label(T2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

#for i in range(len(header)):
 #   resulttable.heading(header[i],text=header[i])

for h in header:
    resulttable.heading(h,text=h)

headerwidth = [150,170,80,80,80]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)


#resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',30,5,150])


def update_table():
    resulttable.delete(*resulttable.get_children())
    #for c in resulttable.get_childern()
    #   resulttable.delete(c)
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()




GUI.bind('<Tab>',lambda x:E2.focus())
GUI.mainloop()#อยู่บรรทัดสุดท้ายเป็นการรันตลอดเวลาไม่มีจะะทำให้รันไม่สมบูรณ์
