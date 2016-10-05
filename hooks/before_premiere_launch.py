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

import shutil
from distutils.dir_util import copy_tree


class BeforePremiereLaunch(tank.Hook):
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
        multi_launchapp = self.parent
        # Make sure we will use the same Python interpreter down the line
        os.environ["PYTHON"] = sys.executable
        os.environ["TANK_CONTEXT"] = tank.context.serialize(multi_launchapp.context)
        extensions = multi_launchapp.get_setting("extensions")
        # Install extensions in user directory to avoid permission issues
        extensions_path = os.path.expanduser("~/Library/Application Support/Adobe/CEP/extensions")
        extension_version = multi_launchapp.get_setting("extension_version")
        if not os.path.exists(extensions_path):
            os.makedirs(extensions_path)
        # Loop over all extensions, and create symlinks when needed
        for extension in extensions:
            if extension == "pi-premiere-importcut":
                multi_launchapp.log_info("Checking extension %s..." % extension)
                install_path = os.path.join(extensions_path, extension)
                # note: this doesn't work across mounted network folders
                # so we actually have to copy the files over
                # if not os.path.exists(install_path):
                #     os.symlink(extensions[extension], install_path)
                try:
                    if os.path.exists(install_path):
                        multi_launchapp.log_info("Attempting to remove %s..." % install_path)
                        if os.path.islink(install_path):
                            os.unlink(install_path)
                        else:
                            shutil.rmtree(install_path)
                    source_path = os.path.join(extensions[extension], extension_version)
                    if not os.path.exists(source_path):
                        multi_launchapp.log_info("Source path %s does NOT exist!" % source_path)
                        multi_launchapp.log_info("Unable to copy and launch Premiere with extension")
                        return
                    multi_launchapp.log_info("Attempting to copy %s to %s..." % (source_path, install_path))
                    # os.system('cp -r "%s" "%s"' % (source_path, install_path))
                    copy_tree(source_path, install_path)
                    # Update the panel shotgun projects and render profiles lists
                    multi_launchapp.log_info("Attempting to refresh panel index %s..." % install_path)
                    refresh_panel = "%s/bash/make_index.sh" % install_path
                    refresh_panel = refresh_panel.replace(" ", "\ ")
                    sg = multi_launchapp.shotgun
                    project = sg.find_one("Project", [["id", "is", multi_launchapp.context.project["id"]]], ["tank_name"])
                    cmd = "%s %s" % (refresh_panel, project["tank_name"])
                    multi_launchapp.log_info(cmd)
                    os.system(cmd)
                except Exception, e:
                    multi_launchapp.log_info(e)
                    raise

                multi_launchapp.log_info("Created %s" % install_path)

        # > current_entity = multi_launchapp.context.entity

        # you can set environment variables like this:
        # os.environ["MY_SETTING"] = "foo bar"

        # if you are using a shared hook to cover multiple applications,
        # you can use the engine setting to figure out which application
        # is currently being launched:
        #
        # > multi_launchapp = self.parent
        # > if multi_launchapp.get_setting("engine") == "tk-nuke":
        #       do_something()
