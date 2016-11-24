# -*- coding: utf-8 -*-
import jpype

import os

jvm_path = jpype.getDefaultJVMPath()
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
jar_path = basedir + '/app/datasource/spiderJar.jar'
jvmArg = "-Djava.class.path=" + jar_path

# jvmArg1 = "-classpath {}".format(basedir)
# jpype.startJVM(jvm_path, "-ea")

try:
    # if jpype.isJVMStarted():
    #     jpype.shutdownJVM()
    jpype.startJVM(jvm_path, '-ea', jvmArg)
except InterruptedError as e:
    print(e)

PY = jpype.JPackage('cardpay').pengyuan.Base64
py = PY()

TA = jpype.JClass('upa.client.UPAClient')
upa = TA()
z_result = upa.setDevelopmentId("FCA0WKKJOBUEJUFAI0BVRKQBJNEPJEJQ")
print(z_result)
