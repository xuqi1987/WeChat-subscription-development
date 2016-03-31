# -*- coding: utf-8 -*-

API_KEY = '3fd269fc978b1159373f8480211ffc81'
API_SECRET = '9SdqAcTYA273l5Nh1b71dD2RA82Fs8CQ'

# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
import time
from pprint import pformat
def print_result(hint, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(k): encode(v) for (k, v) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])


# 首先，导入SDK中的API类
from facepp import API

class Face():
    def __init__(self):
        API_KEY = '3fd269fc978b1159373f8480211ffc81'
        API_SECRET = '9SdqAcTYA273l5Nh1b71dD2RA82Fs8CQ'
        self.api = API(API_KEY, API_SECRET)
        self.persons = []
        self.faces = []
        pass

    def checkface(self,url):
        face = self.api.detection.detect(url = url)['face']

        if len(face) > 0:
            self.faces.append(face[0]['face_id'])
            return face[0]['face_id']
        return ""

    def getface(self,face_id):
        ret = self.api.info.get_face(face_id=face_id)
        print_result("face",ret)
        return ret

    def get_person_list(self):
        people = self.api.info.get_person_list()['person']
        for item in people:
                yield item['person_name']

    def add_person(self,name,url):

        # 创建face
        face = self.api.detection.detect(url = url)['face'][0]
        # 如果这个人没有了
        if name not in self.get_person_list():
            rst = self.api.person.create(
                person_name = name, face_id = face['face_id'])
        # 如果有这个人
        else:
            rst = self.api.person.add_face(
                person_name = name, face_id = face['face_id'])

    def add_person(self,name,img):

        # 创建face
        faceinfo = self.api.detection.detect(img = img)

        print_result("xuqi",faceinfo)
        #face = self.api.detection.detect(img = img)['face'][0]
        face= faceinfo['face'][0]

        # 如果这个人没有了
        if name not in self.get_person_list():
            rst = self.api.person.create(
                person_name = name, face_id = face['face_id'])
        # 如果有这个人
        else:
            rst = self.api.person.add_face(
                person_name = name, face_id = face['face_id'])


    def create_group(self,groupname):
        self.api.group.create(group_name = groupname)
        self.api.group.add_person(group_name = groupname, person_name = self.faces.iterkeys())
        pass

    def train(self,groupname):
        rst = self.api.train.identify(group_name = groupname)
        rst = self.api.wait_async(rst['session_id'])
        pass

    def recog(self,groupname,url):
        rst = self.api.recognition.identify(group_name = groupname, url = url)
        print_result('recognition result', rst)
        print '=' * 60
        print 'The person with highest confidence:', \
                rst['face'][0]['candidate'][0]['person_name']

    def del_info(self,groupname):
        self.api.group.delete(group_name = groupname)
        self.api.person.delete(person_name = self.faces.iterkeys())