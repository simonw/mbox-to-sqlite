from click.testing import CliRunner
from mbox_to_sqlite.cli import cli
import pathlib
import pytest
import sqlite_utils

tests_dir = pathlib.Path(__file__).parent


@pytest.mark.parametrize("table", (None, "other"))
def test_mbox(table):
    runner = CliRunner()
    with runner.isolated_filesystem():
        args = ["mbox", "enron.db", str(tests_dir / "enron-sample.mbox")]
        if table is not None:
            args.extend(["--table", table])
        else:
            table = "messages"
        result = runner.invoke(cli, args)
        assert result.exit_code == 0
        db = sqlite_utils.Database("enron.db")
        assert set(db.table_names()) == {
            table,
            "{}_fts".format(table),
            "{}_fts_data".format(table),
            "{}_fts_idx".format(table),
            "{}_fts_docsize".format(table),
            "{}_fts_config".format(table),
        }
        assert list(db[table].rows) == [
            {
                "Message-ID": "<26521776.1075852054120.JavaMail.evans@thyme>",
                "Date": "Fri, 29 Dec 2000 03:49:00 -0800 (PST)",
                "From": "vladimir.gorny@enron.com",
                "To": "tim.belden@enron.com, kevin.presto@enron.com, john.lavorato@enron.com",
                "Subject": "12/28 Power VaR",
                "Cc": "frank.hayden@enron.com, stacey.white@enron.com, lacrecia.davenport@enron.com, \n\tdavid.port@enron.com",
                "Mime-Version": "1.0",
                "Content-Type": "text/plain; charset=us-ascii",
                "Content-Transfer-Encoding": "7bit",
                "Bcc": "frank.hayden@enron.com, stacey.white@enron.com, lacrecia.davenport@enron.com, \n\tdavid.port@enron.com",
                "X-From": "Vladimir Gorny",
                "X-To": "Tim Belden, Kevin M Presto, John J Lavorato",
                "X-cc": "Frank Hayden, Stacey W White, LaCrecia Davenport, David Port",
                "X-bcc": "",
                "X-Folder": "\\Sally_White_Nov2001\\Notes Folders\\West var",
                "X-Origin": "WHITE-S",
                "X-FileName": "swhite.nsf",
                "payload": "As of 12/28 Power VaR increased by $8.7 MM to $43.7 MM (limit of $50 MM) and \nWest Power increased by $9.2 MM to $35.8 MM. This increase is mainly \nattributable to an addition of a long MidC position of ~1.8 MM Mwhs - a deal \nwith BPA: Buy 250-360 MWs for the period 2/01-9/01. See the increase in \ncomponent VaR in 2001 below (Longs are driving the risk in the portfolio).\n\n\n\nVlady.\n",
            },
            {
                "Message-ID": "<29534117.1075852053898.JavaMail.evans@thyme>",
                "Date": "Fri, 9 Mar 2001 02:23:00 -0800 (PST)",
                "From": "valarie.sabo@enron.com",
                "To": "kroum.kroumov@enron.com",
                "Subject": "release to production of scheduling forward obs. report",
                "Cc": "diana.scholtes@enron.com, cara.semperger@enron.com, will.smith@enron.com, \n\tstacey.white@enron.com, tim.belden@enron.com, fran.chang@enron.com, \n\tsamantha.law@enron.com, heather.dunton@enron.com, \n\tduong.luu@enron.com",
                "Mime-Version": "1.0",
                "Content-Type": "text/plain; charset=us-ascii",
                "Content-Transfer-Encoding": "7bit",
                "Bcc": "diana.scholtes@enron.com, cara.semperger@enron.com, will.smith@enron.com, \n\tstacey.white@enron.com, tim.belden@enron.com, fran.chang@enron.com, \n\tsamantha.law@enron.com, heather.dunton@enron.com, \n\tduong.luu@enron.com",
                "X-From": "Valarie Sabo",
                "X-To": "Kroum Kroumov",
                "X-cc": "Diana Scholtes, Cara Semperger, Will Smith, Stacey W White, Tim Belden, Fran Chang, Samantha Law, Heather Dunton, Duong Luu",
                "X-bcc": "",
                "X-Folder": "\\Sally_White_Nov2001\\Notes Folders\\Val",
                "X-Origin": "WHITE-S",
                "X-FileName": "swhite.nsf",
                "payload": 'I\'ve tested the "schedule" version of forward obs.  It seems to be working \nwell.  \n\nThe wish list might include a summary page to show the desks net 0. And it \ncould use a default that pulls all the west desks when the West portfolio is \nclicked, while retaining the flexibility of overriding the west default to \nchoose individual desks - HOWEVER - it does work fine the way it is.\n\nPlease release this to production and let Fran Chang, Heather Dunton, \nSamantha Law and Diana Scholtes know when it is released.  Thanks!',
            },
        ]
