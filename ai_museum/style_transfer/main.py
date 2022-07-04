import cv2
import numpy as np
from datetime import datetime  # 시간 출력을 위한 import

'''
content 이미지를 정의된 모델의 스타일 입혀주는 방법!!
이미지의 경로를 바꾸거나 모델을 선택할 수 있도록 사용자에게 선택할 수 있도록 만드는 방법을 모색해볼 것
'''
# def style_transfer(number):
def style_transfer():
    # 커피머신 준비하기
    # 모델 불러오기 후 변수 정의 : cv2.dnn.readNetFromTorch('./위치/파일이름.t7')
    net = cv2.dnn.readNetFromTorch('style_transfer/models/the_scream.t7')  # modesls 의 리스트 정의 필요
    # net = cv2.dnn.readNetFromTorch(number)

    # 원두 넣을 준비하기
    # 이미지 불러오기 후 변수 정의 : cv2.imread('./경로/파일이름.jpg')
    img = cv2.imread('static/images/img_02.jpg')

    # h[높이], w[너비], c[채널] = img.shape : 이미지의 형태 
    h, w, c = img.shape

    # 사이즈 재조정 : cv2.resize(src: Mat, dsize: Tuple[int, int], dts: Mat = ..., fx: int = ..., fy: int = ..., interpolation: int = ...)
    '''
    h : w = new_h : 500
    w * new_h = h * 500
    new_h = h / w * 500
        = dsize=(500, int(h / w * 500)
        소수점 방지 int
    '''
    img = cv2.resize(img, dsize=(500, int(h / w * 500)))
    print(img.shape) # 사이즈 조정 완료 : (325, 500, 3)

    MEAN_VALUE = [103.939, 116.779, 123.680]
    '''
    전처리 과정(Preprocessing) : cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
    모델의 성능을 높이기 위한 전처리 과정
    img 의 MEAN_VALUE 값을 빼주는 기능
    차원변형
    '''
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
    print(blob.shape) # 차원 조정 완료(컴퓨터가 인식할 수 있도록 처리) : (1, 3, 325, 500)


    # 전처리한 결과를 input 으로 지정
    net.setInput(blob)
    # 추론이 끝난 값을 output 으로 지정 : 아직 컴퓨터의 언어로 되어있어 확인할 수 없음
    output = net.forward()


    # 후처리 과정
    '''
    차원을 줄여줌 : .squeeze(), 차원을 거꾸로 변형 : transpose()
    두 과정이 끝나면 사람이 보기 쉬운 이미지가 됨
    전처리 과정에서 뺀 MEAN_VALUE 값을 다시 도로 넣어줌
    '''
    output = output.squeeze().transpose((1, 2, 0))
    output = output + MEAN_VALUE

    '''
    MEAN_VALUE 가 더해질 경우 이미지의 규격이 255 를 초과하는 경우가 생김
    초과 방지하기 위해 numpy의 .clip(output, 0, 255) 함수로 255로 허용 제한을 둠
    '''
    output = np.clip(output, 0, 255)
    # 사람이 보기 좋은 형태(정수 형태)로 바꿔주기 위해 .astype('uint8') 함수를 사용
    output = output.astype('uint8')
    
    cv2.imwrite(f'style_transfer/output/{datetime.now().strftime("%Y%m%d-%H%M%S")}.jpg', output)


    # # 후처리가 된 이미지 확인 : .imshow('output', output)
    # cv2.imshow('output', output)
    # # image show : cv2.imshow(winname: Any, mat: Any)
    # cv2.imshow('img', img)
    # # action delay : cv2.waitKey: (delay: ... = ...)
    # cv2.waitKey(0)