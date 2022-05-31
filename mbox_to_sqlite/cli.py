import click
import sqlite_utils
import mailbox


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
def mbox(db_path, mbox_path, table):
    "Import messages from an mbox file"
    db = sqlite_utils.Database(db_path)
    mbox = mailbox.mbox(mbox_path)

    def to_insert():
        for message in mbox.values():
            row = dict(message.items())
            row["payload"] = message.get_payload()
            yield row

    db[table].upsert_all(to_insert(), alter=True, pk="Message-ID")

    if not db[table].detect_fts():
        db[table].enable_fts(["payload", "subject"], create_triggers=True)
