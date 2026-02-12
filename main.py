import os
import sys
import requests
import json
from datetime import datetime, timedelta
import pytz

# ================= 核心配置 =================
START_DATE_STR = "2026-02-12"
WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK")
TZ = pytz.timezone('Asia/Shanghai')

# ================= 功能函数 =================

def get_euthyrox_dose():
    """计算优甲乐剂量"""
    start_date = datetime.strptime(START_DATE_STR, "%Y-%m-%d").date()
    current_date = datetime.now(TZ).date()
    delta = (current_date - start_date).days
    
    if delta < 0: return "⏳ 尚未开始"
    return "💊 1 片 (整片)" if delta % 2 == 0 else "🔪 0.5 片 (半片)"

def send_feishu_card(title, content_markdown, is_check=False):
    """发送飞书卡片"""
    if not WEBHOOK_URL:
        print("Error: No Webhook")
        return

    # 查岗时用橙色标题，普通提醒用红色
    header_color = "orange" if is_check else "red"
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": header_color, 
                "title": {"content": f"🚨 {title}", "tag": "plain_text"}
            },
            "elements": [
                {"tag": "div", "text": {"content": content_markdown, "tag": "lark_md"}},
                {"tag": "hr"},
                {
                    "tag": "note", 
                    "elements": [{"content": "彪哥语录：做人要诚实，身体是自己的！", "tag": "plain_text"}]
                }
            ]
        }
    }

    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Error: {e}")

# ================= 主程序 =================

def main():
    if len(sys.argv) < 2: return
    task_type = sys.argv[1]
    
    # ---------------- 早上 08:00 档 ----------------
    if task_type == "morning_8":
        dose = get_euthyrox_dose()
        msg = (
            "<at id='all'></at> **早安！彪哥来查岗了！**\n"
            "一日之计在于晨，别磨磨唧唧的！\n"
            f"1. **优甲乐：** **{dose}** (空腹！空腹！)\n"
            "2. **安琪坦：** 塞 1 粒"
        )
        send_feishu_card("彪哥早间医嘱 (08:00)", msg)

    elif task_type == "morning_8_check":
        msg = (
            "<at id='all'></at> **半小时过去了，吃没吃呢？**\n"
            "彪哥寻思你应该不能骗我。\n"
            "**别跟我整那虚头巴脑的，没吃赶紧去！**\n"
            "要是吃了，就回复个 1，让我放心！"
        )
        send_feishu_card("彪哥回马枪 (08:30)", msg, is_check=True)

    # ---------------- 上午 09:30 档 ----------------
    elif task_type == "morning_930":
        msg = (
            "<at id='all'></at> **该吃大把药了！**\n"
            "论成败人生豪迈，这点药得按时吃，没毛病！\n"
            "1. **爱乐维** 1 粒 | **维D** 5 粒\n"
            "2. **DHA** 2 粒 | **免疫球蛋白** 2 粒\n"
            "3. **地屈孕酮** 2 粒 | **小红片** 1 片"
        )
        send_feishu_card("彪哥温馨提示 (09:30)", msg)

    elif task_type == "morning_930_check":
        msg = (
            "<at id='all'></at> **咋样了？药咽下去没？**\n"
            "我就怕你一忙起来把正事忘了。\n"
            "**身体可是革命的本钱，必须咔咔拿下！**\n"
            "赶紧的，别让彪哥操心！"
        )
        send_feishu_card("彪哥突击检查 (10:00)", msg, is_check=True)

    # ---------------- 晚上 18:30 档 ----------------
    elif task_type == "evening_1830":
        msg = (
            "<at id='all'></at> **晚饭后别光顾着乐呵！**\n"
            "天大地大，身体最大！\n"
            "1. **地屈孕酮** 2 片\n"
            "2. **补佳乐** 1 片 | **小红片** 1 片"
        )
        send_feishu_card("彪哥晚间指示 (18:30)", msg)

    elif task_type == "evening_1830_check":
        msg = (
            "<at id='all'></at> **是不是又把药忘了？**\n"
            "别以为天黑了彪哥就看不见你了。\n"
            "**抓紧把药吃了，做个讲究人！**"
        )
        send_feishu_card("彪哥晚间巡视 (19:00)", msg, is_check=True)

    # ---------------- 晚上 22:30 档 ----------------
    elif task_type == "night_2230":
        msg = (
            "<at id='all'></at> **最后这一哆嗦！**\n"
            "整完安琪坦赶紧睡觉，梦里啥都有！\n"
            "**安琪坦：** 塞 1 粒"
        )
        send_feishu_card("彪哥睡前叮嘱 (22:30)", msg)

    elif task_type == "night_2230_check":
        msg = (
            "<at id='all'></at> **还不睡？还不塞药？**\n"
            "熬夜对身体不好，听彪哥一句劝！\n"
            "**整完赶紧躺下，明天又是咔咔的一天！**"
        )
        send_feishu_card("彪哥最后通牒 (23:00)", msg, is_check=True)

if __name__ == "__main__":
    main()
