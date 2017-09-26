import time




def application(environ, start_response):
    """
    被服务器调用用来处理动态请求，产生响应数据
    :param environ: dict字典，保存了客户端的请求数据
    :param start_response: function函数对象，服务器提供的，用来接收状态码和相应头
    :return: 相应题数据
    """
    status_code = "200 OK"  # 状态码
    response_headers = [("Server", "MyServer"), ("Content-Type", "text")]  # 响应头
    # 通过调用start_response函数，将状态码与响应头返回给服务器
    start_response(status_code, response_headers)


    # 通过返回值，返回响应体
    return time.ctime()


