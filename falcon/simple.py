from __future__ import annotations

from falcon import HTTP_201, Response, Request, MEDIA_JSON


class SimpleResource:
    def on_get(self, _: Request, resp: Response):
        resp.media = {"message": "Hello World"}

    def on_post(self, req: Request, resp: Response):
        error = req.get_param_as_bool("error") or False
        if req.content_type == MEDIA_JSON:
            error = req.media.get("error") or error

        if error:
            raise ValueError("User requested an error")
        resp.media = {"message": "I'm fine"}
        resp.status = HTTP_201
