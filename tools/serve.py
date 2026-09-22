# Static server for the working tree with Cache-Control: no-store, so a browser
# never shows you yesterday's CSS.
#   python3 tools/serve.py 8791 src
import http.server, sys, os

os.chdir(sys.argv[2])


class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        # never answer 304 — every request gets a fresh body
        if "If-Modified-Since" in self.headers:
            self.headers.replace_header("If-Modified-Since", "")
        return super().send_head()

    def log_message(self, *a):
        pass


http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
