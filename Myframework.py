import time
HTML_ROOT_DIR = "./html"


class Application(object):
    """定义一个web服务器应用的核心，起到一个桥梁的作用，相当于一个小框架"""
    def __init__(self, urls):
        """
        创建一个Application类的对象，并保存对应的路由列表信息urls
        :param urls: [(路径，函数), ()]  # 路由列表        
        """
        self.urls = urls

    def __call__(self, environ, start_response):
        """
        对象被当成函数调用时执行的代码
        :param environ: 字典，保存了用户的请求数据
        :param start_response: 函数对象，有服务器提供，接收状态码和响应头
        :return: 响应体
        """
        # 从environ字典中获取用户请求的路径
        path = environ["PATH_INFO"]
        # 根据path路径区分静态和动态
        # path == "/static/index.html"  "/say_ctime"
        if path.startswith("static"):
            # 表示用户请求的是静态文件
            # path == "/static/index.html"  "/say_ctime"
            file_path = path[7:]  # 切取文件路径

            if file_path == "/":
                file_path = "/index.html"

            try:
                # 打开文件
                file = open(HTML_ROOT_DIR + file_path, "rb")
            except IOError:
                # 表示用户请求的文件不存在，要返回404响应信息
                status_code = "404 Not Found"  # 响应状态码
                response_headers = [("Server", "MyServer"), ("Content-Type", "text")]  # 响应头
                start_response(status_code, response_headers)
                return b"file not exist!"   # 响应体
            else:
                # 表示文件存在
                # 读取文件内容
                file_data = file.read()
                # 关闭文件
                file.close()

                status_code = "200 OK"  # 响应状态码
                response_headers = [("Server", "MyServer"), ("Content-Type", "text/html")]  # 响应头
                start_response(status_code, response_headers)
                return file_data
        else:
            # 表示用户请求的是动态程序
            # path == "/say_ctime"
            # 遍历路由列表，找到用户请求的函数
            for view_path, view_fun in self.urls:
                if view_path == path:
                    response_body = view_fun(environ, start_response)
                    return response_body.encode()

            # 循环执行后，程序仍然没有返回，表示用户请求的路径没有找到，所以需要返回404错误
            status_code = "404 Not Found"  # 响应状态码
            response_headers = [("Server", "MyServer"), ("Content-Type", "text")]  # 响应头
            start_response(status_code, response_headers)
            return b"program not exist!"  # 响应体


# 视图函数 view
def say_ctime(environ, start_response):
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


# 视图函数 view
def say_hello(environ, start_response):
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
    return "hello" + str(time.ctime())


urls = [("/say_ctime", say_ctime), ("/hello", say_hello)]  # 路由列表

app = Application(urls)


# 会把app对象传递给服务器，有服务器按照wsgi协议进行调用
# response_body = app(environ, start_response)


