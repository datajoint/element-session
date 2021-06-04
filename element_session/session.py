import datajoint as dj
import importlib
import inspect

schema = dj.schema()

_linking_module = None


def activate(schema_name, create_schema=True, create_tables=True, linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server to activate the `session` element
        :param create_schema: when True (default), create schema in the database if it does not yet exist.
        :param create_tables: when True (default), create tables in the database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `session` element:
             Upstream tables:
                + Subject: the subject for which a particular experimental session is associated with
                + Project: the project for which experimental sessions are associated with
                + Experimenter: the experimenter(s) participating in any particular experimental session
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module),\
        "The argument 'dependency' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    schema.activate(schema_name, create_schema=create_schema,
                    create_tables=create_tables, add_objects=linking_module.__dict__)


@schema
class Session(dj.Manual):
    definition = """
    -> Subject
    session_datetime: datetime(3)
    """

    @classmethod
    def make_nwb(cls, session_key):
        from .export import session_to_nwb
        nwb_session = session_to_nwb(session_key)
        nwb_session.subject = _linking_module.Subject.make_nwb(session_key)
        return nwb_session


@schema
class SessionDirectory(dj.Manual):
    definition = """
    -> Session
    ---
    session_dir: varchar(256)       # Path to the data directory for a particular session
    """


@schema
class SessionExperimenter(dj.Manual):
    definition = """
    -> Session
    -> Experimenter
    """


@schema
class SessionNote(dj.Manual):
    definition = """
    -> Session
    ---
    session_note: varchar(1000)
    """


@schema
class ProjectSession(dj.Manual):
    definition = """
    -> Project
    -> Session
    """