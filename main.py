import os
import sys
import requests
import json
from datetime import datetime, timedelta
import pytz

# ================= 核心配置区域 =================
# 1. 设置优甲乐开始循环的日期（明天）
# 逻辑：这一天吃 1 片，第二天吃 0.5，第三天吃 1...
START_DATE_STR = "2026-02-12"

# 2. 从 GitHub 设置里获取飞书 Webhook（不用改这里，去 Settings 里配）
WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK")

# 3. 设置时区为北京时间
TZ = pytz.timezone('Asia/Shanghai')

# ================= 功能函数 =================

def get_euthyrox_dose():
    """
    计算优甲乐剂量
    逻辑：(当前日期 - 开始日期) 的天数差。
    如果是偶数天 (0, 2, 4...) -> 1 片
    如果是奇数天 (1, 3, 5...) -> 0.5 片
    """
    start_date = datetime.strptime(START_DATE_STR, "%Y-%m-%d").date()
    current_date = datetime.now(TZ).date()
    
    delta = (current_date - start_date).days
    
    # 如果还没到开始日期
    if delta < 0:
        return "⏳ 尚未开始 (等待2月12日)"
    
    if delta % 2 == 0:
        return "💊 1 片 (整片)"
    else:
        return "🔪 0.5 片 (半片)"

def send_feishu_card(title, content_markdown):
    """
    发送飞书交互式卡片 (红色加急版)
    """
    if not WEBHOOK_URL:
        print("错误：未找到 FEISHU_WEBHOOK 环境变量")
        return

    # 飞书卡片的消息体
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "red",  # 红色标题表示紧急
                "title": {
                    "content": f"🚨 {title}",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": content_markdown,
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr" # 分割线
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "content": "请务必按量服用，确认后请在群里回复",
                            "tag": "plain_text"
                        }
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        print(f"消息发送状态: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"发送出错: {e}")

# ================= 主程序入口 =================

def main():
    # 获取外部传入的参数，决定发送哪个提醒
    if len(sys.argv) < 2:
        print("请指定任务类型: morning_8, morning_930, evening_1830, night_2230")
        return
    
    task_type = sys.argv[1]
    
    # --- 1. 早上 08:00 (优甲乐循环 + 安琪坦) ---
    if task_type == "morning_8":
        dose = get_euthyrox_dose()
        msg = (
            "<at id='all'></at> **早上好！空腹用药提醒**\n\n"
            f"1. **优甲乐：** **{dose}** (今日关键剂量)\n"
            "2. **安琪坦：** 塞 1 粒"
        )
        send_feishu_card("08:00 用药提醒", msg)

    # --- 2. 早上 09:30 (饭后一堆药) ---
    elif task_type == "morning_930":
        msg = (
            "<at id='all'></at> **早饭后记得吃药**\n\n"
            "1. **爱乐维：** 1 粒\n"
            "2. **维生素D：** 5 粒\n"
            "3. **DHA：** 2 粒\n"
            "4. **免疫球蛋白：** 2 粒\n"
            "5. **地屈孕酮：** 2 粒\n"
            "6. **小红片：** 1 片"
        )
        send_feishu_card("09:30 用药提醒", msg)

    # --- 3. 晚上 18:30 (晚饭后) ---
    elif task_type == "evening_1830":
        msg = (
            "<at id='all'></at> **晚饭后用药提醒**\n\n"
            "1. **地屈孕酮：** 2 片\n"
            "2. **补佳乐：** 1 片\n"
            "3. **小红片：** 1 片"
        )
        send_feishu_card("18:30 用药提醒", msg)

    # --- 4. 晚上 22:30 (睡前) ---
    elif task_type == "night_2230":
        msg = (
            "<at id='all'></at> **睡前安琪坦**\n\n"
            "1. **安琪坦：** 塞 1 粒\n"
            "2. (准备睡觉，晚安)"
        )
        send_feishu_card("22:30 用药提醒", msg)

if __name__ == "__main__":
    main()
