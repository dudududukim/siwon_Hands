# 취약계층을 위한 스마트 공유 냉장고 시스템

취약계층을 위한 스마트 공유 냉장고 시스템은 음식 낭비를 줄이고 취약계층에게 도움을 제공하는 사회적 목적을 가진 프로젝트입니다. RFID를 이용한 잠금장치와 실시간 이미지 분석을 통한 음식 재고 관리를 특징으로 합니다.

## 기능

- **RFID 접근 제어**: 취약계층만이 접근 가능
- **자동 재고 관리**: 내부 카메라와 이미지 분석을 통한 실시간 재고 확인
- **음식물 투입 및 분배 자동화**: 3축 이동장치를 통한 자동화된 음식물 처리

## 설치 방법

이 시스템을 구축하기 위해서는 다음과 같은 하드웨어가 필요합니다.

- Arduino
- RFID 리더기
- ESP32-CAM
- 솔레노이드 잠금장치
- stepping motor

## 하드웨어 및 FLOWCHART
![image](https://github.com/user-attachments/assets/96653b6a-1231-47ce-984f-a5d599319720)

![image](https://github.com/user-attachments/assets/ece3a685-a2ab-455b-b9b5-494ecffe55b6)

## 솔루션
<img width="1124" alt="image" src="https://github.com/user-attachments/assets/e9273962-866b-440a-a81b-ff30ccdd7aee">
<img width="1115" alt="image" src="https://github.com/user-attachments/assets/b5a6e8b9-c309-4035-b197-16d154208c24">


소프트웨어와 라이브러리 설치는 아래의 단계를 따르십시오.

1. 레포지토리를 클론합니다.
   ```bash
   git clone https://github.com/your-github-username/your-repository-name

2. 필요한 라이브러리를 설치합니다.
   ```bash
   pip install -r requirements.txt


## 사용법

시스템을 시작하기 위해 아두이노와 연결된 모든 장치를 초기화하고, 아래의 명령을 실행합니다.

```bash
python main.py



## 시연영상
https://youtu.be/0dWZBx3Ez50?si=kfydq7GPBWIDgueA
