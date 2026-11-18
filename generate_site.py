import os
from urllib.parse import quote

# 1. 서울 25개 구 및 동 데이터
seoul_data = {
    'jongno': {'name': '종로구', 'dongs': ['청운동', '효자동', '사직동', '삼청동', '부암동', '평창동', '무악동', '교남동', '가회동', '종로1.2.3.4가동', '종로5.6가동', '이화동', '혜화동', '창신1동', '창신2동', '창신3동', '숭인1동', '숭인2동']},
    'jung': {'name': '중구', 'dongs': ['소공동', '회현동', '명동', '필동', '장충동', '광희동', '을지로동', '신당동', '다산동', '약수동', '청구동', '동화동', '황학동', '중림동']},
    'yongsan': {'name': '용산구', 'dongs': ['후암동', '용산2가동', '남영동', '청파동', '원효로1동', '원효로2동', '효창동', '용문동', '이촌1동', '이촌2동', '이태원1동', '이태원2동', '한남동', '서빙고동', '보광동']},
    'seongdong': {'name': '성동구', 'dongs': ['왕십리2동', '왕십리도선동', '마장동', '사근동', '행당1동', '행당2동', '응봉동', '금호1가동', '금호2.3가동', '금호4가동', '옥수동', '성수1가1동', '성수1가2동', '성수2가1동', '성수2가3동', '송정동', '용답동']},
    'gwangjin': {'name': '광진구', 'dongs': ['중곡1동', '중곡2동', '중곡3동', '중곡4동', '능동', '구의1동', '구의2동', '구의3동', '광장동', '자양1동', '자양2동', '자양3동', '자양4동', '화양동', '군자동']},
    'dongdaemun': {'name': '동대문구', 'dongs': ['신설동', '용두동', '제기동', '전농1동', '전농2동', '답십리1동', '답십리2동', '장안1동', '장안2동', '청량리동', '회기동', '휘경1동', '휘경2동', '이문1동', '이문2동']},
    'jungnang': {'name': '중랑구', 'dongs': ['면목본동', '면목2동', '면목3.4동', '면목5동', '면목7동', '상봉1동', '상봉2동', '중화1동', '중화2동', '묵1동', '묵2동', '망우본동', '망우3동', '신내1동', '신내2동']},
    'seongbuk': {'name': '성북구', 'dongs': ['성북동', '삼선동', '동선동', '돈암1동', '돈암2동', '안암동', '보문동', '정릉1동', '정릉2동', '정릉3동', '정릉4동', '길음1동', '길음2동', '종암동', '월곡1동', '월곡2동', '장위1동', '장위2동', '장위3동', '석관동']},
    'gangbuk': {'name': '강북구', 'dongs': ['삼양동', '미아동', '송중동', '송천동', '삼각산동', '번1동', '번2동', '번3동', '수유1동', '수유2동', '수유3동', '우이동', '인수동']},
    'dobong': {'name': '도봉구', 'dongs': ['창1동', '창2동', '창3동', '창4동', '창5동', '도봉1동', '도봉2동', '쌍문1동', '쌍문2동', '쌍문3동', '쌍문4동', '방학1동', '방학2동', '방학3동']},
    'nowon': {'name': '노원구', 'dongs': ['상계1동', '상계2동', '상계3.4동', '상계5동', '상계6.7동', '상계8동', '상계9동', '상계10동', '중계본동', '중계1동', '중계2.3동', '중계4동', '하계1동', '하계2동', '공릉1동', '공릉2동']},
    'eunpyeong': {'name': '은평구', 'dongs': ['불광1동', '불광2동', '갈현1동', '갈현2동', '구산동', '대조동', '응암1동', '응암2동', '응암3동', '역촌동', '신사1동', '신사2동', '증산동', '수색동', '진관동']},
    'seodaemun': {'name': '서대문구', 'dongs': ['천연동', '북아현동', '충현동', '신촌동', '연희동', '홍제1동', '홍제2동', '홍제3동', '홍은1동', '홍은2동', '남가좌1동', '남가좌2동', '북가좌1동', '북가좌2동']},
    'mapo': {'name': '마포구', 'dongs': ['공덕동', '아현동', '도화동', '용강동', '대흥동', '염리동', '신수동', '서교동', '합정동', '망원1동', '망원2동', '연남동', '성산1동', '성산2동', '상암동']},
    'yangcheon': {'name': '양천구', 'dongs': ['목1동', '목2동', '목3동', '목4동', '목5동', '신월1동', '신월2동', '신월3동', '신월4동', '신월5동', '신월6동', '신월7동', '신정1동', '신정2동', '신정3동', '신정4동', '신정6동', '신정7동']},
    'gangseo': {'name': '강서구', 'dongs': ['등촌1동', '등촌2동', '등촌3동', '화곡본동', '화곡1동', '화곡2동', '화곡3동', '화곡4동', '화곡8동', '우장산동', '가양1동', '가양2동', '가양3동', '발산1동', '공항동', '방화1동', '방화2동', '방화3동']},
    'guro': {'name': '구로구', 'dongs': ['신도림동', '구로1동', '구로2동', '구로3동', '구로4동', '구로5동', '가리봉동', '고척1동', '고척2동', '개봉1동', '개봉2동', '개봉3동', '오류1동', '오류2동', '수궁동']},
    'geumcheon': {'name': '금천구', 'dongs': ['가산동', '독산1동', '독산2동', '독산3동', '독산4동', '시흥1동', '시흥2동', '시흥3동', '시흥4동', '시흥5동']},
    'yeongdeungpo': {'name': '영등포구', 'dongs': ['영등포본동', '영등포동', '여의동', '당산1동', '당산2동', '도림동', '문래동', '양평1동', '양평2동', '신길1동', '신길3동', '신길4동', '신길5동', '신길6동', '신길7동', '대림1동', '대림2동', '대림3동']},
    'dongjak': {'name': '동작구', 'dongs': ['노량진1동', '노량진2동', '상도1동', '상도2동', '상도3동', '상도4동', '흑석동', '사당1동', '사당2동', '사당3동', '사당4동', '사당5동', '대방동', '신대방1동', '신대방2동']},
    'gwanak': {'name': '관악구', 'dongs': ['보라매동', '청림동', '성현동', '행운동', '낙성대동', '청룡동', '은천동', '상현동', '서원동', '신원동', '서림동', '신사동', '난향동', '조원동', '대학동', '난곡동', '삼성동', '미성동']},
    'seocho': {'name': '서초구', 'dongs': ['서초1동', '서초2동', '서초3동', '서초4동', '잠원동', '반포본동', '반포1동', '반포2동', '반포3동', '반포4동', '방배본동', '방배1동', '방배2동', '방배3동', '방배4동', '양재1동', '양재2동', '내곡동']},
    'gangnam': {'name': '강남구', 'dongs': ['역삼1동', '역삼2동', '개포1동', '개포2동', '개포4동', '청담동', '삼성1동', '삼성2동', '대치1동', '대치2동', '대치4동', '신사동', '논현1동', '논현2동', '압구정동', '세곡동', '자곡동', '일원동', '수서동', '도곡1동', '도곡2동']},
    'songpa': {'name': '송파구', 'dongs': ['잠실본동', '잠실2동', '잠실3동', '잠실4동', '잠실6동', '잠실7동', '풍납1동', '풍납2동', '거여1동', '거여2동', '마천1동', '마천2동', '방이1동', '방이2동', '오륜동', '오금동', '송파1동', '송파2동', '석촌동', '삼전동', '가락본동', '가락1동', '가락2동', '문정1동', '문정2동', '장지동', '위례동', '잠실동']},
    'gangdong': {'name': '강동구', 'dongs': ['강일동', '상일1동', '상일2동', '명일1동', '명일2동', '고덕1동', '고덕2동', '암사1동', '암사2동', '암사3동', '천호1동', '천호2동', '천호3동', '성내1동', '성내2동', '성내3동', '둔촌1동', '둔촌2동']}
}

