# 프로필 수정 안내

## 사진 바꾸기

1. 사진을 **PNG 형식**으로 준비합니다. 세로 3:4 비율을 권장합니다.
2. 이 저장소의 [`assets`](assets) 폴더에서 **Add file → Upload files**를 선택합니다.
3. 파일 이름을 **`portrait.png`**로 맞춰 업로드하고 `main` 브랜치에 커밋합니다. 기존 파일을 교체하면 됩니다.
4. **Actions → Update profile banner**가 완료되면 프로필 배너에 사진이 반영됩니다.

사진은 프레임 중앙을 기준으로 잘립니다. 얼굴 주변에 여백이 있는 사진을 사용하면 좋습니다.
프로필 README에 들어가는 사진이며, GitHub 계정의 원형 아바타는 GitHub 설정에서 별도로 바꿀 수 있습니다.

## 소개와 연구 내용

[`README.md`](README.md)를 수정하면 됩니다. 본문은 GitHub 기본 Markdown을 사용합니다.

## 이름과 수상 내역

[`profile.json`](profile.json)을 수정하면 배너가 자동으로 다시 만들어집니다.
수상 내역은 두 항목을 기준으로 배치되어 있습니다. 파일 안의 `awards` 배열에서 이름과 설명을 바꿀 수 있습니다.

배너는 라이트·다크 모드와 모바일 화면용으로 각각 생성됩니다. `assets/header-*.svg` 파일은 자동 생성 결과이므로 직접 편집하지 않습니다.

## CV 바꾸기

[`assets/Chihyun-Ahn-CV.pdf`](assets/Chihyun-Ahn-CV.pdf)를 새 PDF로 교체하면 됩니다. 프로필의 **CV (PDF)** 링크는 같은 파일 이름을 유지하는 동안 자동으로 새 파일을 가리킵니다.

## 로컬에서 배너 만들기

Python 3.10 이상이 필요하며 추가 패키지는 필요하지 않습니다.

```sh
python scripts/render_profile.py
```

사진과 수상 배너는 독립된 SVG 이미지로 제공되고, 연구 내용과 외부 링크는 검색·복사가 가능한 본문 텍스트로 유지됩니다.
