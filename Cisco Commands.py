from netmiko import ConnectHandler
import sys
import time
import select
import paramiko
import re
import ping2 as p

platform = 'cisco_ios'
username = 'xxxx' # edit to reflect
password = 'xxxx'  # edit to reflect

def date():
        import datetime

        x = datetime.datetime.now()

        d = str(x.day)
        m = str(x.month)
        a = str(x.year)

        date = d+"-"+m+"-"+a

        return date

def horario():
        import datetime

        x = datetime.datetime.now()

        h = str(x.hour)
        m = str(x.minute)
        s = str(x.second)
        ms = str(x.microsecond)

        if int(h)<10:
                h = "0"+h
        if int(m)<10:
                m = "0"+m
        if int(s)<10:
                s = "0"+s
        
        hour = h+":"+m+":"+s+":"+ms[0:4]
              
        return hour

def tamanho(url):
        ip = open(url,'r')

        tamanho = 0

        for host in ip:
                tamanho+=1

        ip.close()        

        return tamanho

data = date()
hora = horario()

url = "ip.txt"      
tamanhoArquivo = tamanho(url)

log = open('Log_'+data+'.txt','w') ##Arquivo Contendo Logs de Sucesso 
ips = open(url,'r') ##Arquivo Contendo os IPs 

i=1
tarefas=0
output = ""
outputLog = ""

for host in ips:

        porcentagem = round(100/tamanhoArquivo*i)
                                        
        print(f'Tarefa {i} de {tamanhoArquivo}, {porcentagem}%\n')
        
        host = host.strip()

        ping = p.pingIP(host, 4)
            
        if (ping == True):

                outputLog = f" {horario()} ..... Ping {host} okay \n"
                
                try:
                        comandos = open('Log_'+host+'.txt','w') ##Arquivo onde serão salvos os comandos
                        
                        ##print('## Logging into',host,' ##\n')
                        device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
                        device.send_command('terminal length 0')
                        ##device.send_command('enable')
                        
                        outputLog += f" {horario()} ..... Tarefas em {host} Iniciadas \n"

##                        ##SH RUN##
##                        command = "show run"
##                        outputLog += f" {horario()} ..... {command} no host {host} Iniciado\n"
##
##                        ##print('## Iniciando',command,"host",host,'##\n')
##                        output += "#####....."+ command +".....#####\n\n"
##                        output += device.send_command(command)
##                        output += "\n\n#####................#####\n\n"
##
##                        outputLog += f" {horario()} ..... {command} no host {host} Concluido \n"
##                        ##print('##',command,host,'Concluido ##\n')

                        ##SH CDP NEIGHBORS##
                        command = "show cdp neighbors"
                        outputLog += f" {horario()} ..... {command} no host {host} Iniciado\n"

                        ##print('## Iniciando',command,"host",host,'##\n')
                        output += "#####....."+ command +".....#####\n\n"
                        output += device.send_command(command)
                        output += "\n\n#####................#####\n\n"

                        outputLog += f" {horario()} ..... {command} no host {host} Concluido \n"
                        ##print('##',command,host,'Concluido ##\n')

                        ##SH CDP NEIGHBORS DETAIL##
                        command = "show cdp neighbors detail"
                        outputLog += f" {horario()} ..... {command} no host {host} Iniciado\n"

                        ##print('## Iniciando',command,"host",host,'##\n')
                        output += "#####....."+ command +".....#####\n\n"
                        output += device.send_command(command)
                        output += "\n\n#####................#####\n\n"

                        outputLog += f" {horario()} ..... {command} no host {host} Concluido \n"
                        ##print('##',command,host,'Concluido ##\n')

                        ##SH VERSION##
                        command = "show version"
                        outputLog += f" {horario()} ..... {command} no host {host} Iniciado\n"

                        ##print('## Iniciando',command,"host",host,'##\n')
                        output += "#####....."+ command +".....#####\n\n"
                        output += device.send_command(command)
                        output += "\n\n#####................#####\n\n"

                        outputLog += f" {horario()} ..... {command} no host {host} Concluido \n"
                        ##print('##',command,host,'Concluido ##\n')

                        outputLog += f" {horario()} ..... {host} Concluido \n"
                      
                        ##print('## Comandos em',host,'Concluidos ##\n')

                        tarefas+=1
                     
                except:
                        print(f" {horario()}.....## host {host} Falha de Acesso ##\n")
                        

                
                
        else:
              print(f" {horario()}.....## Ping no host {host} Falhou ##\n")
             
        i+=1

##Gravando No Arquivo##
if output != "" and outputLog != "" :

        comandos.write(output)
        log.write(outputLog)

        comandos.close()
        device.disconnect()

        ips.close()
        log.close()

if tamanhoArquivo == 1:
        print('Tarefa Concluida')
else:
        print('Tarefas Concluidas\n')
