# SKN33-1ST-3TEAM

## 🔎 프로젝트명
### 자동차 리콜 통합 조회 시스템

## 팀 소개
### 팀명: 3조
<table>
<tr>
    <th>김정재</th>
    <th>신진호</th>
    <th>이준희</th>
    <th>유하연</th>
</tr>

<tr>
    <td align="center">
        <img src="data/images/1.png" width="150">
    </td>
    <td align="center">
        <img src="data/images/2.png" width="150">
    </td>
    <td align="center">
        <img src="data/images/3.png" width="150">
    </td>
    <td align="center">
        <img src="data/images/4.png" width="150">
    </td>
</tr>

<tr>
    <td align="center">
        <a href="https://github.com/kimjeongjaeae">GitHub</a>
    </td>
    <td align="center">
        <a href="https://github.com/Gitcatho">GitHub</a>
    </td>
    <td align="center">
        <a href="https://github.com/Isnthee">GitHub</a>
    </td>
    <td align="center">
        <a href="https://github.com/lululu9988">GitHub</a>
    </td>
</tr>

</table>

- 신진호: 팀장, git 관리, 웹 크롤링, DB 설계
- 김정재: DB 설계, Streamlit, 데이터 가공, 시각화
- 이준희: 웹 크롤링, git관리
- 유하연: DB 설계, Streamlit

## 프로젝트 소개

1. 차량별 리콜 이력 조회
2. 리콜 통계 및 시각화 분석
3. 지역/제조사별 서비스센터 검색
4. 리콜 관련 뉴스 검색
5. 리콜 FAQ 조회

## 💻 기술스택
<img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/mysql-4479A1?style=flat-square&logo=mysql&logoColor=white"/>
<img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/git-F03C2E?style=flat-square&logo=git&logoColor=white"/>
<img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/folium-77B829?style=flat-square&logo=folium&logoColor=white"/>
<img src="https://img.shields.io/badge/markdown-000000?style=flat-square&logo=markdown&logoColor=white"/>


## 프로젝트 필요성(배경)

자동차 리콜은 차량 안전과 직결되는 중요한 정보이지만, 
일반 사용자가 자신의 차량에 대한 리콜 여부를 확인하기 위해서는 
여러 사이트를 방문하거나 복잡한 검색 과정을 거쳐야 합니다.

또한 리콜 관련 정보는 제조사, 정부기관, 뉴스 기사 등 
다양한 곳에 분산되어 있어 필요한 정보를 한 번에 
확인하기 어렵다는 문제가 있습니다.

본 프로젝트는 공공데이터와 웹 크롤링 기술을 활용하여 
리콜 정보를 통합 제공하고, 사용자 중심의 조회 기능과 
시각화 서비스를 제공함으로써 자동차 안전 정보의 접근성과 
활용성을 높이고자 기획되었습니다.

## 프로젝트 목표
자동차 리콜 정보가 여러 공공데이터, 뉴스, 서비스센터 정보로 흩어져 있어 사용자가 한번에 확인하기 어렵다는 문제를 해결하는게 주 목표입니다.
이 프로젝트를 통해 차량 리콜 데이터를 수집, 정제하여 DB화 하고 웹 서비스로 제공하여 사용자가 자신의 차량 리콜 여부와 관련 정보를 쉽고 빠르게 확인할 수 있도록 합니다.

## 데이터 수집 방법

- 공공데이터 포털에서 리콜 자동차 정보 csv파일로 수집
- 웹페이지 크롤링으로 FAQ 데이터 수집
- Naver News API 이용해 차량별 리콜 뉴스데이터 수집

## DB 설계(논리/물리 ERD)
<img src="data/images/ERD_1차프로젝트_논리.png">
논리
<img src="data/images/ERD_1차프로젝트_물리.png">
물리

## 주요기능

### 1. 메인 대시보드
- 각 서비스로 바로 이동
### 2. 내 차 리콜 조회
- 제조사, 차종 선택시 리콜 대상, 이력 조회
- 선택 차종 관련 리콜 뉴스 조회
### 3. 리콜 데이터 분석
- 연도 범위내 데이터 분석
- 제조사별 리콜 건수
- 연도별 리콜 추이
- 결함 유형별 리콜 건수
- 연도별 결함 유형 추이
- 브랜드별 결함 유형 현황
- 제조사별 차종 리콜 현황
### 4. 가까운 서비스센터 찾기
- 지역별 서비스센터 찾기
- 제조사별 필터링 가능
### 6. 리콜 뉴스 검색
- 리콜 관련 키워드 검색
- 차종별 리콜 관련 뉴스 검색
### 7. 자동차 리콜 FAQ
- FAQ 검색 기능 지원
- 키워드 강조 기능 제공
## 실행방법

## 수행 화면 캡처

## 📝회고 

| 이름 | 회고                                                                                                                                                                                                                    |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 김정재 |                                                                                                                                                                                                                       |
| 신진호 | 교육장에서 진행한 첫 프로젝트였습니다. 큰 문제 없이 마무리할 수 있어 만족스러웠고, 각자 배우고 싶었던 분야를 맡아 진행하며 모두가 성장할 수 있는 프로젝트였던 것 같습니다.                                                                                                                 |
| 이준희 | 유능한 팀원분들과 클로드 덕분에 1st 프로젝트를 무사히 완료할 수 있었던 것 같습니다. 팀원 분들의 발목을 잡지 않기 위해 아둥바둥 한 것 치곤 1인분도 해내지 못한 것 같은 아쉬움이 남아 자신을 반성하게 되었습니다. git과 github를 통한 첫 협업 경험은 재직 중에도 경험하지 못한 값진 경험인 동시에, 앞으로 다가올 수 많은 충돌에 대한 경각심 또한 심어준 것 같습니다. |
| 유하연 | github 작업에서 문제가 생기지 않도록, git사용법에 대해 더 숙지하는 것이 좋겠다고 생각했습니다.                                                                                                                                                            |