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
            if recurso in self.content.keys():
                httpCode = "200 OK"
                htmlBody = "<html><body> <h1>Acortador URL's <br></h1> Ej: pepito.com " + self.content[recurso] + "</body></html>"
            elif re.match("[0-9]", recurso[1]):
                try:
                    num = int(recurso[1:])
                    try:
                        httpCode = " 301 Moved Permanently\nLocation: http://" + self.dic2[num][13:]
                        htmlBody = ""
                    except KeyError:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body> Recurso no disponible..." + self.form + "</body></html>"
                except ValueError:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body> Recurso no disponible..." + self.form + "</body></html>"
            else:

                    httpCode = "404 Not Found  "
                    htmlBody = "<html><body>Recurso no disponible..." + self.form + "</body></html>"
        elif metodo == "POST":
            if cuerpo == "":
                httpCode = "404"
                htmlBody = "<html><body>Not Found"+self.form+" </body></html>"
            else:
                if cuerpo in self.dic1:
                    httpCode = "200 OK"
                    htmlBody = "<html><body>http://localhost:1234/" + str(self.dic1[cuerpo]) + "</body></html>"
                else:
                    self.seq = self.seq + 1
                    self.dic1[cuerpo] = self.seq
                    self.dic2[self.seq] = cuerpo
                    httpCode = "200 OK"
                    htmlBody = "<html><body> Url ---> http://localhost:1234/" + str(self.dic1[cuerpo]) + "</body></html>"
        return (httpCode, htmlBody)


if __name__ == "__main__":
    try:
        testWebApp = contentApp("localhost", 1234)
    except KeyboardInterrupt:
        print ' Close Socket...'
        sys.exit()
