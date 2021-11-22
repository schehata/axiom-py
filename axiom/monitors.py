from enum import Enum
from time import timedelta
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Comparison(Enum):
    BELOW = "below"
    BELOW_OR_EQUAL = "belowOrEqual"
    ABOVE = "above"
    ABOVE_OR_EQUAL = "aboveOrEqual"


@dataclass
class Monitor:
    """
    A Monitor continuesly runs a query on a dataset and evaluates its result
    against a configured threshold. Upon reaching those it will invoke the
    configured notifiers.
    """
	# unique ID of the monitor.
    id: str
	# Dataset the monitor belongs to.
    dataset: str
	# Name is the display name of the monitor.
    name: str
	# Description of the monitor.
    description: str
	# DisabledUntil is the time until the monitor is being executed again.
    disabledUntil: str
    # Query is executed by the monitor and the result is compared using the
	# monitors configured comparison operator against the configured threshold.
    query: Query
	# IsAPL is true if the query is an APL query.
    aplQuery: bool
	# Threshold the query result is compared against, which evalutes if the
	# monitor acts or not.
    threshold: float
	# Comparison operator to use for comparing the query result and threshold
	# value.
    comparison: Comparison
	# NoDataCloseWait specifies after which amount of laking a query result,
	# the monitor is closed.
    noDataCloseWaitMinutes: timedelta
	# Frequency the monitor is executed by.
    frequencyMinutes: timedelta
	# Duration the monitor goes back in time and looks at the data it acts on.
    durationMinutes: timedelta
	# Notifiers attached to the monitor.
    notifiers: List[str]
	# LastCheckTime specifies the last time the monitor executed the query and
	# compared its result against the threshold.
    lastCheckTime: str
	# LastCheckState is the state associated with the last monitor execution.
    lastCheckState: Dict[str, str]
	# Disabled is true, if the monitor is disabled and thus not running.
    disabled: bool
	# LastError is the last error that was observed while running the monitor.
    lastError: str


class MonitorsClient:
    """
    MonitorsClient handles communication with the monitor related operations of
    the Axiom API.
    
    Axiom API Reference: /api/v1/monitors
    """

    session: Session

    def __init__(self, session: Session, logger: Logger):
        self.session = session
        self.logger = logger

    def get_list(self) -> List[Monitor]:
        """Lists all available monitors."""
        path = ""
        resp = self.session.get(path)
        
        monitors: List[Monitor] = []
        for rec in resp.json():
            m = dacite.from_dict(data_class=Monitor, data=rec)
            monitors.append(m)

        return monitors

    def get(self, id: str) -> Monitor:
        """Get a monitor by id."""
        path = s.basePath + "/" + id
        resp = self.session.get(path)

        return dacite.from_dict(data_class=Monitor, data=resp.json())

    def create(self, req: Monitor) -> Monitor:
        """Create a monitor with the given properties."""
        path = ""
        resp = self.session.post(path, data=ujson.dumps(asdict(req)))
        monitor = dacite.from_dict(data_class=Dataset, data=res.json())
        self.logger.info(f"created new monitor: {monitor.name}")
        return monitor

    def update(self, id: str, req: Monitor) -> Monitor:
        """Update the monitor identified by the given id with the given properties."""
        path = ""
        resp = self.session.put(path, data=ujson.dumps(asdict(req)))
        monitor = dacite.from_dict(data_class=Dataset, data=res.json())
        self.logger.info(f"updated monitor ({monitor.name})")
        return monitor

    def delete(self, id: str):
        """Delete the monitor identified by the given id."""
        path = ""
        self.session.delete(path)
