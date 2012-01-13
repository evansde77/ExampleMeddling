#!/usr/bin/env python3
# encoding: utf-8
"""
WebServer.py

Example module to illustrate setting up a CherryPy based REST server using the biscuit information

Created by Dave Evans on 2012-01-13.
Copyright (c) 2012 evansde77. All rights reserved.
"""

import sys
import os
import cherrypy
import Biscuits.BiscuitDB as BiscuitDB
import Biscuits.BristolBiscuits as Bristol

class Root:
    """
    _Root_
    
    Cherrypy Root 
    """
    @cherrypy.expose
    def index(self):
        """_index_"""
        return "Welcome to BiscuitDB!!\n"


class BiscuitHandler:
    """
    _BiscuitHandler_
    
    Handle requests for biscuit data via URL API calls
    
    """
    @cherrypy.expose
    def index(self):
        """
        _index_
        """
        return "Usage: biscuit/<Country> will return a random biscuit for that country\n"
        

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def biscuit(self, *args):
        """
        _biscuit_
        
        Convert URL biscuit/<country>/<count> into a call to the biscuit DB for the given country
        The country argument can be followed by an optional number of biscuits to return.
        If you ask for lots of biscuits, duplicate biscuits may happen. 
        
        """
        # validate at least one arg and known country
        if not args:
            raise cherrypy.HTTPError(400, "A country was expected but not supplied.")
        country = args[0]
        if not country in BiscuitDB.biscuits:
            raise cherrypy.HTTPError(400, "Unknown Country: {0}".format(country) )

        # validate optional count argument if present
        count = 1
        if len(args) == 2:
            try:
                count = int(args[1])
            except ValueError:
                raise cherrypy.HTTPError(400, "Number of biscuits is not a number: {0}".format(args[1]))
        
        # build JSON response data
        result = {'Results' : [] , "Requested" : {"Country" : country, "Count" : count} }
        for i in range(count):
            result['Results'].append({"Biscuit": BiscuitDB.randomBiscuit(country) } )
        return result
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def count(self, *args):
        """
        _count_
        
        Return the number of known biscuits for the country provided
        """
        if not args:
            raise cherrypy.HTTPError(400, "A country was expected but not supplied.")
        country = args[0]
        if not country in BiscuitDB.biscuits:
            raise cherrypy.HTTPError(400, "Unknown Country: {0}".format(country) )
         
        result = len(BiscuitDB.biscuits[country])  
        return {"Count" : result, "Country" : country}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def incident(self):
        """
        _incident_
        
        generate a Biscuit Incident and return it as JSON
        
        """
        bisc = Bristol.biscuitIncident()
        return bisc
       
    @cherrypy.expose 
    def mike(self):
        """
        _mike_
        
        """
        result = "<html><head><title>Mike Wallace: International Man Of Pastries</title></head>"
        result += "<body><h4>"
        result += Bristol.formattedBiscuitIncident()
        result += "</body></h4></html>"
        return result
        
        

def main():
    """
    _main_
    
    QND Cherrypy server
    """
    settings = { 
      'global': {
         'server.socket_port' : 8888,
         'server.socket_host': "127.0.0.1",
        }
    }
    cherrypy.config.update(settings)
    root = Root()
    root.biscuit = BiscuitHandler()
    cherrypy.quickstart(root)


if __name__ == '__main__':
	main()

