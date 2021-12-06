import datajoint as dj
import numpy as np
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile

from element_session import session

def session_to_nwb_dict(session_key):
    """
    Generate a dictionary object containing required session information.
      Optionally used in combination with other NWB parameters. For example:
      mynwbfile = NWBFile(session_to_nwb(session_key),lab='My Lab')
    :param session_key: Key specifying one entry in session.Session
    :return: dictionary with NWB parameters
    """
    session_key = (session.Session & session_key).fetch1('KEY')

    session_identifier = {}
    for k, v in session_key.items():
        session_identifier[k] = v.strftime('%Y%m%d_%H%M%S') if isinstance(v, datetime) else v

    session_info = (session.Session & session_key).join(session.SessionNote, left=True).fetch1()

    experimenter_pk = np.setxor1d(session.SessionExperimenter.primary_key,
                                  session.Session.primary_key)
    experimenters = (session.SessionExperimenter & session_key).proj(
        experimenter=f'CONCAT({"-".join(experimenter_pk)})').fetch('experimenter')

    session_dict=dict(
      identifier='_'.join(session_identifier.values()),
      session_description=session_info['session_note'] if session_info['session_note'] else '',
      session_start_time=session_info['session_datetime'],
      # source_script='DataJoint element-session NWB exporter',
      # source_script_file_name='element-session/export/nwb.py',
      experimenter=list(experimenters)
      )
    for k in list(session_dict): # Drop blank entries
      if len(str(session_dict[k])) == 0: elem_info.pop(k)
    return session_dict

def session_to_nwb(session_key):
    """
    Generate one NWBFile object representing all session-level information,
      including session identifier, description, start time, etc.

    :param session_key: entry in session.Session table
    :return: NWBFile object
    """
    return NWBFile(**session_to_nwb_dict(session_key))

