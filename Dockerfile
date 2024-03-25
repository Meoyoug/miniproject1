# 파이썬 버젼은 3.12
FROM python:3.12

LABEL maintainer = 'meoyong'

ENV PYTHONUNBUFFERED 1

# 앱 구성에 필요한 파일, 폴더를 도커 환경으로 복사
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
COPY ./scripts /scripts

# 워킹디렉토리 지정
WORKDIR /app
# 포트 지정?
EXPOSE 8000
# DEV 개발 환경 여부
ARG DEV=true
# 도커 빌드시 실행시킬 쉘 스크립트 코드
# 가상환경 생성
RUN python -m venv /py && \
    # 가상환경의 pip 업그레이드
    /py/bin/pip install --upgrade pip && \
    # 가상환경 내에 필요한 패키지 설치
    /py/bin/pip install -r /tmp/requirements.txt && \
    # ubuntu의 apt-get 업데이트
    apt-get update && \
    # ubuntu 환경에 postgresql, 폴더,파일 압축, 해제시 필요한 패키지들 설치
    apt-get install -y postgresql-client build-essential libpq-dev zlib1g zlib1g-dev && \
    # 개발환경일때 알림메시지, 필요한 패키지 설치
    if [ "$DEV" = "true" ] ; \
        then echo "===THIS IS DEVELOPMENT BUILD===" && \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # 필요없는 폴더와 패키지 정리
    apt-get remove -y --purge build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /tmp && \
    # 도커 유저 추가(비밀번호 입력 x, 홈디렉토리 생성 x 옵션 추가)
    adduser \
        --disabled-password \
        --no-create-home \
        fastapi-user && \
    # html, css 등을 저장할 폴더 생성(-p 옵션은 경로에대한 폴더까지 생성해줌)
    mkdir -p /vol/web/static && \
    # 생성한 유저를 폴더의 오너로 지정
    chown -R fastapi-user:fastapi-user /vol && \
    # 폴더에 대한 접근 권한부여
    # 755 : 
    chmod -R 755 /vol && \
    # 스크립트 파일을 실행시키기위해 폴더에 대한 권한 부여
    chmod -R +x /scripts

# 환경변수
ENV PATH="/scripts:/py/bin:$PATH"

# 컨테이너 이미지를 빌드할 때 생성한 fastapi-user를 사용자로 지정하고, 실행할 때 이 유저를 사용함
# USER fastapi-user

# CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
# 스크립트 폴더내의 쉘 스크립트 실행
CMD ["run.sh"]

