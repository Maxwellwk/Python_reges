import socket
import re

from multiprocessing import Process


PORT = 9000

# 用户可以获取的网页目录
HTML_ROOT_DIR = "./html"


def handle_client(c_sock, c_addr):
    """
    子进程处理客户端
    :param c_sock: socket类型对象 处理客户端通信用到的socket对象
    :param c_addr: 元组 （ip，port） 客户端的地址信息
    :return: None
    """
    # 接收客户端发送过来的请求数据，即http请求报文数据
    http_req_data = c_sock.recv(1024)
    print("客户端 %s 发送的http请求报文：\n %s" % (c_addr, http_req_data.decode()))

    # 解析客户端的请求报文
    http_req_data_str = http_req_data.decode()
    # 对http_rep_data_str按照"\r\n"分隔符进行分割
    req_start_line = http_req_data_str.split("\r\n")[0]  # 请求起始行
    # 使用正则表达式从起始行中提出请求的文件名
    file_path = re.match(r"\w+ +(/\S*) +", req_start_line).group(1)
    # 如果用户请求的是住路径，返回主页信息
    if file_path == "/":
        file_path = "/index.html"

    try:
        # 打开文件
        file = open(HTML_ROOT_DIR + file_path, "rb")
    except IOError:
        # 表示用户请求的文件不存在，要返回404响应信息
        # 构造响应报文
        resp_star_line = "HTTP/1.0 404 Not Found\r\n"  # 响应起始行
        resp_headers = "Server: MyServer\r\n"  # 响应头
        resp_headers += "Content-Type: text\r\n"
        resp_body = "file not exist!"  # 响应体

        http_resp_data = resp_star_line + resp_headers + "\r\n" + resp_body
        print("客户端 %s 发送的http请求报文：\n %s" % http_resp_data)

        # 传回给客户端的响应数据
        c_sock.send(http_resp_data.encode())
    else:
        # 表示文件存在
        # 读取文件内容
        file_data = file.read()
        # 关闭文件
        file.close()

        # 构造响应报文
        resp_star_line = "HTTP/1.0 200 OK\r\n"  # 响应起始行
        resp_headers = "Server: MyServer\r\n"  # 响应头
        resp_headers += "Content-Type: text/html\r\n"
        resp_body = "hello itcast python"  # 响应体

        http_resp_data = (resp_star_line + resp_headers + "\r\n").encode() + file_data
        print("客户端 %s 发送的http请求报文：\n %s" % http_resp_data)

        # 传回给客户端的响应数据
        c_sock.send(http_resp_data)

    # 关闭socket
    c_sock.close()


def main():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ("", PORT)
    listen_sock.bind(address)
    listen_sock.listen(128)
    while True:
        client_sock, client_addr = listen_sock.accept()
        print("客户端 %s 已连接" % (client_addr,))
        p = Process(target=handle_client, args=(client_sock, client_addr))
        p.start()
        # 释放client_sock
        client_sock.close()


if __name__ == '__main__':
    main()