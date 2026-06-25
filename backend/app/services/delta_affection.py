from app.services.state import(
    update_affection,
    get_affection
)
from app.services.events import(get_available_events)
event = get_available_events(user_id="user000", heroine_id="heroine02")


import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def apply_affection_rules(message: str, speaker: str):
    # if "うれしい" in message:
    #     update_affection(3)
    # elif "好き" in message:
    #     update_affection(5)
    # elif "嫌い" in message:
    #     update_affection(-5)
    evaluate_emotions(message, speaker)
    get_affection("user000", "heroine02")


emotions_history_ai = np.array([[], [], [], [], [], [], [], []])
emotions_history_user = np.array([[], [], [], [], [], [], [], []])

#モデルとトークナイザの読み込み
model_name = "neuralnaut/deberta-wrime-emotions"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def evaluate_emotions(text, speaker):
    global emotions_history_ai
    global emotions_history_user

    # 1. 分析したいテキスト
    # text

    # 2. テキストをモデルの入力形式に変換
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)

    # 3. 予測を実行
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)

    # 4. 結果の取り出しとデノーマライズ（0.0〜1.0 から 0.0〜3.0 スケールへ変換）
    predictions = outputs.logits.cpu().numpy()[0]
    predictions_original = predictions * 3.0
    predictions_original = np.clip(predictions_original, 0.0, 3.0)

    # 5. 結果の表示
    EMOTION_LABELS = [
        "喜び (joy)",
        "悲しみ (sadness)",
        "期待 (anticipation)",
        "驚き (surprise)",
        "怒り (anger)",
        "恐れ (fear)",
        "嫌悪 (disgust)",
        "信頼 (trust)",
    ]
    print("【感情の分析結果（強さ：0.0 〜 3.0）】")
    for label, score in zip(EMOTION_LABELS, predictions_original):
        print(f"- {label}: {score:.2f}")

    if speaker == "ai":
        emotions_history_ai = np.column_stack((emotions_history_ai, predictions_original))
        print(f"イベント: {event['name'] if event else 'なし'}\n")
        print(f"出力テキスト: {text}\n")
        evaluate_favorable()
    elif speaker == "user":
        emotions_history_user = np.column_stack((emotions_history_user, predictions_original))
        print(f"入力テキスト: {text}\n")


weights = np.array([1.0, -0.3, 0.8, 0.0, -1.2, -0.8, -1.5, 1.5]) #各感情の重み


def evaluate_favorable():
    global emotions_history_user
    global emotions_history_ai

    score_emotions_history_ai = weights @ emotions_history_ai  # 内積を計算、各回の感情ベクトルと重みの内積は各回の現在の好感度となり得る
    print("内積:", score_emotions_history_ai[-1])

    if emotions_history_ai.shape[1] < 7:
        update_affection("user000", "heroine02", score_emotions_history_ai[-1] * 0.5)
        return

    # 移動平均MAを計算する、短期と長期の傾向の比較が可能、それにより現在の好感度の傾向がわかる。これを今のターンの会話の好感度の変化の正負と一致するかを比較することで、好感度変化により正確の変化を計算できる。
    short_term = 3
    long_term = 7

    turn = 10

    score_emotions_history_ai_cut = score_emotions_history_ai[turn - 7:turn]

    short_term_data = score_emotions_history_ai_cut[-short_term:]
    ma_short = np.mean(short_term_data)

    long_term_data = score_emotions_history_ai_cut[-long_term:]
    ma_long = np.mean(long_term_data)

    ma_difference = ma_short - ma_long

    print("移動平均の差:", ma_difference)
    # 以上より傾向の算出による好感度の変化を決定することができる
    # 人間の感情を共感性を考慮して、会話のターンの事の両者の感情の数値が同じ傾向にあるかを比較して、感情の共感ができているかを数値化する。これの変化度合いを利用して、親密度または好感度に影響を与える。

    # 各感情の間の関係性を数値化した行列である、のちに機械学習で各ユーザーの会話に合わせて動的に調節すると理想
    C = np.array([
        #  喜び    悲しみ   期待    驚き    怒り    恐れ    嫌悪    信頼   (Bの感情)
        [1.0, -0.5, 0.5, 0.3, -0.8, -0.5, -1.0, 0.8],  # 喜び (A)
        [-1.0, 1.0, -0.2, 0.2, -0.5, -0.2, -0.5, 0.8],  # 悲しみ (A)
        [0.7, -0.5, 0.8, 0.3, -0.5, -0.5, -0.8, 0.8],  # 期待 (A)
        [0.5, -0.2, 0.4, 0.5, -0.3, -0.3, -0.5, 0.5],  # 驚き (A)
        [-0.8, -0.5, -0.5, 0.2, 0.5, -0.5, -0.5, 0.2],  # 怒り (A)
        [-0.5, 0.2, -0.2, 0.2, -0.5, 0.5, -0.5, 0.8],  # 恐れ (A)
        [-1.0, -0.5, -0.8, 0.0, -0.5, -0.5, 0.3, -0.5],  # 嫌悪 (A)
        [0.8, -0.5, 0.8, 0.3, -0.5, -0.5, -1.0, 1.0]  # 信頼 (A)
    ])

    current_ai = emotions_history_ai[:, -1]
    current_user = emotions_history_user[:, -1]

    # 共感性の計算
    empathy_score = current_ai @ C @ current_user
    print("共感度:", empathy_score)

    print("好感度変化:", score_emotions_history_ai[-1] + ma_difference + empathy_score)

    update_affection("user000", "heroine02", score_emotions_history_ai[-1] + ma_difference + empathy_score)
