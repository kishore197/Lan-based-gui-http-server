import tkinter as tk
import sqlite3 as sq
import os
import http.server as ht
import socketserver as s
from datetime import datetime
import tkinter.messagebox
import threading
import sys

dir=None
db_dir=None
port=None
con=None
con_obj=None
Flag=False
done=None
http_server_thread=None
httpd=None


class Handler(ht.SimpleHTTPRequestHandler):

  def handle_one_request(self):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    global con_obj,con,Flag,httpd
    con_obj.execute('insert into details values (?,?,?)',(self.client_address[0],self.client_address[1],str(date)))
    con.commit()
    return super().handle_one_request()




class thread_server(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  
  def run(self):
    global Flag,httpd
    Flag=True
    print("in thread")
    while Flag:
      httpd.handle_request()
    httpd.shutdown()
    print('yes')


def start_server():
  dir=text_dir.get("1.0",'end-1c')
  db_dir=text_DBMS.get("1.0",'end-1c')
  port=text_port.get("1.0",'end-1c')
  global con,con_obj
  os.chdir(db_dir)
  con=sq.connect('dbms.db',isolation_level=None,check_same_thread=False)
  con_obj= con.cursor()
  con_obj.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='details';''')
  rows=con_obj.fetchall()
  print('\ndirectory of html files:',dir,'\ndirectory of database:',db_dir,'\nPort:',port)
  if(len(rows)==0 or rows[0][0]!='details'):
    con_obj.execute('create table details (adr varchar(20),port varchar(10),time varchar(50))')
  else:
    print('table already exist!!!')
  os.chdir(dir)
  global httpd
  if(port.isdigit()):
    val = int(port)
    try:
      httpd = s.TCPServer(("", val), Handler)
    except:
      tkinter.messagebox.showinfo("Warning!", "Port already in use!")
    http_server_thread=thread_server()
    http_server_thread.start()
  else:
    print('no')
  



def stop_server():
  global Flag,http_server_thread,httpd
  Flag=False

  os._exit(1)
  
 

def view_table():
  try:
    con_obj.execute('select * from details')
    rows=con_obj.fetchall()
    win=tk.Toplevel(gui)
    win.title('Table')
    win.configure(height=500,width=500)
    win.resizable(False,False)
    text_output=tk.Text(win,height=20,width=50)
    text_output.place(x=50,y=50)
    text_output.insert(tk.END,'IP Address            port                 Time\n\n\n')
    for row in rows:
      text_output.insert(tk.END,str(row)+'\n')
    text_output.configure(state = 'disabled')
    win.mainloop()
  except:
    tkinter.messagebox.showinfo("Warning!", "Error!")



def clear_table():
  try:
    global con,con_obj
    con_obj.execute('delete from details')
    con.commit()
    tkinter.messagebox.showinfo("Message", "Done !")
  except:
    tkinter.messagebox.showinfo("Warning!", "Error !")



gui=tk.Tk()
gui.configure(bg='#FFFFFF',height=250,width=600)
gui.resizable(False,False)
gui.title('HTTP Server')
lb_dir = tk.Label (gui,bg = '#FFFFFF' ,text = 'Enter the directory:')
lb_dir.place(x=50,y=50)
lb_port = tk.Label (gui,bg = '#FFFFFF' ,text = 'Enter the Port:')
lb_port.place(x=75,y=100)
lb_DBMS = tk.Label (gui,bg = '#FFFFFF' ,text = 'Enter the DBMS directory:')
lb_DBMS.place(x=15,y=150)
text_dir = tk.Text(gui,bg = '#FFFFFF' , borderwidth = 1,height=1,width=50)
text_dir.place(x=160,y=50)
text_port = tk.Text(gui,bg = '#FFFFFF' , borderwidth = 1,height=1,width=50)
text_port.place(x=160,y=100)
text_DBMS = tk.Text(gui,bg = '#FFFFFF' , borderwidth = 1,height=1,width=50)
text_DBMS.place(x=160,y=150)
bt_start = tk.Button(gui , text='Start Server',height=1,width=16,fg = '#000000' , bg ='#00ffff',activebackground = '#00bfff',activeforeground = '#000000',borderwidth = 0,command=start_server)
bt_start.place(x=30,y=200)
bt_stop = tk.Button(gui , text='Stop Server',height=1,width=16,fg = '#000000' , bg ='#00ffff',activebackground = '#00bfff',activeforeground = '#000000',borderwidth = 0,command=stop_server)
bt_stop.place(x=170,y=200)
bt_dbms = tk.Button(gui , text='View DBMS',height=1,width=16,fg = '#000000' , bg ='#00ffff',activebackground = '#00bfff',activeforeground = '#000000',borderwidth = 0,command=view_table)
bt_dbms.place(x=310,y=200)
bt_start = tk.Button(gui , text='Clear DBMS',height=1,width=16,fg = '#000000' , bg ='#00ffff',activebackground = '#00bfff',activeforeground = '#000000',borderwidth = 0,command=clear_table)
bt_start.place(x=450,y=200)
gui.mainloop()