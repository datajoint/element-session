import datajoint as dj
import numpy as np
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile

from element_session import session
from element_lab.export import *

def session_to_nwb(session_key,lab_key=None,project_key=None,protocol_key=None):
    session_key = (session.Session & session_key).fetch1('KEY')

    session_identifier = {}
    for k, v in session_key.items():
        session_identifier[k] = v.strftime('%Y%m%d_%H%M%S') if isinstance(v, datetime) else v

    session_info = (session.Session & session_key).join(session.SessionNote, left=True).fetch1()

    ## Broz: I'm not sure which fork has the upstream Experimenter table
    # experimenter_pk = np.setxor1d(session.SessionExperimenter.primary_key,
    #                               session.Session.primary_key)
    # experimenters = (session.SessionExperimenter & session_key).proj(
    #     experimenter=f'CONCAT({"-".join(experimenter_pk)})').fetch('experimenter')

    if [x for x in (lab_key,project_key,protocol_key) if x is not None]:
      lab_info=elemlab_to_nwb_dict(lab_key,project_key,protocol_key)
    else: lab_info={}

    return NWBFile(
      ## Session info
      identifier='_'.join(session_identifier.values()),
      session_description=session_info['session_note'] if session_info['session_note'] else '',
      session_start_time=session_info['session_datetime'],
      source_script_file_name='DataJoint element-session/export/nwb.py',
      # experimenter=list(experimenters)
      **lab_info
      )
