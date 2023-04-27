import streamlit as st
from glob import glob
import oss2
import time
import urllib.request


def point():
    st.set_page_config(page_title='相片评分校准')
    st.header('相片评分校准')
    images = glob('images/*.jpg')
    count = 0
    date = time.strftime("%Y%m%d", time.localtime())  # 获得今天的年月日
    # 创建表单
    with st.form("my_form"):
        page = st.sidebar.number_input('序号', count, len(images), value=0)
        image = images[page]
        st.write(image.split('\\')[-1].split('.')[0])
        st.image('https://dataface.oss-cn-beijing.aliyuncs.com/image1_white/' + image.split('\\')[-1])
        W = int(image.split('/')[-1].split('-')[1][1:])
        C = int(image.split('/')[-1].split('-')[2][1:])
        L = int(image.split('/')[-1].split('-')[3][1:])
        G = int(image.split('/')[-1].split('-')[4][1:3])

        # 侧边栏
        with st.sidebar:
            wn = st.sidebar.radio('内向外向:', ('W指数', 'N指数'), index=0 if W > 50 else 1)
            if wn == 'W指数':
                w = st.sidebar.number_input(wn, 0, 100, value=W)
            else:
                w = st.sidebar.number_input(wn, 0, 100, value=100 - W)
            gr = st.sidebar.radio('刚性柔性:', ('G指数', 'R指数'), index=0 if G > 50 else 1)
            if gr == 'G指数':
                g = st.sidebar.number_input(gr, 0, 100, value=G)
            else:
                g = st.sidebar.number_input(gr, 0, 100, value=100 - G)

            cj = st.sidebar.radio('抽象具象:', ('C指数', 'J指数'), index=0 if C > 50 else 1)
            if cj == 'C指数':
                c = st.sidebar.number_input(cj, 0, 100, value=C)
            else:
                c = st.sidebar.number_input(cj, 0, 100, value=100 - C)
            lq = st.sidebar.radio('感性理性:', ('L指数', 'Q指数'), index=0 if L > 50 else 1)
            if lq == 'L指数':
                l = st.sidebar.number_input(lq, 0, 100, value=L)
            else:
                l = st.sidebar.number_input(lq, 0, 100, value=100 - L)
            submit = st.form_submit_button('提交更改')
        if submit:
            w = w if wn == 'W指数' else 100 - w
            c = c if cj == 'C指数' else 100 - c
            l = l if lq == 'L指数' else 100 - l
            g = g if gr == 'G指数' else 100 - g
            # 将评分放入fix中
            try:
                fix = urllib.request.urlopen('https://dataface.oss-cn-beijing.aliyuncs.com/test/output-' + date + '.txt').read()
                fix = fix.decode('utf-8')
            except:
                fix = ''
            fix += '\n' + str({'name': image.split('/')[-1].split('\\')[-1], 'W': w, 'C': c, 'L': l, 'G': g})
            st.write(fix)
            # 上传文件
            # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
            auth = oss2.Auth('LTAI5tKD3Cb6DmRX7CYLbDXk', 'gxqnUmmmbTlvGncIsYWin1LO3rUoM2')
            # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
            # 填写Bucket名称。
            bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'dataface')

            # 上传文件。
            # 如果需要在上传文件时设置文件存储类型（x-oss-storage-class）和访问权限（x-oss-object-acl），请在put_object中设置相关Header。
            # headers = dict()
            # headers["x-oss-storage-class"] = "Standard"
            # headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE
            # 填写Object完整路径和字符串。Object完整路径中不能包含Bucket名称。
            # result = bucket.put_object('exampleobject.txt', 'Hello OSS', headers=headers)
            result = bucket.put_object('test/output-' + date + '.txt', fix)

            # HTTP返回码。
            st.write('http status: {0}'.format(result.status))
            # 请求ID。请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
            st.write('request_id: {0}'.format(result.request_id))
            # ETag是put_object方法返回值特有的属性，用于标识一个Object的内容。
            st.write('ETag: {0}'.format(result.etag))
            # HTTP响应头部。
            st.write('date: {0}'.format(result.headers['date']))


if __name__ == '__main__':
    point()
