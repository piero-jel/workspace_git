from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateRequest(_message.Message):
    __slots__ = ("name", "topic", "content", "compression", "pipeline_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    topic: str
    content: str
    compression: str
    pipeline_config: str
    def __init__(self, name: _Optional[str] = ..., topic: _Optional[str] = ..., content: _Optional[str] = ..., compression: _Optional[str] = ..., pipeline_config: _Optional[str] = ...) -> None: ...

class CreateResponse(_message.Message):
    __slots__ = ("code", "job_id", "name", "topic", "compression", "pipeline_config", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    job_id: str
    name: str
    topic: str
    compression: str
    pipeline_config: str
    message: str
    def __init__(self, code: _Optional[int] = ..., job_id: _Optional[str] = ..., name: _Optional[str] = ..., topic: _Optional[str] = ..., compression: _Optional[str] = ..., pipeline_config: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("code", "job_id", "name", "topic", "compression", "stages", "pipeline", "job_status", "ready", "status", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    STAGES_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    JOB_STATUS_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    job_id: str
    name: str
    topic: str
    compression: str
    stages: str
    pipeline: str
    job_status: str
    ready: bool
    status: str
    message: str
    def __init__(self, code: _Optional[int] = ..., job_id: _Optional[str] = ..., name: _Optional[str] = ..., topic: _Optional[str] = ..., compression: _Optional[str] = ..., stages: _Optional[str] = ..., pipeline: _Optional[str] = ..., job_status: _Optional[str] = ..., ready: bool = ..., status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class PutRequest(_message.Message):
    __slots__ = ("job_id", "status")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    status: str
    def __init__(self, job_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class PutResponse(_message.Message):
    __slots__ = ("code", "job_id", "name", "topic", "compression", "stages", "pipeline", "job_status", "ready", "status", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    STAGES_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    JOB_STATUS_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    job_id: str
    name: str
    topic: str
    compression: str
    stages: str
    pipeline: str
    job_status: str
    ready: bool
    status: str
    message: str
    def __init__(self, code: _Optional[int] = ..., job_id: _Optional[str] = ..., name: _Optional[str] = ..., topic: _Optional[str] = ..., compression: _Optional[str] = ..., stages: _Optional[str] = ..., pipeline: _Optional[str] = ..., job_status: _Optional[str] = ..., ready: bool = ..., status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ListJobsRequest(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class ListJobsResponse(_message.Message):
    __slots__ = ("code", "pending", "processing", "completed", "failed", "cancelled", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    PENDING_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    CANCELLED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    pending: _containers.RepeatedScalarFieldContainer[str]
    processing: _containers.RepeatedScalarFieldContainer[str]
    completed: _containers.RepeatedScalarFieldContainer[str]
    failed: _containers.RepeatedScalarFieldContainer[str]
    cancelled: _containers.RepeatedScalarFieldContainer[str]
    message: str
    def __init__(self, code: _Optional[int] = ..., pending: _Optional[_Iterable[str]] = ..., processing: _Optional[_Iterable[str]] = ..., completed: _Optional[_Iterable[str]] = ..., failed: _Optional[_Iterable[str]] = ..., cancelled: _Optional[_Iterable[str]] = ..., message: _Optional[str] = ...) -> None: ...

class ListProvidersResponse(_message.Message):
    __slots__ = ("code", "providers", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    providers: _containers.RepeatedScalarFieldContainer[str]
    message: str
    def __init__(self, code: _Optional[int] = ..., providers: _Optional[_Iterable[str]] = ..., message: _Optional[str] = ...) -> None: ...
