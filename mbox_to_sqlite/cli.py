import click
import sqlite_utils
import sqlite3
import mailbox


def sql_tracer(sql, params):
    print("SQL: {} - params: {}".format(sql, params))


@click.group()
@click.version_option()
def cli():
    "Load email from .mbox files into SQLite"

@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
)
@click.argument(
    "mbox_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False, exists=True),
)
@click.option("--table", default="messages")
@click.option("--tracer", is_flag=True)
@click.option("--lowercol", is_flag=True)

def mbox(db_path, mbox_path, table, tracer, lowercol):
    "Import messages from an mbox file"
    if tracer:
        db = sqlite_utils.Database(db_path, tracer=sql_tracer)
    else:
        db = sqlite_utils.Database(db_path)
    mbox = mailbox.mbox(mbox_path)

    if lowercol:
        message_id = "message-id"
    else:
        message_id = "Message-ID"

    def to_insert():
        for message in mbox.values():
            if lowercol:
                row = dict([(l.lower(), r) for l,r in message.items()])
            else:
                row = dict(message.items())
            row["payload"] = message.get_payload()
            yield row

    db[table].upsert_all(to_insert(), alter=True, pk=message_id)

    if not db[table].detect_fts():
        db[table].enable_fts(["payload", "subject"], create_triggers=True)

