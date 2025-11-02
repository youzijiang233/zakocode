# run_keke_multi.py
import http.server
import socketserver
import threading
import webbrowser
import os
import sys

# 监听的端口列表：同时监听 1443 和 1433（可按需修改）
PORTS = [1443, 1433]

# 默认自动打开的 URL（只打开本机回环地址的 1443）
AUTO_OPEN_URL = f"http://127.0.0.1:{PORTS[0]}/"

# 切换工作目录到脚本所在目录（确保 keke.html 在同一目录）
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    # 将根路径 "/" 重定向到 /keke.html
    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.send_response(302)
            # 使用相对路径 keke.html
            self.send_header("Location", "/keke.html")
            self.end_headers()
            return
        return super().do_GET()

    # 取消日志输出以保持控制台整洁；需要调试时可注释掉
    def log_message(self, format, *args):
        return

def serve_on_port(port):
    # 定义一个能重用地址的小工厂
    class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    with ReusableTCPServer(("0.0.0.0", port), CustomHandler) as httpd:
        print(f"[{threading.current_thread().name}] Serving on 0.0.0.0:{port} -> /keke.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"端口 {port} 的服务器发生错误: {e}")

def open_browser(url):
    try:
        webbrowser.open(url)
    except Exception:
        pass

def main():
    # 检查 keke.html 是否存在
    if not os.path.exists(os.path.join(current_dir, "keke.html")):
        print("错误：当前目录没有找到 keke.html，请把 keke.html 和此脚本放在同一目录。")
        sys.exit(1)

    # 创建并启动每个端口的服务器线程
    threads = []
    for i, port in enumerate(PORTS):
        t = threading.Thread(target=serve_on_port, args=(port,), name=f"Server-{port}", daemon=True)
        t.start()
        threads.append(t)

    # 等少许时间再打开浏览器（打开到本机回环地址，便于本机访问）
    threading.Timer(0.8, open_browser, args=(AUTO_OPEN_URL,)).start()

    # 主线程保持运行，接收 Ctrl+C 退出
    try:
        print("服务器已启动。可以通过以下地址访问（示例）：")
        for p in PORTS:
            print(f"  http://127.0.0.1:{p}/")
            print(f"  http://<本机局域网IP>:{p}/   （例如 http://192.168.8.213:{p}/）")
            print(f"  http://<穿透地址>:{p}/       （需端口转发或隧道）")
        print("\n按 Ctrl+C 退出。")
        while True:
            # 让主线程不占 CPU
            threading.Event().wait(3600)
    except KeyboardInterrupt:
        print("\n正在关闭服务器...（稍等）")
        # 线程为 daemon，程序退出时会自动结束

if __name__ == "__main__":
    main()
