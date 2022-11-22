def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    return u'\u4e00' <= uchar <= u'\u9fa5'


def is_number(uchar):
    """判断一个unicode是否是数字"""
    return u'\u0030' <= uchar <= u'\u0039'


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    return (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a')


def is_valid_name(name, num):
    if len(name) > num:
        raise Exception(f"长度不能超过 {num} 个字符")
    for i in name:
        if not is_chinese(i) and not is_number(i) and not is_alphabet(i):
            raise Exception(f"名称 {name} 不合法")
    return name
