def del_douhao(s):
    s1 = ""
    for i in s.split(","):
        s1 += i
    return s1
def del_enter(s):
    s1 = ""
    for i in s.split("\n"):
        s1 += i
    return s1
def del_block(s):
    s = s.strip().strip("\n").strip("\t").strip().strip("\n").strip()
    s1 = ""
    for i in s.split("\t"):
        s1 += i
    return s1
# 对文档中的标点、空白、中英文、简繁体等字符进行清洗和整理
def cleaner(s):
    for i in "：:;'\"|\\*-_=+[{]}“”—、】【；‘，。/-*.！@#￥%……&*（）!@#$%^&*() ":
        s_trans = ""
        for j in s.split(i):
            s_trans+=j
        s = s_trans
    return s
