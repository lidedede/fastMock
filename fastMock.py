from japronto import Application
import etcd3, json, sys
import mysqlConnect

def handler(request):
    # print(str(res[request.path]))
    if(alldata[request.path]["type"]=="proto"):
        return request.Response(body=alldata[request.path]["mockvalue"])
    else:
        r = json.dumps(alldata[request.path]["mockvalue"])
        return request.Response(text=r)

def covProto(jsonstr):
    #需要protobuf类型的response可以通过配置mock类型（proto）来返回二进制body
    # serverResponseBody = json_format.Parse(jsonstr, prototest_pb2.ServerResponseBody())
    # body = serverResponseBody.SerializeToString()
    #return body
    return "binnary body"


def initData():
    mc = mysqlConnect.MysqlConnect({"HOST": "xx.xx.xx.xx", "USER": "root", "PWD": "xxxx", "DB": "mock"})
    i = mc.query("select * from mockapi")
    res = {}
    for row in i:
        if(row[3]=="proto"):
            body = covProto(row[2])
            res[row[1]] = {"type": row[3], "mockvalue": body}
        else:
            res[row[1]] = {"type": row[3], "mockvalue": row[2]}
    return res


if __name__ == '__main__':
    try:
        theads = sys.argv[1]
    except Exception as e:
        theads = 1
        print(sys.argv)
        print(e)

    app = Application()

    alldata = initData()
    for k in alldata:
        print(k)
        app.router.add_route(k, handler)
    # worker_num 启动时设置，建议等于真cpu个数，debug=True时，控制台会输出请求的path
    app.run(port=80, worker_num=int(theads), debug=False)
