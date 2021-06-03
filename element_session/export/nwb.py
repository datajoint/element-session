import numpy as np
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile

from element_session import session


def session_to_nwb(session_key):
    session_key = (session.Session & session_key).fetch1('KEY')

    session_identifier = {}
    for k, v in session_key.items():
        if isinstance(v, datetime):
            session_identifier[k] = v.strftime('%Y%m%d_%H%M%S')

    session_info = (session.Session & session_key).join(session.SessionNote, left=True).fetch1()

    experimenter_pk = np.setxor1d(session.SessionExperimenter.primary_key,
                                  session.Session.primary_key)
    experimenters = (session.SessionExperimenter & session_key).proj(
        experimenter=f'CONCAT({"-".join(experimenter_pk)})').fetch('experimenter')

    return NWBFile(identifier='_'.join(session_identifier.values()),
                   session_description=session_info['session_note'] if session_info['session_note'] else '',
                   session_start_time=session_info['session_datetime'],
                   file_create_date=datetime.now(tzlocal()),
                   experimenter=list(experimenters),
                   data_collection='',
                   institution='',
                   experiment_description='',
                   related_publications='',
                   keywords=[])