base_url = "https://sudo-therapy.netlify.app"
base_dir = "output"
os.makedirs(base_dir, exist_ok=True)

# 2. 전체 지역 목록(chips) 생성 (메인 및 모든 지역 페이지에 동일하게 들어갈 링크 블록)
all_regions = []
for gu_key, gu_info in seoul_data.items():
    all_regions.append(gu_info['name'])
    all_regions.extend(gu_info['dongs'])

chips_html = ""
for region in all_regions:
    # URL 인코딩을 통해 안전한 주소 생성
    chips_html += f'<a href="{base_url}/{quote(region)}/">{region}</a>\n'

# 3. 공통 CSS 및 헤더/푸터 설정 (유지보수를 위해 변수로 분리)
COMMON_CSS = """
:root{--mint:#48c8c0;--mint-d:#2aa9a1;--mint-l:#f3fbfa;--ink:#202020;--sub:#7d8387;--soft:#a0a4a4;--line:#e6e8ea;--gray:#f9f9f9;--fill:#f1f2f3}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;overflow-x:hidden}
body{background:#fff;color:var(--ink);font-family:"Pretendard Variable",Pretendard,system-ui,sans-serif;font-size:15.5px;line-height:1.75;word-break:keep-all;-webkit-font-smoothing:antialiased;}
a{color:inherit;text-decoration:none}
.wrap{width:min(90vw,640px);margin-inline:auto}
.serif{font-family:"Noto Serif KR",serif}
header.bar{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header.bar .wrap{display:flex;align-items:center;justify-content:space-between;height:58px}
.logo{font-weight:800;font-size:17px;display:flex;align-items:center;gap:8px}
.logo b{width:9px;height:9px;border-radius:50%;background:var(--mint)}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:0 20px;border-radius:999px;font-weight:700;font-size:14.5px;background:var(--mint);color:#fff;box-shadow:0 10px 22px -12px rgba(72,200,192,.9);transition:transform .15s}
.pill.lg{min-height:54px;padding:0 30px;font-size:16.5px}
.hero{text-align:center;padding:56px 0 30px}
.hero h1{font-size:clamp(27px,7.4vw,40px);line-height:1.3;font-weight:500;letter-spacing:-.03em}
.hero .lead{margin:16px auto 0;color:var(--sub);font-size:15px}
.hero .cta{display:flex;gap:10px;justify-content:center;margin-top:26px}
.sec{padding:50px 0 72px;text-align:center}
.sec.gray{background:var(--gray)}
h2{font-size:clamp(22px,6vw,30px);line-height:1.35;font-weight:500;letter-spacing:-.03em}
h2 em{font-style:normal;color:var(--mint-d)}
.sub{color:var(--sub);font-size:14.5px;margin-top:10px}
.companies-grid { display:grid; gap:12px; margin:26px auto 0; max-width:560px; text-align:left; grid-template-columns:1fr 1fr; }
.companies-grid a { background:#fff; border:1px solid var(--line); border-radius:14px; padding:20px 18px; display:block; transition:border-color .15s; }
.companies-grid a:hover, .companies-grid a:active { border-color:var(--mint); box-shadow:0 10px 22px -12px rgba(72,200,192,.4); }
.companies-grid h3 { font-size:16px; color:var(--ink); margin-bottom:4px; font-weight:800; }
.companies-grid p { font-size:15px; color:var(--mint-d); font-weight:700; }
/* 지역 칩 스타일 추가 */
.chips{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:26px auto 0;max-width:560px}
.chips a{display:flex;align-items:center;justify-content:center;min-height:44px;background:#fff;border:1px solid var(--line);border-radius:999px;font-size:13.5px;font-weight:600;padding:4px 6px;transition:background .15s}
.chips a:active{background:var(--mint);color:#fff;border-color:var(--mint)}
footer{background:#2b2f33;color:#fff;padding:40px 0 48px;text-align:center}
.fab{position:fixed;right:16px;bottom:18px;z-index:30;width:66px;height:66px;border-radius:50%;background:var(--mint);color:#fff;display:grid;place-items:center;text-align:center;font-size:12px;font-weight:800;line-height:1.2}
@media(max-width:480px) { .companies-grid { grid-template-columns:1fr; } }
@media(min-width:720px){.hero{padding-top:84px}.chips{grid-template-columns:repeat(5,1fr)}}
"""

