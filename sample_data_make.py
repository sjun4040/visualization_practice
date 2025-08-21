import pandas as pd
import numpy as np
import random

# reproducibility
random.seed(42)
np.random.seed(42)

# 날짜 생성 (2025-01-01 ~ 2025-08-20 사이)
date_range = pd.date_range(start="2025-01-01", end="2025-08-20")

# 카테고리 정의
flavors = ["초코", "딸기", "바닐라", "녹차", "커피"]
cup_sizes = ["스몰", "미디엄", "라지"]
genders = ["남", "여"]
age_groups = ["10대", "20대", "30대", "40대", "50대이상"]

# 주문 개수 확률 분포
quantities = [1, 2, 3, 4]
quantity_probs = [0.45, 0.35, 0.15, 0.05]

# 맛별 기본 가격 (예시)
flavor_prices = {
    "초코": 3200,
    "딸기": 3000,
    "바닐라": 2800,
    "녹차": 3300,
    "커피": 3100
}

# 컵사이즈별 추가 금액 (예시)
cup_extra = {
    "스몰": 0,
    "미디엄": 700,
    "라지": 1500
}

# 샘플 데이터 400건 생성
data = {
    "날짜": np.random.choice(date_range, 400),
    "성별": np.random.choice(genders, 400),
    "연령대": np.random.choice(age_groups, 400, p=[0.15, 0.35, 0.25, 0.15, 0.10]),
    "맛": np.random.choice(flavors, 400),
    "컵사이즈": np.random.choice(cup_sizes, 400, p=[0.4, 0.4, 0.2]),
    "개수": np.random.choice(quantities, 400, p=quantity_probs)
}

df = pd.DataFrame(data)

# 가격 계산 컬럼 추가
def calc_price(row):
    base = flavor_prices[row['맛']]
    extra = cup_extra[row['컵사이즈']]
    total = (base + extra) * row['개수']
    return total

df['매출'] = df.apply(calc_price, axis=1)

# 날짜순 정렬
df = df.sort_values("날짜").reset_index(drop=True)

# CSV 저장
df.to_csv("icecream_sales.csv", index=False, encoding="utf-8-sig")

print("✅ icecream_sales.csv 파일이 생성되었습니다!")
print(df.head())
