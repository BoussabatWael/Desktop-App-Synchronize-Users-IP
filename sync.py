from http import server
import pipes
import subprocess
import time
from tkinter import *
from logging import root
import tkinter
from wsgiref.simple_server import server_version
import mysql.connector as mysql
from tkinter import TOP, Button, PhotoImage, Toplevel, mainloop
import re
import paramiko
import json
import os
from requests import get
from PIL import ImageTk, Image
import datetime
from os.path import expanduser
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import requests



class Window1:
    
    def __init__(self, master):

        self.master = master
        global path_user
        path_user = expanduser("~")
        global path_credentials
        path_credentials = path_user + "\credentials.txt"
        #### if credentials file exists ####
        try:
            f = open(path_credentials)
            with open(path_credentials, "r") as f:
                info = f.read()
                credential = re.split(",|\n",info)
            try:
                host = 'localhost'   
                DATABASE = "firewall_module"
                DB_USER = "root"
                DB_PASSWORD = ""
     
                connection = mysql.connect(host=host,database=DATABASE,user=DB_USER,password=DB_PASSWORD)
                if connection.is_connected():
                    db_Info = connection.get_server_info()
                    global cursor
                    cursor = connection.cursor(buffered=True)
                    cursor.execute("select database();")
                    record = cursor.fetchone()
                    query = ("SELECT id,username,password,ip_address,auto_sync FROM firewall_users WHERE id = %s AND username = %s AND password = %s AND status IN (1,2,3)")
                    cursor.execute(query,(credential[0],credential[1],credential[2]))
                    global response
                    response = cursor.fetchall()
                    print(response[0])
                    #### if user exists ####
                    if response != [] or len(response) != 0:
                        self.footer = tkinter.Frame(root, bg='#CCCCD1',height=50)
                        self.footer.grid(row=2, sticky='news')
                        self.footer.pack(fill='both', side='bottom')
                        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\loading.png"
                        img = Image.open(path)
                        resize_img = img.resize((100,100))
                        self.img = ImageTk.PhotoImage(resize_img)
                        self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                        self.t66.place(x = 150, y=35)
                        self.t6 = Label(self.master, text="Please hold while we redirect you", font=("Arial Bold",15), bg="#dadade")
                        self.t6.place(x = 47, y=200)
                        self.t7 = Label(self.master, text="Loading ...", font=("Arial Bold",13), bg="#dadade")
                        self.t7.place(x = 165, y=300)
                        pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
                        img_logout = Image.open(pathh)
                        resize_img = img_logout.resize((30,30))
                        self.img_logout = ImageTk.PhotoImage(resize_img)
                        self.BB = Button(self.master, text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout0,border=0,bg="#CCCCD1",fg="#CCCCD1")
                        self.BB.pack()
                        self.BB.place(x=350,y=462,width=40,height=30)
                        root.update()
                        root.after(7000)


                        id_user = response[0][0]
                        username = response[0][1]
                        password_user = response[0][2]
                        content = str(id_user)+","+username+","+password_user
                        #### save user credentials ####
                        with open(path_credentials, 'w') as f:
                            f.write(content)
                        self.master = master

                        #### get user public IP Address ####
                        global local_ip 
                        local_ip = get('https://api.ipify.org').text
                        try:
                            query01 = ("SELECT * FROM firewall_users_servers WHERE user_id =%s AND status IN (1,2,3)")%id_user
                            cursor.execute(query01)
                            global response01
                            response01 = cursor.fetchall()
                            print(response01)
                            len(response01) !=0
                            if response01 != [] and len(response01) != 0 :
                                query00 = ("SELECT firewall_users_servers_rules.* FROM firewall_users_servers_rules JOIN firewall_users_servers on firewall_users_servers_rules.user_server_id = firewall_users_servers.id WHERE firewall_users_servers.user_id=%s AND firewall_users_servers_rules.status = 2")%id_user
                                cursor.execute(query00)
                                global response00
                                response00 = cursor.fetchall()
                                print(response00)
                                if response00 ==[] or len(response00) == 0:
                                    if local_ip == response[0][3]:

                                        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\success.png"
                                        img = Image.open(path)
                                        resize_img = img.resize((150,150))
                                        self.img = ImageTk.PhotoImage(resize_img)
                                        self.t66.config(text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                                        self.t66.place(x = 125, y=35)
                                        self.t6.config(text="IP address matched", font=("Arial Bold",15), bg="#dadade")
                                        self.t6.place(x = 100, y=200)
                                        self.t7.config(text="IP address", font=("Arial Bold",15), bg="#dadade")
                                        self.t7.place(x = 140, y=300)
                                        self.t8 = Label(self.master, text=local_ip, font=("Arial Bold",15), bg="#dadade")
                                        self.t8.place(x = 120, y=340)
                                        pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
                                        img_logout = Image.open(pathh)
                                        resize_img = img_logout.resize((30,30))
                                        self.img_logout = ImageTk.PhotoImage(resize_img)
                                        self.BB = Button(self.master, text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout,border=0,bg="#CCCCD1",fg="#CCCCD1")
                                        self.BB.pack()
                                        self.BB.place(x=350,y=462,width=40,height=30)
                                    else:
                                        self.t7.destroy()
                                        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                        img = Image.open(path)
                                        resize_img = img.resize((150,150))
                                        self.img = ImageTk.PhotoImage(resize_img)
                                        self.t66.config(text="",image=self.img,font=("Arial Bold",15), bg="#dadade",border=0) 
                                        self.t66.place(x = 125, y=35)
                                        self.t6.config(text="Something went wrong...",fg= "red",font=("Arial Bold",14))
                                        self.t6.place(x = 100, y=200)
                                        root.update()
                                else :
                                    ### create logs login ###
                                    now_datetime = datetime.datetime.now()
                                    datetime_str = now_datetime.strftime("%Y-%m-%d %H:%M:%S")
                                    print(datetime_str)
                                    reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('login', '"+datetime_str+"', NULL, '1', %s, '11', %s)")
                                    cursor.execute(reqq,(id_user,id_user))
                                    print("logs created with success")
                                    if response[0][4] == "true":
                                        self.t66.destroy()
                                        self.t6.destroy()
                                        self.t7.destroy()
                                        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\sync.png"
                                        img = Image.open(path)
                                        resize_img = img.resize((120,120))
                                        self.img = ImageTk.PhotoImage(resize_img)
                                        self.t666 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",fg="#dadade",border=0)
                                        self.t666.place(x = 140, y=35)
                                        self.t10 = Label(self.master, text="Synchronizing IP address", font=("Arial Bold",15), bg="#dadade")
                                        self.t10.place(x = 85, y=200)
                                        self.t11 = Label(self.master, text="Loading ...", font=("Arial Bold",13), bg="#dadade")
                                        self.t11.place(x = 165, y=270)
                                        pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
                                        img_logout = Image.open(pathh)
                                        resize_img = img_logout.resize((30,30))
                                        self.img_logout = ImageTk.PhotoImage(resize_img)
                                        self.BB = Button(self.master, text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout4,border=0,bg="#CCCCD1",fg="#ffffff")
                                        self.BB.pack()
                                        self.BB.place(x=350,y=462,width=40,height=30)
                                        root.update()
                                        root.after(1000)
                                        try:
                                            for user_server_rule in response00:
                                                print("user server ruleeeeee")
                                                print(user_server_rule)
                                                query112 = ("SELECT * FROM firewall_users_servers WHERE id = %s AND status IN (1,2,3)")%user_server_rule[5]
                                                cursor.execute(query112)
                                                global response1112
                                                response1112 = cursor.fetchall()
                                                response1112 != []
                                                len(response1112) != 0
                                                query2 = ("SELECT * FROM firewall_servers WHERE id = %s")%response1112[0][4]
                                                cursor.execute(query2)
                                                global response2
                                                response2 = cursor.fetchall()
                                                print(response2)
                                        
                                                query55 = ("SELECT * FROM firewall_rules WHERE id = %s")%user_server_rule[4]
                                                cursor.execute(query55)
                                                global response55
                                                response55 = cursor.fetchall()

                                                if response55[0][6] == 'HTTP' or response55[0][6] == 'HTTPS' or response55[0][6] == 'SSH':
                                                    api_url = "http://localhost/test2.php"

                                                    params = {'server_id': response2[0][0],'Task': 'from_desktop', 'ip_address': local_ip, 'port':response55[0][5],'protocol':'tcp','action':response55[0][1]}
                                                    response_api = requests.post(api_url,json=params)
                                                    print(response_api.status_code)
                                                    #print(json.dumps({"message":"Rule added successfully","code":"success"}))
                                                else:
                                                    api_url = "http://localhost/test2.php"

                                                    params = {'server_id': response2[0][0],'Task': 'from_desktop', 'ip_address': local_ip, 'port':response55[0][5],'protocol':response55[0][6],'action':response55[0][1]}
                                                    response_api = requests.post(api_url,json=params)
                                                    print(response_api.status_code)

                                                if response_api.status_code == 200 :
                                                    #### get account id of user ####
                                                    query = ("SELECT account_id FROM firewall_users WHERE id = %s")%credential[0]
                                                    cursor.execute(query)
                                                    global user
                                                    user = cursor.fetchall()
                                                    account_id = user[0][0]
                                                    print("ACCOUNT ID")
                                                    print(account_id)

                                                    req10 = ("UPDATE firewall_users_servers_rules SET status = 1 WHERE id = %s")%user_server_rule[0]
                                                    cursor.execute(req10)
                                                    print("USER SERVER RULE UPDATED SUCCESSFULLY")

                                                    ###update user ip add ###
                                                    req = ("UPDATE firewall_users SET ip_address = %s WHERE id = %s")
                                                    cursor.execute(req,(local_ip,credential[0]))
                                                    print("USER UPDATED SUCCESSFULLY")

                                                    ### create logs update user ip add ###
                                                    now_datetime0 = datetime.datetime.now()
                                                    datetime_str0 = now_datetime0.strftime("%Y-%m-%d %H:%M:%S")
                                                    print(datetime_str0)
                                                    reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('edit', '"+datetime_str0+"', NULL, '1', %s, '11', %s)")
                                                    cursor.execute(reqq,(credential[0],credential[0]))
                                                    print("logs created with success")

                                                    #### get rules_instances id ####
                                                    print(user_server_rule[4])
                                                    print(response1112[0][4])
                                                    req3 = ("SELECT * FROM firewall_rules_instances WHERE rule_id=%s AND server_id=%s AND status IN (1,2,3)")
                                                    cursor.execute(req3,(user_server_rule[4],response1112[0][4]))
                                                    global dataaa
                                                    dataaa = cursor.fetchall()
                                                    if len(dataaa) != 0 :
                                                        rule_instance_id = dataaa[0][0]
                                                        print("ID RULE INSATCNES :")
                                                        print(rule_instance_id)

                                                        #### create logs create rule instance ####
                                                        now = datetime.datetime.now()
                                                        datetimestr = now.strftime("%Y-%m-%d %H:%M:%S")
                                                        print(datetimestr)
                                                        reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('create', '"+datetimestr+"', NULL, '6', %s, '11', %s)")
                                                        cursor.execute(reqq,(rule_instance_id,credential[0]))
                                                        print("logs created with success")
                                                    else :
                                                        #### add rule to rules instances ####
                                                        print("SERVER ID")
                                                        print(response1112[0][4])
                                                        now_datetime1 = datetime.datetime.now()
                                                        datetime_str1 = now_datetime1.strftime("%Y-%m-%d %H:%M:%S")
                                                        print(datetime_str1)
                                                        req4 = ("INSERT INTO firewall_rules_instances (end_date, start_date, status, rule_id, server_id) VALUES (NULL, '"+datetime_str1+"', '1', %s, %s)")
                                                        cursor.execute(req4,(user_server_rule[4],response1112[0][4]))
                                                        print("RULE INSTANCE ADDED SUCCESSFULLY")

                                                        #### get rules_instances id ####
                                                        req3 = ("SELECT * FROM firewall_rules_instances WHERE rule_id=%s AND server_id=%s AND status IN (1,2,3)")
                                                        cursor.execute(req3,(user_server_rule[4],response1112[0][4]))
                                                        global dataaaaaa
                                                        dataaaaaa = cursor.fetchall()
                                                        rule_instance_id = dataaaaaa[0][0]
                                                        print("ID RULE INSATCNES :")
                                                        print(rule_instance_id)

                                                        #### create logs create rule instance ####
                                                        now = datetime.datetime.now()
                                                        datetimestr = now.strftime("%Y-%m-%d %H:%M:%S")
                                                        print(datetimestr)
                                                        reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('create', '"+datetimestr+"', NULL, '6', %s, '11', %s)")
                                                        cursor.execute(reqq,(rule_instance_id,credential[0]))
                                                        print("logs created with success")

                                                    self.t666.destroy()
                                                    path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\success.png"
                                                    img = Image.open(path)
                                                    resize_img = img.resize((150,150))
                                                    self.img = ImageTk.PhotoImage(resize_img)
                                                    self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                                                    self.t66.place(x = 125, y=35)
                                                    self.t10.config(text="IP address matching done",fg="black",font=("Arial Bold",15))
                                                    self.t10.place(x = 70, y=200)
                                                    self.t11.destroy()
                                                    root.update()
                                                    self.t7 = Label(self.master, text="IP address", font=("Arial Bold",15), bg="#dadade")
                                                    self.t7.place(x = 140, y=300)
                                                    self.t8 = Label(self.master, text=local_ip, font=("Arial Bold",15), bg="#dadade")
                                                    self.t8.place(x = 120, y=340)
                                                else:
                                                    path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                                    img = Image.open(path)
                                                    resize_img = img.resize((150,150))
                                                    self.img = ImageTk.PhotoImage(resize_img)
                                                    self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                                                    self.t66.place(x = 125, y=35)
                                                    self.t10.config(text="Error",fg="red",font=("Arial Bold",14))
                                                    self.t10.place(x = 175, y=200)
                                                    self.t11.config(text="Something went wrong ...",fg="red",font=("Arial Bold",12))
                                                    self.t11.place(x = 100, y=240)
                                                    root.update()
                                                    result = '{ "code":"error", "message":"Cannot connect to the SSH Server..." }'
                                                    print("[!] Cannot connect to the SSH Server")

                                        except:
                                                path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                                img = Image.open(path)
                                                resize_img = img.resize((150,150))
                                                self.img = ImageTk.PhotoImage(resize_img)
                                                self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                                                self.t66.place(x = 125, y=35)
                                                self.t10.config(text="Error",fg="red",font=("Arial Bold",14))
                                                self.t10.place(x = 175, y=200)
                                                self.t11.config(text="Something went wrong ...",fg="red",font=("Arial Bold",12))
                                                self.t11.place(x = 100, y=240)
                                                root.update()
                                                result = '{ "code":"error", "message":"Cannot connect to the SSH Server..." }'
                                                print("[!] Cannot connect to the SSH Server")

                                    else:
                                        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                        img = Image.open(path)
                                        resize_img = img.resize((120,120))
                                        self.img = ImageTk.PhotoImage(resize_img)
                                        self.t66.config(text="",image=self.img, font=("Arial Bold",15), bg="#dadade",fg="#dadade",border=0)
                                        self.t66.place(x = 140, y=35)
                                        self.t6.config(text="IP address not matched", font=("Arial Bold",15), bg="#dadade")
                                        self.t6.place(x = 90, y=190)
                                        self.t7.destroy()
                                        self.t77 = Button(self.master,text='Synchronize IP address',  font=("Arial Bold", 15), command=self.Sync,border=0,bg="#1a6990",fg="#ffffff")
                                        self.t77.place(x=65,y=300,width=270,height=35)
                                        self.t88 = Label(self.master, text="", font=("Arial Bold",15), bg="#dadade")
                                        self.t88.place(x = 85, y=400)

                                        pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
                                        img_logout = Image.open(pathh)
                                        resize_img = img_logout.resize((30,30))
                                        self.img_logout = ImageTk.PhotoImage(resize_img)
                                        self.BBBb = Button(self.master,text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout1,border=0,bg="#CCCCD1",fg="#ffffff")
                                        self.BBBb.pack()
                                        self.BBBb.place(x=350,y=462,width=40,height=30)
                            else:
                                self.t7.destroy()
                                path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                img = Image.open(path)
                                resize_img = img.resize((150,150))
                                self.img = ImageTk.PhotoImage(resize_img)
                                self.t66.config(text="",image=self.img,font=("Arial Bold",15), bg="#dadade",border=0) 
                                self.t66.place(x = 125, y=35)
                                self.t6.config(text="User not assigned to any server",fg= "red",font=("Arial Bold",14))
                                self.t6.place(x = 60, y=200)
                                root.update()
                        except:
                            self.t7.destroy()
                            path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                            img = Image.open(path)
                            resize_img = img.resize((150,150))
                            self.img = ImageTk.PhotoImage(resize_img)
                            self.t66.config(text="",image=self.img,font=("Arial Bold",15), bg="#dadade",border=0) 
                            self.t66.place(x = 125, y=35)
                            self.t6.config(text="User not assigned to any server",fg= "red",font=("Arial Bold",14))
                            self.t6.place(x = 60, y=200)
                            root.update()
                    
                    else: 
                        bg_shape = Image.open(r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\shape.png")
                        resize_imgshape = bg_shape.resize((350, 290))
                        self.bgshape = ImageTk.PhotoImage(resize_imgshape)
                        self.l = Label( root, image = self.bgshape,bg='#dadade')
                        self.l.place(x = 50,y = 235)

                        self.L0 = Label(self.master, text="Welcome", font=("Arial Bold", 22), bg='#dadade',fg="#323a5e")
                        self.L0.place(x=130, y=90)

                        bg_img = Image.open(r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\loginbg.png")
                        resize_img = bg_img.resize((100, 30))
                        self.bg = ImageTk.PhotoImage(resize_img)
                        self.ll = Label( self.master, image = self.bg,bg='#dadade')
                        self.ll.place(x = 145,y = 50)
                    
                        self.T1 = Entry(self.master,bd = 0,font=("Arial",11),highlightthickness=1)
                        self.T1.config(highlightbackground="#3d466e",highlightcolor="#3d466e")
                        self.T1.insert(0,"  Enter username")
                        self.T1.config(state=DISABLED)
                        self.T1.bind("<Button-1>",click)
                        self.T1.pack()
                        self.T1.place(x=54, y=210, width=290,height=40)

                        self.L2 = Label(self.master, text="Password", font=("Arial Bold", 12), bg='#dadade',fg="#3d466e")
                        self.L2.place(x=50, y=270)
                        self.T2 = Entry(self.master, show='*', bd = 0,highlightthickness=1)
                        self.T2.config(highlightbackground="#3d466e",highlightcolor="#3d466e")
                        self.T2.insert(0,"Enter password")
                        self.T2.config(state=DISABLED)
                        self.T2.bind("<Button-1>",click1)
                        self.T2.pack()
                        self.T2.place(x=54, y=300, width=290,height=40)

                        self.B1 = Button(self.master, text="Login", font=("Arial Bold", 15), command=self.verify,border=0,bg="#053275",fg="#ffffff")
                        self.B1.place(x=54, y=400,width=290,height=40)    
                    
                    
            except :
                bg_shape = Image.open(r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\shape.png")
                resize_imgshape = bg_shape.resize((350, 290))
                self.bgshape = ImageTk.PhotoImage(resize_imgshape)
                self.l = Label( root, image = self.bgshape,bg='#dadade')
                self.l.place(x = 50,y = 235)

                self.L0 = Label(self.master, text="Welcome", font=("Arial Bold", 22), bg='#dadade',fg="#323a5e")
                self.L0.place(x=130, y=90)

                bg_img = Image.open(r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\loginbg.png")
                resize_img = bg_img.resize((100, 30))
                self.bg = ImageTk.PhotoImage(resize_img)
                self.ll = Label( self.master, image = self.bg,bg='#dadade')
                self.ll.place(x = 145,y = 50)

                self.T1 = Entry(self.master,bd = 0,font=("Arial",11),highlightthickness=1)
                self.T1.config(highlightbackground="#3d466e",highlightcolor="#3d466e")
                self.T1.insert(0,"  Enter username")
                self.T1.config(state=DISABLED)
                self.T1.bind("<Button-1>",click)
                self.T1.pack()
                self.T1.place(x=54, y=210, width=290,height=40)

                self.L2 = Label(self.master, text="Password", font=("Arial Bold", 12), bg='#dadade',fg="#3d466e")
                self.L2.place(x=50, y=270)
                self.T2 = Entry(self.master, show='*', bd = 0,highlightthickness=1)
                self.T2.config(highlightbackground="#3d466e",highlightcolor="#3d466e")
                self.T2.insert(0,"Enter password")
                self.T2.config(state=DISABLED)
                self.T2.bind("<Button-1>",click1)
                self.T2.pack()
                self.T2.place(x=54, y=300, width=290,height=40)

                self.B1 = Button(self.master, text="Login", font=("Arial Bold", 15), command=self.verify,border=0,bg="#053275",fg="#ffffff")
                self.B1.place(x=54, y=400,width=290,height=40)

                
        except:
            # keep `root` in `self.master`
            def click(event):
                self.T1.config(state=NORMAL)
                self.T1.delete(0, END)

            def click1(event):
                self.T2.config(state=NORMAL)
                self.T2.delete(0, END)

            self.master = master 
            bg_shape = Image.open(r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\shape.png")
            resize_imgshape = bg_shape.resize((350, 290))
            self.bgshape = ImageTk.PhotoImage(resize_imgshape)
            self.l = Label( root, image = self.bgshape,bg='#dadade')
            self.l.place(x = 50,y = 235)
            
            self.L0 = Label(self.master, text="Welcome", font=("Arial Bold", 22), bg='#dadade',fg="#323a5e")
            self.L0.place(x=130, y=90)

            bg_img = Image.open(r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\loginbg.png")
            resize_img = bg_img.resize((100, 30))
            self.bg = ImageTk.PhotoImage(resize_img)
            self.ll = Label( self.master, image = self.bg,bg='#dadade')
            self.ll.place(x = 145,y = 50)

            self.L1 = Label(self.master, text="User", font=("Arial Bold", 12), bg='#dadade',fg="#3d466e")
            self.L1.place(x=50, y=180)
            self.T1 = Entry(self.master,bd = 0,font=("Arial",11),highlightthickness=1)
            self.T1.config(highlightbackground="#3d466e",highlightcolor="#3d466e")
            self.T1.insert(0,"  Enter username")
            self.T1.config(state=DISABLED)
            self.T1.bind("<Button-1>",click)
            self.T1.pack()
            self.T1.place(x=54, y=210, width=290,height=40)
                
            self.L2 = Label(self.master, text="Password", font=("Arial Bold", 12), bg='#dadade',fg="#3d466e")
            self.L2.place(x=50, y=270)
            self.T2 = Entry(self.master, show='*', bd = 0,highlightthickness=1)
            self.T2.config(highlightbackground="#3d466e",highlightcolor="#3d466e")
            self.T2.insert(0,"Enter password")
            self.T2.config(state=DISABLED)
            self.T2.bind("<Button-1>",click1)
            self.T2.pack()
            self.T2.place(x=54, y=300, width=290,height=40)

            self.B1 = Button(self.master, text="Login", font=("Arial Bold", 15), command=self.verify,border=0,bg="#053275",fg="#ffffff")
            self.B1.place(x=54, y=400,width=290,height=40)


    def Logout0(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t7.destroy()
        self.t6.destroy()
        self.t66.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout00(self):
        ##delete credentials file##
        self.t7.destroy()
        self.t6.destroy()
        self.t66.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t7.destroy()
        self.t8.destroy()
        self.t6.destroy()
        self.t66.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout2(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t10.destroy()
        self.t666.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout1(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t66.destroy()
        self.t6.destroy()
        self.t77.destroy()
        self.t88.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout3(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t10.destroy()
        self.t66.destroy()
        self.t11.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout4(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t10.destroy()
        self.t666.destroy()
        self.t11.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)
            
    def Sync(self):
        #### loading ... ####
        self.t6.config(text="Loading synchronizing IP address ...",fg="black",font=("Arial Bold",15))
        self.t6.place(x=35,y=200)
        root.update()
        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\sync.png"
        img = Image.open(path)
        resize_img = img.resize((120,120))
        self.img = ImageTk.PhotoImage(resize_img)
        self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
        self.t66.place(x = 145, y=35)
        root.update()
        try:
            f = open(path_credentials)
            with open(path_credentials, "r") as f:
                info = f.read()
                print(info)
                            
                credential = re.split(",|\n",info)
                print(credential[0])

            host = 'localhost'   
            DATABASE = "firewall_module"
            DB_USER = "root"
            DB_PASSWORD = ""
     
            connection = mysql.connect(host=host,database=DATABASE,user=DB_USER,password=DB_PASSWORD)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                global cursor
                cursor = connection.cursor(buffered=True)
                cursor.execute("select database();")
            for user_server_rule in response100:
                print("user server ruleeeeee")
                print(user_server_rule)
                query112 = ("SELECT * FROM firewall_users_servers WHERE id = %s AND status IN (1,2,3)")%user_server_rule[5]
                cursor.execute(query112)
                global response1112
                response1112 = cursor.fetchall()
                response1112 != []
                len(response1112) != 0
                query2 = ("SELECT * FROM firewall_servers WHERE id = %s")%response1112[0][4]
                cursor.execute(query2)
                global response2
                response2 = cursor.fetchall()
                print(response2[0])

                query55 = ("SELECT * FROM firewall_rules WHERE id = %s")%user_server_rule[4]
                cursor.execute(query55)

                global response55
                response55 = cursor.fetchall()
                print(response55)
                if response55[0][6] == 'HTTP' or response55[0][6] == 'HTTPS' or response55[0][6] == 'SSH':
                    api_url = "http://localhost/test2.php"
                    params = {'server_id': response2[0][0],'Task': 'from_desktop', 'ip_address': local_ip, 'port':response55[0][5],'protocol':'tcp','action':response55[0][1]}
                    response_api = requests.post(url=api_url,json=params)
                    print(response_api.status_code)
                    #print(json.dumps({"message":"Rule added successfully","code":"success"}))
                else:
                    api_url = "http://localhost/test2.php"
                    params = {'server_id': response2[0][0],'Task': 'from_desktop', 'ip_address': local_ip, 'port':response55[0][5],'protocol':response55[0][6],'action':response55[0][1]}
                    response_api = requests.post(url=api_url,json=params)
                    print(response_api.status_code)
                    #print(json.dumps({"message":"Rule added successfully","code":"success"}))

                if response_api.status_code == 200 :
                    #### get account id of user ####
                    query = ("SELECT account_id FROM firewall_users WHERE id = %s")%credential[0]
                    cursor.execute(query)
                    global value
                    value = cursor.fetchall()
                    account_id = value[0][0]
                    print("ACCOUNT ID")
                    print(account_id)
                    req11 = ("UPDATE firewall_users_servers_rules SET status = 1 WHERE id = %s")%user_server_rule[0]
                    cursor.execute(req11)
                    print("USER SERVER RULE UPDATED SUCCESSFULLY")
                    ### update user ip address ###
                    req = ("UPDATE firewall_users SET ip_address = %s WHERE id = %s")
                    cursor.execute(req,(local_ip,credential[0]))
                    print("USER UPDATED SUCCESSFULLY")
                    ### create logs update user ip add ###
                    now_datetime0 = datetime.datetime.now()
                    datetime_str0 = now_datetime0.strftime("%Y-%m-%d %H:%M:%S")
                    print(datetime_str0)
                    reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('edit', '"+datetime_str0+"', NULL, '1', %s, '11', %s)")
                    cursor.execute(reqq,(credential[0],credential[0]))
                    print("logs created with success")
                    req3 = ("SELECT * FROM firewall_rules_instances WHERE rule_id=%s AND server_id=%s AND status IN (1,2,3)")
                    cursor.execute(req3,(response55[0][0],response2[0][0]))
                    global dataaa
                    dataaa = cursor.fetchall()
                    if len(dataaa) != 0 :
                        rule_instance_id = dataaa[0][0]
                        print("ID RULE INSATCNES :")
                        print(rule_instance_id)
                        #### create logs create rule instance ####
                        now = datetime.datetime.now()
                        datetimestr = now.strftime("%Y-%m-%d %H:%M:%S")
                        print(datetimestr)
                        reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('create', '"+datetimestr+"', NULL, '6', %s, '11', %s)")
                        cursor.execute(reqq,(rule_instance_id,credential[0]))
                        print("logs created with success")
                    else :
                        #### add rule to rules instances ####
                        print("SERVER ID")
                        print(response2[0][0])
                        now_datetime1 = datetime.datetime.now()
                        datetime_str1 = now_datetime1.strftime("%Y-%m-%d %H:%M:%S")
                        print(datetime_str1)
                        req4 = ("INSERT INTO firewall_rules_instances (end_date, start_date, status, rule_id, server_id) VALUES (NULL, '"+datetime_str1+"', '1', %s, %s)")
                        cursor.execute(req4,(response55[0][0],response2[0][0]))
                        print("RULE INSTANCE ADDED SUCCESSFULLY")
                        #### get rules_instances id ####
                        req3 = ("SELECT * FROM firewall_rules_instances WHERE rule_id=%s AND server_id=%s AND status IN (1,2,3)")
                        cursor.execute(req3,(response55[0][0],response2[0][0]))
                        global dataaaaa
                        dataaaaa = cursor.fetchall()
                        rule_instance_id = dataaaaa[0][0]
                        print("ID RULE INSATCNES :")
                        print(rule_instance_id)
                        #### create logs create rule instance ####
                        now = datetime.datetime.now()
                        datetimestr = now.strftime("%Y-%m-%d %H:%M:%S")
                        print(datetimestr)
                        reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('create', '"+datetimestr+"', NULL, '6', %s, '11', %s)")
                        cursor.execute(reqq,(rule_instance_id,credential[0]))
                        print("logs created with success")

                    self.t7.destroy()
                    path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\success.png"
                    img = Image.open(path)
                    resize_img = img.resize((150,150))
                    self.img = ImageTk.PhotoImage(resize_img)
                    self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                    self.t66.place(x = 125, y=35)
                    self.t6.config(text="IP address matching done" ,fg="black",font=("Arial Bold",15))
                    self.t6.place(x = 70, y=200)
                    root.update()
                    self.t7 = Label(self.master, text="IP address", font=("Arial Bold",15), bg="#dadade")
                    self.t7.place(x = 140, y=300)
                    self.t8 = Label(self.master, text=local_ip, font=("Arial Bold",15), bg="#dadade")
                    self.t8.place(x = 120, y=340)

                else:
                    path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                    img = Image.open(path)
                    resize_img = img.resize((150,150))
                    self.img = ImageTk.PhotoImage(resize_img)
                    self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                    self.t66.place(x = 125, y=35)
                    self.t6.config(text="Error",fg="red",font=("Arial Bold",14))
                    self.t6.place(x = 175, y=200)
                    self.t7.config(text="Something went wrong ...",fg="red",font=("Arial Bold",12))
                    self.t7.place(x = 100, y=240)
                    root.update()
                    result = '{ "code":"error", "message":"Cannot connect to the SSH Server..." }'
                    print("[!] Cannot connect to the SSH Server")
        except :
            self.t6.config(text="Error while connecting to database",fg="red",font=("Arial Bold",12))
            self.t6.place(x = 60, y=200)
            root.update()

  
    def verify(self):
        def click(event):
            self.T1.config(state=NORMAL)
            self.T1.delete(0, END)

        def click1(event):
            self.T2.config(state=NORMAL)
            self.T2.delete(0, END)
        #### get and check inputs of login form ####
        if self.T1.get()!="Enter username" and self.T1.get()!="" and self.T2.get()!="Enter password" and self.T2.get()!="" :
            try:
                #### Databse credentials ####
                #host = '45.76.121.27'
                #DATABASE = "firewall_module"
                #DB_USER = "admin"
                #DB_PASSWORD = "Admin@2022"

                host = 'localhost'   
                DATABASE = "firewall_module"
                DB_USER = "root"
                DB_PASSWORD = ""
                            
                connection = mysql.connect(host=host,database=DATABASE,user=DB_USER,password=DB_PASSWORD)
                if connection.is_connected():
                    db_Info = connection.get_server_info()
                    global cursor
                    cursor = connection.cursor(buffered=True)
                    cursor.execute("select database();")
                    record = cursor.fetchone()
                    try:

                        key = 'AAAAAAAAAAAAAAAA' #16 char for AES128
                        #FIX IV
                        iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8') #16 char for AES128
                        data= pad(self.T2.get().encode(),16)
                        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
                        encrypted = base64.b64encode(cipher.encrypt(data))
                        encrypted_pass = encrypted.decode("utf-8", "ignore")
                        query = ("SELECT id,username,password,ip_address,auto_sync FROM firewall_users WHERE username = %s AND password = %s AND status IN (1,2,3)") 
                        cursor.execute(query,(self.T1.get(),encrypted_pass))
                        global res
                        res = cursor.fetchall()
                        res != []
                        len(res) != 0
                        if res != [] and len(res) != 0 :
                            print(res[0])
                            self.ll.destroy()
                            self.l.destroy()
                            self.T1.destroy()
                            self.L1.destroy()
                            self.L0.destroy()
                            self.L2.destroy()
                            self.T2.destroy()
                            self.B1.destroy()

                            self.footer = tkinter.Frame(root, bg='#CCCCD1',height=50)
                            self.footer.grid(row=2, sticky='news')
                            self.footer.pack(fill='both', side='bottom')
                            path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\loading.png"
                            img = Image.open(path)
                            resize_img = img.resize((100,100))
                            self.img = ImageTk.PhotoImage(resize_img)
                            self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                            self.t66.place(x = 150, y=35)
                            self.t6 = Label(self.master, text="Please hold while we redirect you", font=("Arial Bold",15), bg="#dadade")
                            self.t6.place(x = 47, y=200)
                            self.t7 = Label(self.master, text="Loading ...", font=("Arial Bold",13), bg="#dadade")
                            self.t7.place(x = 165, y=300)
                            pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
                            img_logout = Image.open(pathh)
                            resize_img = img_logout.resize((30,30))
                            self.img_logout = ImageTk.PhotoImage(resize_img)
                            self.BB = Button(self.master, text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout00,border=0,bg="#CCCCD1",fg="#CCCCD1")
                            self.BB.pack()
                            self.BB.place(x=350,y=462,width=40,height=30)
                            root.update()

                            root.after(7000)
                            try:
                                query1 = ("SELECT * FROM firewall_users_servers WHERE user_id =%s AND status IN (1,2,3)")%res[0][0]
                                cursor.execute(query1)
                                global response1
                                response1 = cursor.fetchall()
                                print(response1)
                                response1 != []
                                len(response1) != 0
                                if response1 == [] and len(response1) == 0 :
                                    self.t7.destroy()
                                    path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                    img = Image.open(path)
                                    resize_img = img.resize((150,150))
                                    self.img = ImageTk.PhotoImage(resize_img)
                                    self.t66.config(text="",image=self.img,font=("Arial Bold",15), bg="#dadade",border=0) 
                                    self.t66.place(x = 125, y=35)
                                    self.t6.config(text="User not assigned to any server",fg= "red",font=("Arial Bold",14))
                                    self.t6.place(x = 60, y=200)
                                    root.update()
                                elif response1 != [] and len(response1) != 0:
                                    
                                    query100 = ("SELECT firewall_users_servers_rules.* FROM firewall_users_servers_rules JOIN firewall_users_servers on firewall_users_servers_rules.user_server_id = firewall_users_servers.id WHERE firewall_users_servers.user_id=%s AND firewall_users_servers_rules.status = 2")%res[0][0]
                                    cursor.execute(query100)
                                    global response100
                                    response100 = cursor.fetchall()
                                    print(response100)
                                    if response100 ==[] or len(response100) == 0:
                                        local_ip = get('https://api.ipify.org').text
                                        if local_ip == res[0][3]:
                                            id_user = res[0][0]
                                            username = res[0][1]
                                            password_user = res[0][2]
                                            content = str(id_user)+","+username+","+password_user
                                            with open(path_credentials, 'w') as f:
                                                f.write(content)

                                                
                                            path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\success.png"
                                            img = Image.open(path)
                                            resize_img = img.resize((150,150))
                                            self.img = ImageTk.PhotoImage(resize_img)
                                            self.t66.config(text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                                            self.t66.place(x = 125, y=35)
                                            self.t6.config(text="IP address matched", font=("Arial Bold",15), bg="#dadade")
                                            self.t6.place(x = 100, y=200)
                                            self.t7.config(text="IP address", font=("Arial Bold",15), bg="#dadade")
                                            self.t7.place(x = 140, y=300)
                                            self.t8 = Label(self.master, text=local_ip, font=("Arial Bold",15), bg="#dadade")
                                            self.t8.place(x = 120, y=340)
                                            pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
                                            img_logout = Image.open(pathh)
                                            resize_img = img_logout.resize((30,30))
                                            self.img_logout = ImageTk.PhotoImage(resize_img)
                                            self.BB = Button(self.master, text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout,border=0,bg="#CCCCD1",fg="#CCCCD1")
                                            self.BB.pack()
                                            self.BB.place(x=350,y=462,width=40,height=30)
                                      
                                        else:
                                            self.t7.destroy()
                                            path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                            img = Image.open(path)
                                            resize_img = img.resize((150,150))
                                            self.img = ImageTk.PhotoImage(resize_img)
                                            self.t66.config(text="",image=self.img,font=("Arial Bold",15), bg="#dadade",border=0) 
                                            self.t66.place(x = 125, y=35)
                                            self.t6.config(text="Something went wrong...",fg= "red",font=("Arial Bold",14))
                                            self.t6.place(x = 100, y=200)
                                            root.update()
                                    
                                    else:
                                        id_user = res[0][0]
                                        username = res[0][1]
                                        password_user = res[0][2]
                                        content = str(id_user)+","+username+","+password_user
                                        print(str(content))
    
                                        with open(path_credentials, 'w') as f:
                                            f.write(content)
                                        ### create logs login ###
                                        now_datetime = datetime.datetime.now()
                                        datetime_str = now_datetime.strftime("%Y-%m-%d %H:%M:%S")
                                        print(datetime_str)
                                        reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('login', '"+datetime_str+"', NULL, '1', %s, '11', %s)")
                                        cursor.execute(reqq,(id_user,id_user))
                                        print("logs created with success")
                                        
                                        self.t66.destroy()
                                        self.t6.destroy()
                                        self.footer.destroy()
                                        self.another = Window2(self.master)
                                                                  
                            except:
                                self.t7.destroy()
                                path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                                img = Image.open(path)
                                resize_img = img.resize((150,150))
                                self.img = ImageTk.PhotoImage(resize_img)
                                self.t66.config(text="",image=self.img,font=("Arial Bold",15), bg="#dadade",border=0) 
                                self.t66.place(x = 125, y=35)
                                self.t6.config(text="User not assigned to any server",fg= "red",font=("Arial Bold",14))
                                self.t6.place(x = 60, y=200)
                                root.update()
                        
                        else:     
                            self.L0.config(text="User does not exists !!",fg= "red",font=("Arial Bold",14))
                            self.L0.place(x = 105, y=95)
                            root.update()
                    except:
                        self.L0.config(text="User does not exists !!",fg= "red",font=("Arial Bold",14))
                        self.L0.place(x = 105, y=95)
                        root.update()        
            except :
                self.L0.config(text="Error while connecting to database",fg="red",font=("Arial Bold",14))
                self.L0.place(x = 50, y=95)
                root.update()                

        else:
            self.L0.config(text="Please fill the complete field !!",fg="red",font=("Arial Bold",14))
            self.L0.place(x = 65, y=95)
            root.update()
       

class Window2(Window1):
    def __init__(self, master):
        self.master = master
        self.footer = tkinter.Frame(root, bg='#CCCCD1',height=50)
        self.footer.grid(row=2, sticky='news')
        self.footer.pack(fill='both', side='bottom')
        
        host = 'localhost'   
        DATABASE = "firewall_module"
        DB_USER = "root"
        DB_PASSWORD = ""
                    
        connection = mysql.connect(host=host,database=DATABASE,user=DB_USER,password=DB_PASSWORD)
        db_Info = connection.get_server_info()
        global cursor
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        #### get user public IP Address ####
        global local_ip 
        local_ip = get('https://api.ipify.org').text

        if res[0][4] == "true":
            path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\sync.png"
            img = Image.open(path)
            resize_img = img.resize((150,150))
            self.img = ImageTk.PhotoImage(resize_img)
            self.t666 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",fg="#dadade",border=0)
            self.t666.place(x = 115, y=35)
            self.t10 = Label(self.master, text="Synchronizing IP address", font=("Arial Bold",15), bg="#dadade")
            self.t10.place(x = 75, y=200)
            self.t11 = Label(self.master, text="Loading ...", font=("Arial Bold",13), bg="#dadade")
            self.t11.place(x = 150, y=270)
            pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
            img_logout = Image.open(pathh)
            resize_img = img_logout.resize((30,30))
            self.img_logout = ImageTk.PhotoImage(resize_img)
            self.BB = Button(self.master, text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout4,border=0,bg="#CCCCD1",fg="#ffffff")
            self.BB.pack()
            self.BB.place(x=350,y=462,width=40,height=30)
            root.update()
            root.after(1000)
            try:
                f = open(path_credentials)
                with open(path_credentials, "r") as f:
                    info = f.read()
                    print(info) 
                    global credential     
                    credential = re.split(",|\n",info)
                    print(credential[0])

                for user_server_rule in response100:
                    print("user server ruleeeeee")
                    print(user_server_rule)
                    query112 = ("SELECT * FROM firewall_users_servers WHERE id = %s AND status IN (1,2,3)")%user_server_rule[5]
                    cursor.execute(query112)
                    global response1112
                    response1112 = cursor.fetchall()
                    print(response1112)
                    response1112 != []
                    len(response1112) != 0
                    query2 = ("SELECT * FROM firewall_servers WHERE id = %s")%response1112[0][4]
                    cursor.execute(query2)
                    global response2
                    response2 = cursor.fetchall()
                    print(response2)

                    query55 = ("SELECT * FROM firewall_rules WHERE id = %s")%user_server_rule[4]
                    cursor.execute(query55)
                    global response55
                    response55 = cursor.fetchall()
                    if response55[0][6] == 'HTTP' or response55[0][6] == 'HTTPS' or response55[0][6] == 'SSH':
                        api_url = "http://localhost/test2.php"
                        params = {'server_id': response2[0][0],'Task': 'from_desktop', 'ip_address': local_ip, 'port':response55[0][5],'protocol':'tcp','action':response55[0][1]}
                        response_api = requests.post(api_url,json=params)
                        print(response_api.status_code)
                        #print(json.dumps({"message":"Rule added successfully","code":"success"}))
                    else:
                        api_url = "http://localhost/test2.php"
                        params = {'server_id': response2[0][0],'Task': 'from_desktop', 'ip_address': local_ip, 'port':response55[0][5],'protocol':response55[0][6],'action':response55[0][1]}
                        response_api = requests.post(api_url,json=params)
                        print(response_api.status_code)
                        #print(json.dumps({"message":"Rule added successfully","code":"success"}))

                    if response_api.status_code == 200 :
                        #### get account id of user ####
                        query = ("SELECT account_id FROM firewall_users WHERE id = %s")%credential[0]
                        cursor.execute(query)
                        global user
                        user = cursor.fetchall()
                        account_id = user[0][0]
                        print("ACCOUNT ID")
                        print(account_id)
                        req10 = ("UPDATE firewall_users_servers_rules SET status = 1 WHERE id = %s")%user_server_rule[0]
                        cursor.execute(req10)
                        print("USER SERVER RULE UPDATED SUCCESSFULLY")
                        ###update user ip add ###
                        req = ("UPDATE firewall_users SET ip_address = %s WHERE id = %s")
                        cursor.execute(req,(local_ip,credential[0]))
                        print("USER UPDATED SUCCESSFULLY")
                        ### create logs update user ip add ###
                        now_datetime0 = datetime.datetime.now()
                        datetime_str0 = now_datetime0.strftime("%Y-%m-%d %H:%M:%S")
                        print(datetime_str0)
                        reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('edit', '"+datetime_str0+"', NULL, '1', %s, '11', %s)")
                        cursor.execute(reqq,(credential[0],credential[0]))
                        print("logs created with success")
                        #### get rules_instances id ####
                        print(user_server_rule[4])
                        print(response1112[0][4])
                        req3 = ("SELECT * FROM firewall_rules_instances WHERE rule_id=%s AND server_id=%s AND status IN (1,2,3)")
                        cursor.execute(req3,(user_server_rule[4],response1112[0][4]))
                        global dataaa
                        dataaa = cursor.fetchall()
                        if len(dataaa) != 0 :
                            rule_instance_id = dataaa[0][0]
                            print("ID RULE INSATCNES :")
                            print(rule_instance_id)
                            #### create logs create rule instance ####
                            now = datetime.datetime.now()
                            datetimestr = now.strftime("%Y-%m-%d %H:%M:%S")
                            print(datetimestr)
                            reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('create', '"+datetimestr+"', NULL, '6', %s, '11', %s)")
                            cursor.execute(reqq,(rule_instance_id,credential[0]))
                            print("logs created with success")
                        else :
                            #### add rule to rules instances ####
                            print("SERVER ID")
                            print(response1112[0][4])
                            now_datetime1 = datetime.datetime.now()
                            datetime_str1 = now_datetime1.strftime("%Y-%m-%d %H:%M:%S")
                            print(datetime_str1)
                            req4 = ("INSERT INTO firewall_rules_instances (end_date, start_date, status, rule_id, server_id) VALUES (NULL, '"+datetime_str1+"', '1', %s, %s)")
                            cursor.execute(req4,(user_server_rule[4],response1112[0][4]))
                            print("RULE INSTANCE ADDED SUCCESSFULLY")
                            #### get rules_instances id ####
                            req3 = ("SELECT * FROM firewall_rules_instances WHERE rule_id=%s AND server_id=%s AND status IN (1,2,3)")
                            cursor.execute(req3,(user_server_rule[4],response1112[0][4]))
                            global dataaaaaa
                            dataaaaaa = cursor.fetchall()
                            rule_instance_id = dataaaaaa[0][0]
                            print("ID RULE INSATCNES :")
                            print(rule_instance_id)
                            #### create logs create rule instance ####
                            now = datetime.datetime.now()
                            datetimestr = now.strftime("%Y-%m-%d %H:%M:%S")
                            print(datetimestr)
                            reqq = ("INSERT INTO firewall_users_logs (action, action_date, code, element, element_id, source, user_id) VALUES ('create', '"+datetimestr+"', NULL, '6', %s, '11', %s)")
                            cursor.execute(reqq,(rule_instance_id,credential[0]))
                            print("logs created with success")

                        self.t666.destroy()
                        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\success.png"
                        img = Image.open(path)
                        resize_img = img.resize((150,150))
                        self.img = ImageTk.PhotoImage(resize_img)
                        self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                        self.t66.place(x = 125, y=35)
                        self.t10.config(text="IP address matching done",fg="black",font=("Arial Bold",15))
                        self.t10.place(x = 70, y=200)
                        self.t11.destroy()
                        root.update()
                        self.t7 = Label(self.master, text="IP address", font=("Arial Bold",15), bg="#dadade")
                        self.t7.place(x = 140, y=300)
                        self.t8 = Label(self.master, text=local_ip, font=("Arial Bold",15), bg="#dadade")
                        self.t8.place(x = 120, y=340)

                    else:
                        path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                        img = Image.open(path)
                        resize_img = img.resize((150,150))
                        self.img = ImageTk.PhotoImage(resize_img)
                        self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                        self.t66.place(x = 125, y=35)
                        self.t10.config(text="Error",fg="red",font=("Arial Bold",14))
                        self.t10.place(x = 175, y=200)
                        self.t11.config(text="Something went wrong ...",fg="red",font=("Arial Bold",12))
                        self.t11.place(x = 100, y=240)
                        root.update()
                        result = '{ "code":"error", "message":"Cannot connect to the SSH Server..." }'
                        print("[!] Cannot connect to the SSH Server")    
            except:
                path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
                img = Image.open(path)
                resize_img = img.resize((150,150))
                self.img = ImageTk.PhotoImage(resize_img)
                self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",border=0)
                self.t66.place(x = 125, y=35)
                self.t10.config(text="Error",fg="red",font=("Arial Bold",14))
                self.t10.place(x = 175, y=200)
                self.t11.config(text="Something went wrong ...",fg="red",font=("Arial Bold",12))
                self.t11.place(x = 100, y=240)
                root.update()
                result = '{ "code":"error", "message":"Cannot connect to the SSH Server..." }'
                print("[!] Cannot connect to the SSH Server")
    
        else:
            path = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\warning.png"
            img = Image.open(path)
            resize_img = img.resize((120,120))
            self.img = ImageTk.PhotoImage(resize_img)
            self.t66 = Label(self.master, text="",image=self.img, font=("Arial Bold",15), bg="#dadade",fg="#dadade",border=0)
            self.t66.place(x = 140, y=35)
            self.t6 = Label(self.master, text="IP address not matched", font=("Arial Bold",15), bg="#dadade")
            self.t6.place(x = 90, y=190)
            self.t7 = Button(self.master, text='Synchronize IP address',  font=("Arial Bold", 13), command=self.Sync,border=0,bg="#1a6990",fg="#ffffff")
            self.t7.place(x=65,y=300,width=270,height=35)
            self.t8 = Label(self.master, text="", font=("Arial Bold",15), bg="#dadade")
            self.t8.place(x = 85, y=400)
            pathh = r"C:\\Program Files (x86)\\GCS\\IP_SYNC\\logout.png"
            img_logout = Image.open(pathh)
            resize_img = img_logout.resize((30,30))
            self.img_logout = ImageTk.PhotoImage(resize_img)
            self.BB = Button(self.master, text='Logout',  font=("Arial ", 15),image=self.img_logout, command=self.Logout1,border=0,bg="#CCCCD1",fg="#ffffff")
            self.BB.pack()
            self.BB.place(x=350,y=462,width=40,height=30)
    
    
    def Logout1(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t66.destroy()
        self.t6.destroy()
        self.t7.destroy()
        self.t8.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout2(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t10.destroy()
        self.t666.destroy()
        self.another = Window1(self.master)

    def Logout3(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t10.destroy()
        self.t11.destroy()
        self.t66.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout4(self):
        ##delete credentials file##
        os.remove(path_credentials)
        self.t10.destroy()
        self.t666.destroy()
        self.t66.destroy()
        self.t11.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def Logout(self):
         ##delete credentials file##
        os.remove(path_credentials)
        self.t10.destroy()
        self.t66.destroy()
        self.footer.destroy()
        self.another = Window1(self.master)

    def stop(self):
        root.destroy()



root = Tk()
root.title("IP SYNC")
root.iconbitmap(r'C:\\Program Files (x86)\\GCS\\IP_SYNC\\favicon.ico')

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width - 405)
center_y = int(screen_height - 570)

# set the position of the window to the center of the screen
root.geometry(f'{400}x{500}+{center_x}+{center_y}')

root.configure(background="#dadade")
root.resizable(False, False)

run = Window1(root)
root.mainloop()