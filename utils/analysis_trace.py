"""Auditable stage trace for the MedFindr v1.2 prototype."""
from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Any
@dataclass
class TraceStage:
    name:str
    status:str
    summary:str
    timestamp_utc:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    def to_dict(self)->dict[str,Any]:
        return {"name":self.name,"status":self.status,"summary":self.summary,"timestamp_utc":self.timestamp_utc}
@dataclass
class AnalysisTrace:
    analysis_id:str
    stages:list[TraceStage]=field(default_factory=list)
    def add(self,name:str,status:str,summary:str)->None: self.stages.append(TraceStage(name,status,summary))
    def to_dict(self)->dict[str,Any]:
        return {"analysis_id":self.analysis_id,"stages":[x.to_dict() for x in self.stages]}
