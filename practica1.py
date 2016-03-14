#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 contentApp class
 Simple web application for managing content

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp
import random
import sys
import re
import csv

class contentApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content

    seq = 0
    form = '<form method=POST>  Introduzca la Url:<input type=text name=Url value= http:// ><br/><input type=submit value=Enviar></form>'
    content = {'/': form,
               }
    """
    dic1 = dicionario clave url y valor numero
    dic2 = diccionario clave numero valor url
    """
    dic1 = {}
    dic2 = {}


    def toString(self,dic):
        table=""
        string=""
        for key in dic:
            table="<table style=width:50%><tr><td>URL</td> <td> KEY </td> </tr>"
            string+="<tr><td>"+str(key.replace("%2F","/").replace("%3A",":"))+"</td>"+"<td>"+str(dic[key])+"</td></tr>";
        return table+string;

    def reader(self):
        with open('datos.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                 self.dic1[row[0]]=row[1]
                 self.dic2[int(row[1])]=row[0]
                 aux=int(row[1])
                 if(aux>self.seq):
                     self.seq=aux

    def writer(self):
        with open('datos.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for element in self.dic1:
                spamwriter.writerow([element,self.dic1[element]])

    def parse(self, request):
        """Return the resource name (including /)"""

        metodo = request.split(' ', 2)[0]
        recurso = request.split(' ', 2)[1]

        if metodo == "PUT":
            cuerpo = request.split("\r\n\r\n", 1)[1]
        elif metodo == "POST":
            cuerpo = request.split("\r\n\r\n", 1)[1].split('=')[1].replace('+', '')
        else:
            cuerpo = ""
        return (metodo, recurso, cuerpo)

    def process(self, resourceName):

        """Process the relevant elements of the request.

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """

        (metodo, recurso, cuerpo) = resourceName
        if metodo == "GET":
            if recurso in self.content:
                try:
                    self.reader()
                except IOError:
                    self.dic1={}
                httpCode = "200 OK"
                htmlBody = "<html><body bgcolor=#E6E6FA> <h1 style=color:blue >Acortador URL's <br></h1> Ej: pepito.com " + self.content[recurso] + self.toString(self.dic1)+"</body></html>"

            elif re.match("[0-9]", recurso[1]):
                try:
                    num = int(recurso[1:])
                    try:

                        httpCode = " 302 Found\nLocation: http://" + self.dic2[num][13:]
                        htmlBody = ""
                    except KeyError:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body bgcolor= #FA5858><strong> Recurso no disponible...</strong>" + self.form + "</body></html>"
                except ValueError:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body bgcolor=#FA5858 ><strong> Recurso no disponible...</strong>" + self.form + "</body></html>"
            else:

                    httpCode = "404 Not Found  "
                    htmlBody = "<html><body bgcolor=#FA5858 ><strong>Recurso no disponible...</strong>" + self.form + "</body></html>"
        elif metodo == "POST":
            if cuerpo == "":
                httpCode = "404"
                htmlBody = "<html><body bgcolor=#FA5858 >Not Found"+self.form+" </body></html>"
            else:
                if cuerpo in self.dic1:
                    httpCode = "200 OK"
                    htmlBody = "<html><body bgcolor=#E6E6FA> URL: ---> <a href= http://localhost:1234/"+str(self.dic1[cuerpo])+"> http://localhost:1234/"+ str(self.dic1[cuerpo])+"</a></body></html>"

                else:
                    self.seq = self.seq + 1
                    self.dic1[cuerpo] = self.seq
                    self.dic2[self.seq] = cuerpo
                    self.writer();
                    httpCode = "200 OK"
                    htmlBody = "<html><body bgcolor=#E6E6FA> URL: ---> <a href= http://localhost:1234/"+str(self.dic1[cuerpo])+"> http://localhost:1234/"+ str(self.dic1[cuerpo])+"</a></body></html>"
        return (httpCode, htmlBody)


if __name__ == "__main__":
    try:
        testWebApp = contentApp("localhost", 1234)
    except KeyboardInterrupt:
        print ' Close Socket...'
        sys.exit()
