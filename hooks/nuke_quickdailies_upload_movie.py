# Copyright (c) 2015 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
from sgtk import Hook

class NukeQuickdailiesUploadMovie(Hook):
    """
    Hook that is used to upload quicktime to Shotgun for use in Screening Room.
    """

    def execute(self, mov_path, version_id, comments, **kwargs):
        """
        Main hook entry point

        :param mov_path:    str path to movie on disk
        :version_id:        int id of the Version entity in Shotgun
        :comments:          str comments provided in the quickdaily node when submitted

        :returns:            None
        """
        app = self.parent
        app.log_debug("Uploading movie %s to Shotgun Version %s..." % (mov_path, version_id))
        try:
            result = app.shotgun.upload('Version', version_id, mov_path, 'sg_uploaded_movie')
        except Exception, e:
            app.log_warning("Unable to upload movie to Shotgun: %s" % e)

