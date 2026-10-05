from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.function import Function
from app.models.expected_mapping import ExpectedMapping
from app.models.policy_evidence import PolicyEvidence


class DBSemanticRepository:
    """
    Loads database records required for semantic FDO analysis.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_application(
        self,
        application_id: str,
    ) -> Application:
        application = self.session.scalar(
            select(Application).where(
                Application.application_id
                == application_id
            )
        )

        if application is None:
            raise ValueError(
                f"Application not found: {application_id}"
            )

        return application

    def get_functions(
        self,
        application_id: str,
    ) -> list[Function]:
        return list(
            self.session.scalars(
                select(Function).where(
                    Function.application_id
                    == application_id
                )
            )
        )

    def get_expected_mappings(
        self,
        application_id: str,
    ) -> list[ExpectedMapping]:
        return list(
            self.session.scalars(
                select(ExpectedMapping).where(
                    ExpectedMapping.application_id
                    == application_id
                )
            )
        )

    def get_policy_evidence(
        self,
        policy_id: str,
    ) -> list[PolicyEvidence]:
        return list(
            self.session.scalars(
                select(PolicyEvidence).where(
                    PolicyEvidence.policy_id
                    == policy_id
                )
            )
        )