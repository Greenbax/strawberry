from typing import Any, Dict, Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket

from strawberry.asgi import GraphQL as BaseGraphQL
from strawberry.asgi.handlers import GraphQLTransportWSHandler, GraphQLWSHandler
from tests.http.schema import Query, get_schema


class DebuggableGraphQLTransportWSHandler(GraphQLTransportWSHandler):
    async def get_context(self) -> object:
        context = await super().get_context()
        context["ws"] = self._ws
        context["tasks"] = self.tasks
        context["connectionInitTimeoutTask"] = self.connection_init_timeout_task
        return context


class DebuggableGraphQLWSHandler(GraphQLWSHandler):
    async def get_context(self) -> object:
        context = await super().get_context()
        context["ws"] = self._ws
        context["tasks"] = self.tasks
        context["connectionInitTimeoutTask"] = None
        return context


class GraphQL(BaseGraphQL[Dict[str, Any], Query]):
    graphql_transport_ws_handler_class = DebuggableGraphQLTransportWSHandler
    graphql_ws_handler_class = DebuggableGraphQLWSHandler

    async def get_root_value(self, request: Union[Request, WebSocket]) -> Query:
        return Query()

    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Dict[str, Union[Request, WebSocket, Response, str, None]]:
        return {"request": request, "response": response, "custom_value": "Hi"}


def create_app(**kwargs: Any) -> GraphQL:
    return GraphQL(get_schema(), **kwargs)
