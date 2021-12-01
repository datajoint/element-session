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
      # experimenter=list(experimenters)

      ## Lab info
      ## Broz: How can I limit to only items that exist, avoiding blank entries?
      institution=(lab_info['institution']
            if 'institution' in lab_info else ''),
      lab=(lab_info['lab_name']
            if 'lab_name' in lab_info else ''),
      experiment_description=(lab_info['project_description']
            if 'project_description' in lab_info else ''),
      keywords=(lab_info['proj_keyw'] # list
            if 'proj_keyw' in lab_info else []),
      notes=(lab_info['protocol_description']
            if 'protocol_description' in lab_info else ''),
      pharmacology=(lab_info['pharmacology']
            if 'pharmacology' in lab_info else ''),
      related_publications=(lab_info['proj_pubs'] # list
            if 'proj_pubs' in lab_info else []),
      slices=(lab_info['slices']
            if 'slices' in lab_info else ''),
      source_script=(lab_info['repositoryurl']
            if 'repositoryurl' in lab_info else ''),
      surgery=(lab_info['surgery']
            if 'surgery' in lab_info else ''),
      virus=(lab_info['virus'] if 'virus' in lab_info else ''),
      protocol=(lab_info['protocol']
            if 'protocol' in lab_info else '')

      ## AttributeError: 'str' object has no attribute 'parent'
      ## Broz: I thought these were notes about the stimulus?
      ##    Error indicates trying to process stim file itself?
      # stimulus=(lab_info['stimulus']
      #       if 'stimulus' in lab_info else []),


      )
