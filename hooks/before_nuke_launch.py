# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Before App Launch Hook

This hook is executed prior to application launch and is useful if you need
to set environment variables or run scripts as part of the app initialization.
"""

import os
import sys
import tank
import pprint
import subprocess
import pickle


class BeforeNukeLaunch(tank.Hook):
    """
    Hook to set up the system prior to app launch.
    """
    
    def execute(self, app_path, app_args, version, **kwargs):
        """
        The execute functon of the hook will be called prior to starting the required application        
        
        :param app_path: (str) The path of the application executable
        :param app_args: (str) Any arguments the application may require
        :param version: (str) version of the application being run if set in the "versions" settings
                              of the Launcher instance, otherwise None

        """

        # accessing the current context (current shot, etc)
        # can be done via the parent object
        #
        # > multi_launchapp = self.parent
        # > current_entity = multi_launchapp.context.entity
        
        # you can set environment variables like this:
        # os.environ["MY_SETTING"] = "foo bar"
        
        # if you are using a shared hook to cover multiple applications,
        # you can use the engine setting to figure out which application 
        # is currently being launched:
        #
        
        multi_launchapp = self.parent

        home_path = os.path.expanduser("~")
        profile_path = "%s/.profile_jaunt" % home_path
        cmd = 'source %s' % profile_path
        dump = '/usr/bin/python -c "import os,pickle; print pickle.dumps(os.environ)"'
	
        penv = os.popen('%s && %s' % (cmd,dump))
        env = pickle.loads(penv.read())
        os.environ = env
              
        tank.util.prepend_path_to_env_var("NUKE_PATH", os.environ["NUKE_PATH"])
        tank.util.prepend_path_to_env_var("PATH", os.environ["PATH"])
        tank.util.prepend_path_to_env_var("PYTHONPATH", os.environ["PYTHONPATH"])
        multi_launchapp.log_info("SOURCE: " + os.environ["NUKE_PATH"])
        multi_launchapp.log_info("NUKE PATH: " + os.environ["NUKE_PATH"])
        multi_launchapp.log_info("PATH: " + os.environ["PATH"])
        multi_launchapp.log_info("PYTHONPATH: " + os.environ["PYTHONPATH"])
            
        
        
        
        
        