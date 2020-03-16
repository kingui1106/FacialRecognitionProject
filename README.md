# FacialRecognitionProject
基于opencv人脸识别项目，接入微信公众号

https://github.com/kingui1106/FacialRecognitionProject/tree/master

①运行主程序
运行ngrok内网穿透:./ngrok.sh
运行监控和微信：./start.sh
运行人脸识别：./face.sh

②添加新的人脸进行下列操作origin文件夹：
录入新的人脸：Python face_data.py
训练人脸数据：Python face_training.py
训练完后，把FacialRecognitionProject/trainer文件夹复制到 we/trainer，运行主程序。
测试识别人脸：Python face_recognition.py


微信端：
1.户主在公众号菜单列表选择开启门功能，公众号会返回秘钥要求，输入正确的秘钥（初始密码为123），门打开，再次在菜单界面选择关门功能，门将会关闭。
2.户主可以在公众号菜单列表选择实时监控功能，通过公众号返回的网站，点击进入可以获得当前的监控内容。
3.访客关注门禁系统的微信公众号，然后在菜单界面选择访客功能，在户主端会收到访客的请求信息，这时候户主可以选择拍照功能，来获取当前访客的照片，确认后，可以在公众号菜单列表选择开门功能。


人脸识别端：
1.首先在摄像头下进行户主拍照，存入本地服务器，作为到时候识别的参照照片。
2.户主在进门的时候，脸正对摄像头，程序自动进行识别，识别成功后，门自动打开，播放器根据不同的户主播放不同的欢迎音效，大约十秒后，门自动关闭。
