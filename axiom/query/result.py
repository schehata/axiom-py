from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
from enum import Enum


class MessageCode(Enum):
	"""Message codes represents the code associated with the query."""
	UNKNOWN_MESSAGE_CODE = ""
	VIRTUAL_FIELD_FINALIZE_ERROR = "virtual_field_finalize_error"
	MISSING_COLUMN = "missing_column"
	LICENSE_LIMIT_FOR_QUERY_WARNING = "license_limit_for_query_warning"
	DEFAULT_LIMIT_WARNING = "default_limit_warning"


@dataclass
class MessagePriority(Enum):
	"""Message priorities represents the priority of a message associated with a query."""
	TRACE = "trace"
	DEBUG = "debug"
	INFO = "info"
	WARN = "warn"
	ERROR = "error"
	FATAL = "fatal"


@dataclass
class Message:
	"""a message associated with a query result."""
	# priority of the message.
	priority: MessagePriority
	# describes how often a message of this type was raised by the query.
	count: int
	# code of the message.
	code: MessageCode
	# a human readable text representation of the message.
	msg: str


@dataclass
class QueryStatus:
	"""the status of a query result."""
	# the duration it took the query to execute.
	elapsedTime: timedelta
	# the amount of blocks that have been examined by the query.
	blocksExamined: int
	# the amount of rows that have been examined by the query.
	rowsExamined: int
	# the amount of rows that matched the query.
	rowsMatched: int
	# the amount of groups returned by the query.
	numGroups: int
	# describes if the query result is a partial result.
	isPartial: bool
	# ContinuationToken is populated when isPartial is true and must be passed
	# to the next query request to retrieve the next result set.
	continuationToken: str = field(init=False, default=False)
	# describes if the query result is estimated.
	isEstimate: bool = field(init=False)
	# the timestamp of the oldest block examined.
	minBlockTime: datetime
	# the timestamp of the newest block examined.
	maxBlockTime: datetime
	# messages associated with the query.
	messages: List[Message] = field(init=False)


@dataclass
class Entry:
	"""Entry is an event that matched a query and is thus part of the result set."""
	# the time the event occurred. Matches SysTime if not specified
	# during ingestion.
	_time: datetime
	# the time the event was recorded on the server.
	_sysTime: datetime
	# the unique ID of the event row.
	_rowId: str
	# contains the raw data of the event (with filters and aggregations
	# applied).
	data: Dict[str, any]


@dataclass
class EntryGroupAgg:
	"""an aggregation which is part of a group of queried events."""
	# alias is the aggregations alias. If it wasn't specified at query time, it
	# is the uppercased string representation of the aggregation operation.
	op: str
	# value is the result value of the aggregation.
	value: any


@dataclass
class EntryGroup:
	"""a group of queried event."""
	# the unique id of the group.
	id: int
	# group maps the fieldnames to the unique values for the entry.
	group: Dict[str, any]
	# aggregations of the group.
	aggregations: List[EntryGroupAgg]


@dataclass
class Interval:
	"""the interval of queried time series."""
	# startTime of the interval.
	startTime: datetime
	# endTime of the interval.
	endTime: datetime
	# groups of the interval.
	groups: List[EntryGroup]


@dataclass
class Timeseries:
	"""Timeseries are queried time series."""
	# the intervals that build a time series.
	series: List[Interval]
	# totals of the time series.
	totals: List[EntryGroup]


@dataclass
class QueryResult:
    """Result is the result of a query."""
	# Status of the query result.
    status: QueryStatus
	# Matches are the events that matched the query.
    matches: List[Entry]
	# Buckets are the time series buckets.
    buckets: Timeseries
	# SavedQueryID is the ID of the query that generated this result when it
	# was saved on the server. This is only set when the query was send with
	# the `SaveKind` option specified.
    # savedQueryID: str
