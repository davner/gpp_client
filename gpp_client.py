"""Module for the GPP client."""

__all__ = ["GPPClient"]

import logging

from gql import Client
from gql.dsl import DSLQuery, DSLSchema, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
from schemas import ObservationSchema


class GPPClient:
    def __init__(self, api_url: str, api_key: str, schema_path: str):
        """
        Initialize the GPPClient.

        Parameters
        ----------
        api_url : str
            The GraphQL API URL.
        api_key : str
            The API key for authorization.
        schema_path : str
            The path to the pre-downloaded schema.graphql file.
        """

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.transport = RequestsHTTPTransport(
            url=api_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )

        with open(schema_path, "r") as schema_file:
            schema_str = schema_file.read()

        self.client = Client(transport=self.transport, schema=schema_str)
        self.logger.info("GPPClient initialized with API URL: %s", api_url)

        self.dsl_schema = DSLSchema(self.client.schema)

    def get_observation_by_id(self, observation_id: str) -> dict:
        # Build query.
        # TODO: Make dynamic with user supplied fields.
        query = dsl_gql(
            DSLQuery(
                self.dsl_schema.Query.observation.args(
                    **{"observationId": observation_id}
                ).select(
                    self.dsl_schema.Observation.id,
                    self.dsl_schema.Observation.subtitle,
                    self.dsl_schema.Observation.title,
                    self.dsl_schema.Observation.scienceBand,
                    self.dsl_schema.Observation.existence,
                    self.dsl_schema.Observation.posAngleConstraint.select(
                        self.dsl_schema.PosAngleConstraint.mode
                    ),
                )
            )
        )

        # Execute the query.
        with self.client as session:
            result = session.execute(query)
            self.logger.info("Fetched observation: %s", result)

        # Validate return with marshmallow.
        schema = ObservationSchema(partial=True)
        return schema.load(result["observation"])
