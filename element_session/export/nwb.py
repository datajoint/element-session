import datetime
from uuid import uuid4
import datajoint as dj
import pynwb

try:
    import element_animal.subject
    HAVE_ELEMENT_ANIMAL = True
except ModuleNotFoundError:
    HAVE_ELEMENT_ANIMAL = False
try:
    import element_lab.lab
    HAVE_ELEMENT_LAB = True
except ModuleNotFoundError:
    HAVE_ELEMENT_LAB = False


def session_to_nwb(
        session_key: dict,
        lab_schema_name=(dj.config['custom']['database.prefix']+'lab'),
        subject_schema_name=(dj.config['custom']['database.prefix']+'subject'),
        session_schema_name=(dj.config['custom']['database.prefix']+'session'),
        subject_id=None,
        lab_key=None,
        project_key=None,
        protocol_key=None,
        additional_nwbfile_kwargs=None):
    """Gather session- and subject-level metadata and use it to create an NWBFile.

    Parameters
    ----------
    session_key: dict,
        e.g.,
        {
            'subject': 'subject5',
            'session_datetime': datetime.datetime(2020, 5, 12, 4, 13, 7)
        }
    {lab/subject/session}_schema_name devault to dj.config['custom']['database.prefix']
        plus the relevant string {lab/subject/session}.
    subject_id: str, optional
        Indicate subject_id if it cannot be inferred
    lab_key, project_key, protocol_key: dict, optional
        Used to gather additional optional metadata.
    additional_nwbfile_kwargs: dict, optional
        Optionally overwrite or add fields to NWBFile.

    Returns
    -------
    pynwb.NWBFile

    mappings:
        Session::KEY -> NWBFile.session_id
        Session::session_note -> NWBFile.session_description
        Session::session_datetime -> NWBFile.session_start_time
        SessionExperimenter::experimenter -> NWBFile.experimenter

        subject.Subject::subject -> NWBFile.subject.subject_id
        subject.Subject::sex -> NWBFile.subject.sex

        lab.Lab::institution -> NWBFile.institution
        lab.Lab::lab_name -> NWBFile.lab

        lab.Protocol::protocol -> NWBFile.protocol
        lab.Protocol::notes -> NWBFile.notes

        lab.Project::experiment_description -> NWBFile.experiment_description
        lab.Project.Keywords.keyword -> NWBFile.keywords
        lab.Project.Publications.publication -> NWBFile.related_publications

    """
    if HAVE_ELEMENT_LAB:
        lab = dj.create_virtual_module('lab', lab_schema_name)
    if HAVE_ELEMENT_ANIMAL:
        subject = dj.create_virtual_module('subject', subject_schema_name)
    session = dj.create_virtual_module('session', session_schema_name)

    # ensure only one session key is entered
    session_key = (session.Session & session_key).fetch1("KEY")

    session_identifier = {
        k: v.isoformat() if isinstance(v, datetime.datetime) else v
        for k, v in session_key.items()}

    nwbfile_kwargs = dict(
        session_id="_".join(session_identifier.values()), identifier=str(uuid4()))

    session_info = (session.Session & session_key).join(session.SessionNote, left=True).fetch1()

    nwbfile_kwargs.update(
        session_start_time=session_info["session_datetime"].astimezone(
            datetime.timezone.utc))

    nwbfile_kwargs.update(session_description=session_info.get("session_note", ""))

    experimenters = list((session.SessionExperimenter & session_key).fetch("user"))

    nwbfile_kwargs.update(experimenter=list(experimenters) or None)

    if HAVE_ELEMENT_ANIMAL:
        from element_animal.export.nwb import subject_to_nwb
        nwbfile_kwargs.update(subject=subject_to_nwb(session_key))

        if HAVE_ELEMENT_LAB and any([lab_key, project_key, protocol_key]):
            from element_lab.export.nwb import element_lab_to_nwb_dict
            nwbfile_kwargs.update(
                element_lab_to_nwb_dict(
                    lab_key=lab_key, project_key=project_key, protocol_key=protocol_key
                )
            )

    else:
        subject_id = subject_id or session_key.get("subject")
        if subject_id is None:
            raise ValueError("You musts specify a subject_id.")
        nwbfile_kwargs.update(subject=pynwb.file.Subject(subject_id=subject_id))

    if additional_nwbfile_kwargs is not None:
        nwbfile_kwargs.update(additional_nwbfile_kwargs)

    return pynwb.NWBFile(**nwbfile_kwargs)
