"""Local dev server for Rapid T&T.

Serves the project folder and falls back to index.html for app routes such as
/element/<id>, so every screen can be opened, reloaded or scanned by its URL.

    python server.py                 # http://localhost:8000
    python server.py --port 3000
    python server.py --host 0.0.0.0  # reachable from a phone on the same Wi-Fi
"""

import argparse
import http.server
import os
from functools import partial

ROOT = os.path.dirname(os.path.abspath(__file__))


class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        # Real files (and directories with an index) are served as-is;
        # anything else is an app route and gets index.html.
        if not os.path.exists(path):
            self.path = "/index.html"
        return super().send_head()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    handler = partial(SPAHandler, directory=ROOT)
    with http.server.ThreadingHTTPServer((args.host, args.port), handler) as httpd:
        shown = "localhost" if args.host in ("127.0.0.1", "0.0.0.0") else args.host
        print(f"Rapid T&T running at http://{shown}:{args.port}/  (Ctrl+C to stop)", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
