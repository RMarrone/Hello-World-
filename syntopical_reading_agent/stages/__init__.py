"""
Syntopical Reading Stages

Each stage implements a step in the syntopical reading process
from "How to Read a Book" by Mortimer Adler.
"""

from .stage1_survey import SurveyStage
from .stage2_terminology import TerminologyStage
from .stage3_questions import QuestionsStage
from .stage4_issues import IssuesStage
from .stage5_synthesis import SynthesisStage

__all__ = [
    "SurveyStage",
    "TerminologyStage",
    "QuestionsStage",
    "IssuesStage",
    "SynthesisStage",
]
