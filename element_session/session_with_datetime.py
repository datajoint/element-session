import datajoint as dj
import importlib
import inspect

schema = dj.schema()

_linking_module = None


def activate(schema_name, create_schema=True, create_tables=True, linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server to activate
                            the `session` element
        :param create_schema: when True (default), create schema in the
                              database if it does not yet exist.
        :param create_tables: when True (default), create tables in the
                              database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `session` element:
             Upstream tables:
                + Subject: the subject with which an experimental session is associated
                + Project: the project with which experimental sessions are associated
                + Experimenter: the experimenter(s) participating in a given session
                                To supply from element-lab add `Experimenter = lab.User`
                                to your `workflow/pipeline.py` before `session.activate()`
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'dependency' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


@schema
class Session(dj.Manual):
    definition = """
    -> Subject
    session_datetime: datetime
    """


@schema
class SessionDirectory(dj.Manual):
    definition = """
    -> Session
    ---
    session_dir: varchar(256) # Path to the data directory for a session
    """


@schema
class SessionExperimenter(dj.Manual):
    definition = """
    # Individual(s) conducting the session
    -> Session
    -> Experimenter
    """


@schema
class SessionNote(dj.Manual):
    definition = """
    -> Session
    ---
    session_note: varchar(1024)
    """


@schema
class ProjectSession(dj.Manual):
    definition = """
    -> Project
    -> Session
    """
