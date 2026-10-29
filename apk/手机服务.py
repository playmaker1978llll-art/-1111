# -*- coding: utf-8 -*-
"""烧心题库 手机网页服务：自动选端口 + 控制台二维码。"""
import http.server, os, socket, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = dict(http.server.SimpleHTTPRequestHandler.extensions_map)
    extensions_map[".html"] = "text/html; charset=utf-8"
    extensions_map[".webmanifest"] = "application/manifest+json; charset=utf-8"
    extensions_map[".js"] = "application/javascript; charset=utf-8"
    extensions_map[".png"] = "image/png"

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

srv = None
port = 8099
for p in range(8099, 8120):
    try:
        srv = http.server.ThreadingHTTPServer(("0.0.0.0", p), Handler)
        port = p
        break
    except OSError:
        continue
if srv is None:
    print("没有可用端口")
    sys.exit(1)

url = "http://%s:%d/" % (lan_ip(), port)
print()
print("  烧心题库 · 手机访问")
print("  手机和电脑连同一个 WiFi，浏览器打开：")
print()
print("      " + url)
print()
try:
    import segno
    qr = segno.make(url)
    try:
        qr.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr.png"), scale=8, border=2)
        print("  二维码已保存为 qr.png（可直接给手机扫）")
    except Exception as e2:
        print("  （二维码图片保存失败：%s）" % e2)
    try:
        qr.terminal(compact=True)
    except Exception:
        pass
except Exception as e:
    print("  （二维码生成失败：%s）" % e)
print()
print("  打开后：安卓 Chrome 菜单→添加到主屏幕；iPhone Safari 分享→添加到主屏幕")
print("  关掉这个窗口，手机就打不开了。")
print()
sys.stdout.flush()
srv.serve_forever()

