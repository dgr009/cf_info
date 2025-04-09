# Cloudflare DNS Info 조회 스크립트

이 Python 스크립트는 Cloudflare 계정의 DNS 정보를 보기 쉽게 조회하여 Rich Table 형태로 정리하여 보여줍니다.

---

## 🚀 주요 기능

- CloudFlare API를 이용한 DNS record 목록 조회
- .env 셋팅으로 필요한 어카운트 및 도메인호스트 필터링

---

## 🛠️ 필요 환경

- Python 3.8 이상
- Cloudflare 계정 및 API 키

---

## 📌 사전 준비 및 설정

### 1️⃣ Python 패키지 설치

아래 명령어를 통해 필요한 Python 패키지를 설치합니다.

```bash
pip install python-dotenv requests rich
```

### 2️⃣ 환경 변수 설정 (`.env` 파일)

스크립트와 동일한 디렉터리에 `.env` 파일을 만들고 아래의 환경 변수를 설정합니다.

```env
CLOUDFLARE_EMAIL=your-email@example.com
CLOUDFLARE_API_TOKEN=your-api-token

# (선택적) 특정 account, zone만 검색할 경우
ACCOUNTS=account1,account2
ZONES=example.com,example.org
```

### 🔑 API 토큰 생성법

Cloudflare 대시보드에서 [My Profile > API Tokens](https://dash.cloudflare.com/profile/api-tokens) 메뉴에서 생성할 수 있습니다.

권장하는 최소 권한:
- Account: `Account Settings - Read`
- Zone: `DNS - Read`

---

## ⚙️ 사용 방법

스크립트 기본 실행법 (Default - 전체조회):

```bash
python cf_info.py
```

특정 계정이나 도메인(zone)을 필터링하여 조회:

```bash
python cf_info.py --account <계정명 일부> --zone <도메인 일부>
```

예시:

```bash
python cf_info.py --account exam --zone ple
```

위 명령은 계정명에 "exam"가 포함되고, 도메인명에 "ple"가 포함된 모든 계정과 도메인의 DNS 정보를 출력합니다.

환경 변수에 설정된 계정과 도메인이 있을 경우 해당 설정이 우선 적용됩니다.

환경 변수에 설정된 내용이 없고 option 필터링이 없을경우 기본 전체 검색이 적용됩니다.

필터링 우선순위 : Argment > ENV > Default(all)

---

## 🗂️ 로그 파일

로그는 아래 경로에 기록됩니다.

```
logs/cloudflare_dns_info.log
```

---

## 📖 테이블 출력 예시

Rich Table을 활용한 명확한 테이블로 표시됩니다.

| Type | Name | Contents | Priority | Proxy | TTL | Created | Modified | Message |
|------|------|----------|----------|-------|-----|---------|----------|---------|
| A    | test | 192.0.2.1 | -        | True  | 3600 | 2024-05-10 15:30 | 2024-05-12 14:22 | example comment |

---

## ⚠️ 주의사항

- 과도한 API 호출은 Cloudflare API 호출 제한에 도달할 수 있으니 유의하세요.
- 보안상 API 키는 절대 외부에 노출하지 마세요.

---

## 📞 지원 및 문의

스크립트 사용 중 문제가 발생하거나 추가 기능 요청이 있으면 개발자에게 문의하세요.

---

## 📄 라이센스

이 스크립트는 MIT 라이센스로 제공됩니다. 자유롭게 수정 및 배포할 수 있습니다.