# 4. 메인 페이지 생성 로직 (출장마사지 키워드 제외)
main_template = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>수도테라피 | 프리미엄 스웨디시 홈테라피</title>
<meta name="description" content="수도테라피에서 검증된 프리미엄 홈테라피 업체를 만나보세요. 끝나고 캐모마일 차 한 잔이면 밤이 짧아지는 날에도 갑니다.">
<link rel="canonical" href="{base_url}/">
<link rel="icon" href="/favicon.ico">
<meta property="og:type" content="website">
<meta property="og:title" content="수도테라피 | 프리미엄 스웨디시 홈테라피">
<meta property="og:description" content="수도테라피에서 검증된 프리미엄 홈테라피 업체를 만나보세요. 끝나고 캐모마일 차 한 잔이면 밤이 짧아지는 날에도 갑니다.">
<meta property="og:url" content="{base_url}/">
<meta property="og:image" content="{base_url}/img/og-root.jpg">

<script>
  document.addEventListener("DOMContentLoaded", function() {{
    const canonicalUrl = document.querySelector('link[rel="canonical"]')?.href || window.location.href;
    const jsonLd = {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "url": canonicalUrl,
      "name": document.title,
      "description": document.querySelector('meta[name="description"]')?.content || "",
      "itemListElement": [
        {{"@type": "LocalBusiness", "position": 1, "name": "퀸즈홈테라피", "telephone": "0507-1280-3296"}},
        {{"@type": "LocalBusiness", "position": 2, "name": "한국미인테라피", "telephone": "0507-1280-3140"}},
        {{"@type": "LocalBusiness", "position": 3, "name": "오늘밤테라피", "telephone": "0507-1280-3199"}},
        {{"@type": "LocalBusiness", "position": 4, "name": "주주테라피", "telephone": "0507-1280-3197"}},
        {{"@type": "LocalBusiness", "position": 5, "name": "기쁨테라피", "telephone": "0507-1280-3183"}},
        {{"@type": "LocalBusiness", "position": 6, "name": "미인클럽테라피", "telephone": "0507-1280-3180"}}
      ]
    }};
    const script = document.createElement('script');
    script.type = "application/ld+json";
    script.text = JSON.stringify(jsonLd);
    document.head.appendChild(script);
  }});
