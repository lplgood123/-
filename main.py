import os
import sys
import requests
import json
from datetime import datetime, timedelta
import pytz

# ================= 核心配置区域 =================
# 1. 设置优甲乐开始循环的日期（明天）
START_DATE_STR = "2026-02-12"

# 2. 从 GitHub 设置里获取飞书 Webhook
WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK")

# 3. 设置时区为北京时间
TZ = pytz.timezone('Asia/Shanghai')

# ================= 功能函数 =================

def get_euthyrox_dose():
    """计算优甲乐剂量"""
    start_date = datetime.strptime(START_DATE_STR, "%Y-%m-%d").date()
    current_date = datetime.now(TZ).date()
    
    delta = (current_date - start_date).days
    
    if delta < 0:
        return "⏳ 尚未开始"
    
    if delta % 2 == 0:
        return "💊 1 片 (整片)"
    else:
        return "🔪 0.5 片 (半片)"

def send_feishu_card(title, content_markdown):
    """发送飞书交互式卡片 (红色加急版)"""
    if not WEBHOOK_URL:
        print("错误：未找到 FEISHU_WEBHOOK 环境变量")
        return

    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "red",
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
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "content": "彪哥语录：身体是革命的本钱，必须咔咔拿下！",
                            "tag": "plain_text"
                        }
                    ]
                }
            ]
        }
    }

    try:
        requests.post(WEBHOOK_URL, json=payload)
        print("消息发送成功")
    except Exception as e:
        print(f"发送出错: {e}")

# ================= 主程序入口 =================

def main():
    if len(sys.argv) < 2:
        print("请指定任务类型")
        return
    
    task_type = sys.argv[1]
    
    # --- 1. 早上 08:00 ---
    if task_type == "morning_8":
        dose = get_euthyrox_dose()
        msg = (
            "<at id='all'></at> **早安！彪哥来查岗了！**\n"
            "一日之计在于晨，这点事儿都办不明白吗？\n"
            "**必须空腹，把这药给我安排上！听见没？**\n\n"
            f"1. **优甲乐：** **{dose}** (看准了别吃错)\n"
            "2. **安琪坦：** 塞 1 粒"
        )
        send_feishu_card("彪哥早间医嘱 (08:00)", msg)

    # --- 2. 早上 09:30 ---
    elif task_type == "morning_930":
        msg = (
            "<at id='all'></at> **听彪哥一句劝，该吃药了！**\n"
            "**论成败人生豪迈，这点药得按时吃，身体必须咔咔的！没毛病！**\n\n"
            "1. **爱乐维：** 1 粒\n"
            "2. **维生素D：** 5 粒\n"
            "3. **DHA：** 2 粒\n"
            "4. **免疫球蛋白：** 2 粒\n"
            "5. **地屈孕酮：** 2 粒\n"
            "6. **小红片：** 1 片"
        )
        send_feishu_card("彪哥温馨提示 (09:30)", msg)

    # --- 3. 晚上 18:30 ---
    elif task_type == "evening_1830":
        msg = (
            "<at id='all'></at> **晚饭吃挺好呗？别光顾着乐呵！**\n"
            "天大地大，身体最大！该干正事了，抓紧把药吃了！\n"
            "**讲究人，办事必须有头有尾！**\n\n"
            "1. **地屈孕酮：** 2 片\n"
            "2. **补佳乐：** 1 片\n"
            "3. **小红片：** 1 片"
        )
        send_feishu_card("彪哥晚间指示 (18:30)", msg)

    # --- 4. 晚上 22:30 ---
    elif task_type == "night_2230":
        msg = (
            "<at id='all'></at> **天不早了，最后这一哆嗦！**\n"
            "整完赶紧睡觉，梦里啥都有！\n"
            "**身体养得杠杠的，必须拿下！晚安！**\n\n"
            "1. **安琪坦：** 塞 1 粒"
        )
        send_feishu_card("彪哥睡前叮嘱 (22:30)", msg)

if __name__ == "__main__":
    main()
