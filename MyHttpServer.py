import socket
import re
import Myframework

from multiprocessing import Process


class HTTPServer(object):
    """定义一个http服务器类"""
    def __init__(self, app):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.app = app

    def bind(self, port):
        """
        为服务器绑定一个固定的端口号
        :param port: int 端口号
        :return: None
        """
        address = ("", port)
        self.listen_sock.bind(address)

    def start_response(self, status_code, response_headers):
        """
        用来接收响应状态码与响应头
        :param status_code: "200 OK"  状态码
        :param response_headers: [("Server", "MyServer"), ("Content-Type", "text")] 相应头
        :return: None
        """
        res_start_line = "HTTP/1.0 " + status_code + "\r\n"  # 响应的起始行
        # 遍历处理response_headers，形成相应头
        resp_headers = ""
        for header_name, header_value in response_headers:
            resp_headers += (header_name + ": " + header_value + "\r\n")
        # 将拼接好的响应报文前半部分保存
        self.resp_start_line_hearders = res_start_line + resp_headers

    def handle_client(self, c_sock, c_addr):
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

        match_result = re.match(r"(\w+) +(/\S*) +", req_start_line)
        req_method = match_result.group(1)  # 请求方式
        file_path = match_result.group(2)  # 请求路径
        # 构造一个字典，用来保存解析的数据
        environ = {
            "PATH_INFO": file_path,
            "REQUEST_METHOD": req_method
        }
        # 调用框架Application类的对象，获取响应体
        response_body = self.app(environ, self.start_response)
        # 构造最终的响应报文
        res_data = (self.resp_start_line_hearders + "\r\n").encode() + response_body
        c_sock.send(res_data)
        c_sock.close()

    def start(self):
        """开启HTTP服务器运行"""
        self.listen_sock.listen(128)
        while True:
            client_sock, client_addr = self.listen_sock.accept()
            print("客户端 %s 已连接" % (client_addr,))
            p = Process(target=self.handle_client, args=(client_sock, client_addr))
            p.start()
            # 释放client_sock
            client_sock.close()


if __name__ == '__main__':
    http_server = HTTPServer(Myframework.app)
    http_server.bind(8000)
    http_server.start()