import datetime

from element_session.export.nwb import session_to_nwb


def test_session_to_nwb():

    session_key = {
        'subject': 'subject5',
        'session_datetime': datetime.datetime(2020, 5, 12, 4, 13, 7)
    }
lab_key = {'lab': 'LabA'}
protocol_key = {'protocol': 'ProtA'}
project_key = {'project': 'ProjA'}
    nwbfile = session_to_nwb(session_key, lab_key=lab_key, protocol_key=protocol_key, project_key=project_key)

    assert nwbfile.session_id == 'subject5_2020-05-12T04:13:07'
    assert nwbfile.session_description == "Test"
    assert nwbfile.session_start_time == datetime.datetime(2020, 5, 12, 4, 13, 7, tzinfo=datetime.timezone.utc)
    assert nwbfile.experimenter == ["User1"]

    assert nwbfile.subject.subject_id == "subject5"
    assert nwbfile.subject.sex == "M"

    assert nwbfile.institution == "Example Uni"
    assert nwbfile.lab == "The Example Lab"

    assert nwbfile.protocol == "ProtA"
    assert nwbfile.notes == "Protocol for managing data ingestion"

    assert nwbfile.experiment_description == "Example project to populate element-lab"