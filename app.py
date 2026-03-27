import streamlit as st
import datetime

# タイトル
st.title("封入作業計算（Packing Calculator）")
st.caption("時間差人員・フィルム/ケース混在に対応")

# 入力
total = st.number_input("件数", value=400)

ratio = st.slider("フィルム割合", 0.0, 1.0, 0.85)
case_ratio = 1 - ratio

st.write(f"ケース割合：{case_ratio:.1f}")

people_early = st.number_input("前半人数（10:00〜10:30）", value=2)
people_late = st.number_input("後半人数（10:30以降）", value=3)

start_time = st.time_input("開始時間", datetime.time(10, 0))

# 件数内訳
film = total * ratio
case = total * case_ratio

# 内訳表示
st.subheader("内訳")
st.write(f"フィルム件数：約 {film:.0f} 件")
st.write(f"ケース件数：約 {case:.0f} 件")

# ケース多い警告
if case_ratio > 0.4:
    st.warning("⚠️ ケース比率が高めです（時間かかる可能性あり）")

# 処理能力
film_rate = 100
case_rate = 40

# 前半30分（0.5時間）
early_capacity = ((film_rate * ratio) + (case_rate * case_ratio)) * people_early * 0.5

# 残り
remaining = total - early_capacity

# 後半処理能力（1時間）
late_capacity_per_hour = ((film_rate * ratio) + (case_rate * case_ratio)) * people_late

# 後半時間
if remaining > 0:
    late_time = remaining / late_capacity_per_hour
else:
    late_time = 0

# 総時間
total_time = 0.5 + late_time

# 終了時間
start_dt = datetime.datetime.combine(datetime.date.today(), start_time)
end_dt = start_dt + datetime.timedelta(hours=total_time)

# 結果表示
st.subheader("結果")

st.write(f"前半処理件数：約 {early_capacity:.0f} 件")
st.write(f"残件数：約 {max(0, remaining):.0f} 件")
st.write(f"作業時間：約 {total_time:.2f} 時間")

st.success(f"終了時間：{end_dt.strftime('%H:%M')}")

# 12時判定
deadline = datetime.datetime.combine(datetime.date.today(), datetime.time(12, 0))

if end_dt <= deadline:
    st.success("✅ 12時までに完了予定です")
else:
    st.error("⚠️ 12時を超える見込みです")
