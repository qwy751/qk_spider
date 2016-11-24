import inspect
import json
#此处引用相对路径有问题，名称转换暂时不能执行
from ..names import read_name

def params_to_dict(outer=1):
    """
    根据外层参数名,生成参数字典,当参数值为None时,不生成该项,保证参数名符合接口要求
    :param outer: 本函数为第0层，默认获取调用本函数的参数
    :return: 生成的{参数:值}字典
    """
    cf = inspect.currentframe()
    frame = inspect.getouterframes(cf)[outer][0]
    args, _, _, values = inspect.getargvalues(frame)
    # print('function name "%s"' % inspect.getframeinfo(frame)[2])
    result = {i: values[i] for i in args if values[i] is not None}
    if 'self' in result:
        result.pop('self')

    if 'cls' in result:
        result.pop('cls')
    return result


def convert(report_dict):
    """
    将查询结果转换为json格式
    :param report_dict: 字典或者字典的列表
    :return: 转换产生的json字符串
    """
    converted = convert_dict(report_dict)
    json_str = json.dumps(converted, indent=2, ensure_ascii=False)
    return json_str


def find_name(name):
   name_dict = read_name()
   for n, v in name_dict.items():
       if v == name:
           return n
   return None


def convert_dict(report_dict):
    """
    根据查询结果进行转换，将结果名称换成系统名称，添加其它额外信息
    :param report_dict: 是字典或者字典的列表
    :return: 转换后产生的字典
    """
    result = {}
    # 节点有多项
    if isinstance(report_dict, list):
        for obj in report_dict:
            if isinstance(obj, str):
                # TODO: 这里字符串翻译为指定定义
                result.extend(report_dict)
                break
            result.append(convert_dict(obj))
    elif isinstance(report_dict, dict):
        # 节点为字典
        for name, value in report_dict.items():
            wrap = dict()
            child_value = dict()
            real_name = find_name(name)
            if real_name is not None:
                wrap[real_name] = child_value
            else:
                wrap[name] = child_value
            result.append(wrap)
            child_value["name"] = name
            child_value["desc"] = name
            child_value["tag"] = name
            if isinstance(value, str):
                child_value["value"] = value
            else:
                child_value["value"] = convert_dict(value)
    return result


class SafeSub(dict):
    """
    用于处理format_map优雅地处理某个值
    """

    def __missing__(self, key):
        return "null"  # 缺省就什么都不填写
