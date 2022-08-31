from falcon import Response


class XHeaderMiddleware:
    def process_request(self, _, resp: Response):
        """Middleware response"""
        resp.append_header("X-Framework", "falcon")
        resp.append_header("X-Framework-Codename", "B")
