import datetime
from uuid import uuid4
import pynwb
import datajoint as dj

from .. import session_with_id, session_with_datetime

if session_with_datetime.schema.is_activated():
    session = session_with_datetime
elif session_with_id.schema.is_activated():
    session = session_with_id
else:
    raise dj.DataJointError("Session schema has not been activated.")


def session_to_nwb(
    session_key: dict,
    lab_key: dict = None,
    project_key: dict = None,
    protocol_key: dict = None,
    additional_nwbfile_kwargs=None,
) -> pynwb.NWBFile:
    """Return subject and session metadata as NWBFile object

    Gather session- and subject-level metadata and use it to create an NWBFile. If there
    is no subject_to_nwb export function in the current namespace, subject_id will be
    inferred from the set of primary attributes in the Subject table upstream of
    Session.

    Example:
        session_to_nwb(
            session_key={'subject': 'subject5',
                'session_datetime': datetime.datetime(2020, 5, 12, 4, 13, 7)},
            lab_key={"lab": "LabA"}
            )

    Element to NWB Mappings:
        session.Session::KEY -> NWBFile.session_id  \n
        session.Session::session_datetime -> NWBFile.session_start_time \n
        session.SessionNote::session_note -> NWBFile.session_description \n
        session.SessionExperimenter::user -> NWBFile.experimenter \n
        subject.Subject::subject -> NWBFile.subject.subject_id \n
        subject.Subject::sex -> NWBFile.subject.sex \n
        lab.Lab::institution -> NWBFile.institution \n
        lab.Lab::lab_name -> NWBFile.lab \n
        lab.Protocol::protocol -> NWBFile.protocol \n
        lab.Protocol::protocol_description -> NWBFile.notes \n
        lab.Project::project_description -> NWBFile.experiment_description \n
        lab.ProjectKeywords.keyword -> NWBFile.keywords \n
        lab.ProjectPublication.publication -> NWBFile.related_publications \n

    Args:
        session_key (dict): Key for session.Session.
            Assumes session_datetime is in UTC time zone.
        lab_key (dict, optional): Key for lab.Lab. Defaults to None.
        project_key (dict, optional): Key for lab.Project. Defaults to None.
        protocol_key (dict, optional): Key for Lab.Protocol. Defaults to None.
        additional_nwbfile_kwargs (dict, optional): Optionally overwrite or add fields
            to NWBFile. Defaults to None.

    Returns:
        pynwb.NWBFile: NWB file object
    """

    # ensure only one session key is entered
    session_key = (session.Session & session_key).fetch1("KEY")

    session_identifier = {
        k: v.isoformat() if isinstance(v, datetime.datetime) else str(v)
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