</script>

<style>
{COMMON_CSS}
</style>
</head>
<body class="root">
<header class="bar"><div class="wrap"><a class="logo" href="{base_url}/"><b></b>수도테라피</a><a class="pill" href="#companies">제휴 업체</a></div></header>

<section class="hero">
<div class="wrap">
<h1 class="serif">프리미엄 테라피<br>스웨디시 홈테라피</h1>
<p class="lead">씻을 기운조차 없는 날이 있죠. 편안함을 안고 갑니다.</p>
<div class="cta"><a class="pill lg" href="#companies">업체 바로보기</a></div>
</div>
</section>

<section id="companies" class="sec gray"><div class="wrap"><h2 class="serif"><em>수도테라피</em> 제휴 업체</h2><p class="sub">원하시는 업체를 누르시면 바로 연결됩니다.</p>
<div class="companies-grid">
  <a href="tel:0507-1280-3296"><h3>퀸즈홈테라피</h3><p>0507-1280-3296</p></a>
  <a href="tel:0507-1280-3140"><h3>한국미인테라피</h3><p>0507-1280-3140</p></a>
  <a href="tel:0507-1280-3199"><h3>오늘밤테라피</h3><p>0507-1280-3199</p></a>
  <a href="tel:0507-1280-3197"><h3>주주테라피</h3><p>0507-1280-3197</p></a>
  <a href="tel:0507-1280-3183"><h3>기쁨테라피</h3><p>0507-1280-3183</p></a>
  <a href="tel:0507-1280-3180"><h3>미인클럽테라피</h3><p>0507-1280-3180</p></a>
</div>
</div></section>

<!-- 모든 지역 칩스 영역 -->
<section class="sec"><div class="wrap"><h2 class="serif"><em>다른</em> 동네</h2><p class="sub">원하시는 동네 이름을 누르면 그곳 안내로 이어집니다.</p>
<div class="chips">
{chips_html}
</div></div></section>

