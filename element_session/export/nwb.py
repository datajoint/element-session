import datetime
from uuid import uuid4

import numpy as np
from pynwb import NWBFile
from pynwb.file import Subject

from . import session

try:
    import element_animal
    HAVE_ELEMENT_ANIMAL = True
except:
    HAVE_ELEMENT_ANIMAL = False
try:
    import element_lab
    HAVE_ELEMENT_LAB = True
except:
    HAVE_ELEMENT_LAB = False


def session_to_nwb(session_key: dict, subject_id=None):
    """Gather session- and subject-level metadata and use it to create an NWBFile.

    Parameters
    ----------
    session_key: dict,
        e.g.,
        {
            'subject': 'subject5',
            'session_datetime': datetime.datetime(2020, 5, 12, 4, 13, 7)
        }
    subject_id: str, optional
        Indicate subject_id if it cannot be inferred

    Returns
    -------
    pynwb.NWBFile

    mappings:
        Session::KEY -> NWBFile.session_id
        Sesion::session_note -> NWBFile.session_description
        Session::session_datetime -> NWBFile.session_start_time
        SessionExperimenter::experimenter -> NWBFile.experimenter

        subject.Subject.subject -> NWBFile.subject.subject_id
        subject.Subject.sex -> NWBFile.subject.sex

        lab.Lab.institution -> NWBFile.institution
        lab.Lab.lab_name -> NWBFile.lab
        lab.Lab.time_zone -> NWBFile.session_start_time.timezone

    """

    # ensure only one session key is entered
    session_key = (session.Session & session_key).fetch1("KEY")

    session_identifier = {}
    for k, v in session_key.items():
        session_identifier[k] = v.isoformat() if isinstance(v, datetime.datetime) else v

    nwbfile_kwargs = dict(
        session_id="_".join(session_identifier.values()), identifier=str(uuid4()),
    )

    session_info = (
        (session.Session & session_key).join(session.SessionNote, left=True).fetch1()
    )

    nwbfile_kwargs.update(
        session_start_time=session_info["session_datetime"].astimezone(
            datetime.timezone.utc
        )
    )

    if "session_note" in session_info and session_info["session_note"]:
        nwbfile_kwargs.update(session_description=session_info["session_note"])
    else:
        nwbfile_kwargs.update(session_description="no session note found")

    experimenter_pk = np.setxor1d(
        session.SessionExperimenter.primary_key, session.Session.primary_key,
    )

    experimenters = (
        (session.SessionExperimenter & session_key)
        .proj(experimenter=f'CONCAT({"-".join(experimenter_pk)})')
        .fetch("experimenter")
    )

    nwbfile_kwargs.update(
        experimenter=list(experimenters) if list(experimenters) else None
    )

    if HAVE_ELEMENT_ANIMAL and element_animal.subject.schema.is_activated():

        subject_info = (subject.Subject & session_key).fetch1()

        nwbfile_kwargs.update(
            subject=Subject(
                subject_id=subject_info["subject"], sex=subject_info["sex"],
            )
        )

        if HAVE_ELEMENT_LAB and element_lab.lab.schema.is_activated():
            lab_query = lab.Lab & subject.Subject.Lab() & session_key
            if lab_query:
                lab_record = lab_query.fetch1()

            nwbfile_kwargs.update(
                institution=lab_record.get("institution", None),
                lab=lab_record.get("lab_name", None),
            )

            # if timezone is present, localize session_start_time, which is in UTC be default
            if "time_zone" in lab_record and lab_record["time_zone"][:3] == "UTC":
                hours = int(lab_record["time_zone"][3:])
                hours_timedelta = timedelta(hours=hours)
                nwbfile_kwargs["session_start_time"].astimezone(
                    timezone(hours_timedelta)
                )
    else:
        if subject_id is None:
            raise ValueError(
                "If you are not using element_animal, you musts specify a subject_id."
            )
        nwbfile_kwargs.update(subject=Subject(subject_id=subject_id))

    return NWBFile(**nwbfile_kwargs)

