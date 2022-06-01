import datetime
from uuid import uuid4
import pynwb

from .. import session

def session_to_nwb(
    session_key: dict,
    lab_key=None,
    project_key=None,
    protocol_key=None,
    additional_nwbfile_kwargs=None,
):
    """Gather session- and subject-level metadata and use it to create an NWBFile. If
    there is no subject_to_nwb export function in the current namespace, subject_id will
    be inferred from the set of primary attributes in the Subject table upstream of Session.

    Parameters
    ----------
    session_key: dict,
        e.g.,
        {
            'subject': 'subject5',
            'session_datetime': datetime.datetime(2020, 5, 12, 4, 13, 7),
        }
        Assumes session_datetime is in UTC time zone.
    lab_key, project_key, protocol_key: dict, optional
        Used to gather additional optional metadata.
    additional_nwbfile_kwargs: dict, optional
        Optionally overwrite or add fields to NWBFile.

    Returns
    -------
    pynwb.NWBFile

    mappings:
        session.Session::KEY -> NWBFile.session_id
        session.Session::session_datetime -> NWBFile.session_start_time
        session.SessionNote::session_note -> NWBFile.session_description
        session.SessionExperimenter::user -> NWBFile.experimenter

        subject.Subject::subject -> NWBFile.subject.subject_id
        subject.Subject::sex -> NWBFile.subject.sex

        lab.Lab::institution -> NWBFile.institution
        lab.Lab::lab_name -> NWBFile.lab

        lab.Protocol::protocol -> NWBFile.protocol
        lab.Protocol::protocol_description -> NWBFile.notes

        lab.Project::project_description -> NWBFile.experiment_description
        lab.ProjectKeywords.keyword -> NWBFile.keywords
        lab.ProjectPublication.publication -> NWBFile.related_publications

    """

    # ensure only one session key is entered
    session_key = (session.Session & session_key).fetch1("KEY")

    session_identifier = {
        k: v.isoformat() if isinstance(v, datetime.datetime) else v
        for k, v in session_key.items()
    }

    nwbfile_kwargs = dict(
        session_id="_".join(session_identifier.values()),
        identifier=str(uuid4()),
    )

    session_info = (
        (session.Session & session_key).join(session.SessionNote, left=True).fetch1()
    )

    nwbfile_kwargs.update(
        session_start_time=session_info["session_datetime"].astimezone(
            datetime.timezone.utc
        )
    )

    nwbfile_kwargs.update(session_description=session_info.get("session_note", ""))

    experimenters = (session.SessionExperimenter & session_key).fetch("user")

    nwbfile_kwargs.update(experimenter=list(experimenters) or None)

    subject_to_nwb = getattr(session._linking_module, "subject_to_nwb", False)

    if subject_to_nwb:
        nwbfile_kwargs.update(subject=subject_to_nwb(session_key))
    else:
        subject_id = "_".join(
            (getattr(session._linking_module, "Subject") & session_key)
            .fetch1("KEY")
            .values()
        )
        nwbfile_kwargs.update(subject=pynwb.file.Subject(subject_id=subject_id))

    if any([lab_key, project_key, protocol_key]):
        element_lab_to_nwb_dict = getattr(
            session._linking_module, "element_lab_to_nwb_dict", False
        )

        if element_lab_to_nwb_dict:
            nwbfile_kwargs.update(
                element_lab_to_nwb_dict(
                    lab_key=lab_key, project_key=project_key, protocol_key=protocol_key
                )
            )

    if additional_nwbfile_kwargs is not None:
        nwbfile_kwargs.update(additional_nwbfile_kwargs)

    return pynwb.NWBFile(**nwbfile_kwargs)