<footer>
<div class="wrap"><div class="logo" style="justify-content:center;color:#fff;font-size:19px;"><b></b>수도테라피</div><p style="color:#b8bcc0;font-size:14px;margin-top:10px;">프리미엄 테라피 안내</p></div>
</footer>
<a class="fab" href="#companies">업체<br>보기</a>
</body>
</html>
"""

# 메인 페이지 파일 쓰기
with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(main_template)

# 5. 서브 페이지(지역) HTML 템플릿 (출장마사지 제외)
sub_template = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{dong} 프리미엄 테라피 | 수도테라피</title>
<meta name="description" content="{dong} 수도테라피에서 검증된 프리미엄 홈테라피 업체를 만나보세요. 끝나고 캐모마일 차 한 잔이면 밤이 짧아지는 날 {dong}으로 갑니다.">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico">
<meta property="og:type" content="website">
<meta property="og:title" content="{dong} 프리미엄 테라피 | 수도테라피">
<meta property="og:description" content="{dong} 수도테라피에서 검증된 프리미엄 홈테라피 업체를 만나보세요. 끝나고 캐모마일 차 한 잔이면 밤이 짧아지는 날 {dong}으로 갑니다.">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://sudo-therapy.netlify.app/img/og-root.jpg">

<script>
  document.addEventListener("DOMContentLoaded", function() {{
    const canonicalUrl = document.querySelector('link[rel="canonical"]')?.href || window.location.href;
    const jsonLd = {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "url": canonicalUrl,
      "name": document.title,
      "description": document.querySelector('meta[name="description"]')?.content || "",
      "itemListElement": [
        {{"@type": "LocalBusiness", "position": 1, "name": "퀸즈홈테라피", "telephone": "0507-1280-3296"}},
        {{"@type": "LocalBusiness", "position": 2, "name": "한국미인테라피", "telephone": "0507-1280-3140"}},
        {{"@type": "LocalBusiness", "position": 3, "name": "오늘밤테라피", "telephone": "0507-1280-3199"}},
        {{"@type": "LocalBusiness", "position": 4, "name": "주주테라피", "telephone": "0507-1280-3197"}},
        {{"@type": "LocalBusiness", "position": 5, "name": "기쁨테라피", "telephone": "0507-1280-3183"}},
        {{"@type": "LocalBusiness", "position": 6, "name": "미인클럽테라피", "telephone": "0507-1280-3180"}}
      ]
    }};
    const script = document.createElement('script');
    script.type = "application/ld+json";
    script.text = JSON.stringify(jsonLd);
    document.head.appendChild(script);
  }});
</script>

<style>
{css}
</style>
</head>
<body class="root">
<header class="bar"><div class="wrap"><a class="logo" href="{base}/"><b></b>수도테라피</a><a class="pill" href="#companies">제휴 업체</a></div></header>

<section class="hero">
<div class="wrap">
<h1 class="serif">{dong} 프리미엄 테라피<br>스웨디시 홈테라피</h1>
<p class="lead">씻을 기운조차 없는 날이 있죠. {dong}까지 제휴 업체가 편안함을 안고 갑니다.</p>
<div class="cta"><a class="pill lg" href="#companies">업체 바로보기</a></div>
</div>
</section>

<section id="companies" class="sec gray"><div class="wrap"><h2 class="serif"><em>{dong}</em> 제휴 업체</h2><p class="sub">원하시는 업체를 누르시면 바로 연결됩니다.</p>
<div class="companies-grid">
  <a href="tel:0507-1280-3296"><h3>퀸즈홈테라피</h3><p>0507-1280-3296</p></a>
  <a href="tel:0507-1280-3140"><h3>한국미인테라피</h3><p>0507-1280-3140</p></a>
  <a href="tel:0507-1280-3199"><h3>오늘밤테라피</h3><p>0507-1280-3199</p></a>
  <a href="tel:0507-1280-3197"><h3>주주테라피</h3><p>0507-1280-3197</p></a>
  <a href="tel:0507-1280-3183"><h3>기쁨테라피</h3><p>0507-1280-3183</p></a>
  <a href="tel:0507-1280-3180"><h3>미인클럽테라피</h3><p>0507-1280-3180</p></a>
</div>
</div></section>

<!-- 서브 페이지에도 동일하게 지역 칩스 영역 삽입 -->
<section class="sec"><div class="wrap"><h2 class="serif"><em>다른</em> 동네</h2><p class="sub">원하시는 동네 이름을 누르면 그곳 안내로 이어집니다.</p>
<div class="chips">
{chips}
</div></div></section>

<footer>
<div class="wrap"><div class="logo" style="justify-content:center;color:#fff;font-size:19px;"><b></b>수도테라피</div><p style="color:#b8bcc0;font-size:14px;margin-top:10px;">{dong} 프리미엄 테라피 안내</p></div>
</footer>
<a class="fab" href="#companies">업체<br>보기</a>
</body>
</html>
"""

# 6. 구/동 단위로 서브페이지 폴더 및 HTML 생성 (Sitemap 연동)
sitemap_urls = [f"{base_url}/"]

for gu_key, gu_info in seoul_data.items():
    gu_name = gu_info['name']
    
    # 구(Gu) 폴더 생성 
    gu_folder = os.path.join(base_dir, gu_name)
    os.makedirs(gu_folder, exist_ok=True)
    gu_url = f"{base_url}/{quote(gu_name)}/"
    sitemap_urls.append(gu_url)
    
    with open(os.path.join(gu_folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(sub_template.format(dong=gu_name, url=gu_url, base=base_url, chips=chips_html, css=COMMON_CSS))
    
    # 동(Dong) 폴더 생성
    for dong in gu_info['dongs']:
        dong_folder = os.path.join(base_dir, dong)
        os.makedirs(dong_folder, exist_ok=True)
        dong_url = f"{base_url}/{quote(dong)}/"
        sitemap_urls.append(dong_url)
        
        with open(os.path.join(dong_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(sub_template.format(dong=dong, url=dong_url, base=base_url, chips=chips_html, css=COMMON_CSS))

# 7. Sitemap.xml 생성
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n"
sitemap_content += '</urlset>'

with open(os.path.join(base_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_content)

# 8. Robots.txt 생성
robots_content = f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n"
with open(os.path.join(base_dir, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots_content)

print("✅ 모든 메인/지역 페이지 및 sitemap.xml, robots.txt 생성이 완료되었습니다.")