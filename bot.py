import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from telegram.constants import ParseMode
import random
import detection
from detection import detect_pose, process_image, detect_pose_ai
# Import all functions from detection.py
 # === Database initialization ===
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()

 # === Add chat_id to the database ===
def add_user(chat_id: int):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

 # === Get all chat_id ===
def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]

 # Test stages
Q1, Q2, Q3, Q4, Q5 = range(5)
T1_Q1, T1_Q2, T1_Q3, T1_Q4, T1_Q5, T1_Q6, T1_Q7, T1_Q8, T1_Q9, T1_Q10 = range (10)
C_Q1, C_Q2, C_Q3, C_Q4, C_Q5, C_Q6 = range(6)
F_Q1, F_Q2, F_Q3, F_Q4, F_Q5, F_Q6, F_Q7, F_Q8, F_Q9, F_Q10 = range(10)
P_Q1, P_Q2, P_Q3, P_Q4, P_Q5, P_Q6, P_Q7, P_Q8, P_Q9, P_Q10, P_Q11, P_Q12 = range(12)
T2_Q1, T2_Q2, T2_Q3, T2_Q4, T2_Q5, T2_Q6, T2_Q7, T2_Q8, T2_Q9= range(9)
HISTORY = [
    "Ancient India",
    "Yoga Sutras of Patanjali",
    "Medieval Schools",
    "British Colonization",
    "Emergence of Hatha Yoga",
    "Swami Vivekananda",
    "Yoga in the USA",
    "Global Boom"
]
HISTORY_PRINT = {
    'Ancient India': 'Yoga emerges as a spiritual and physical practice in ancient India over 2500 years ago.',
    'Yoga Sutras of Patanjali': 'Patanjali systematizes yoga in his treatise "Yoga Sutras" around the 2nd century BCE.',
    'Medieval Schools': 'In the medieval period, various schools of yoga appear, including Raja Yoga, Bhakti Yoga, and Karma Yoga.',
    'British Colonization': 'During British colonization of India, yoga partially loses popularity but is preserved in traditional schools.',
    'Emergence of Hatha Yoga': 'In the 15th-16th centuries, Hatha Yoga develops as a physical practice combining asanas, pranayama, and meditation.',
    'Swami Vivekananda': 'Swami Vivekananda presents yoga to the West at the World Parliament of Religions in Chicago in 1893.',
    'Yoga in the USA': 'In the 20th century, yoga becomes popular in the USA thanks to masters such as Pattabhi Jois, B.K.S. Iyengar, and Indra Devi.',
    'Global Boom': 'From the late 20th century, yoga gains worldwide popularity as a health and spiritual practice.'
}
D_Q1=range(1)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_user(chat_id)
    await update.message.reply_text(
        "✋ Welcome to the yoga community!\n\n"
        "To begin your journey and become a yoga enthusiast, I suggest:\n\n"
        "   1. Familiarize yourself with the theoretical material (recommended: 'Light on Yoga' by B.K.S. Iyengar, 'The Heart of Yoga' by T.K.V. Desikachar).\n"
        "   2. Test your knowledge with a short quiz.\n\n"
        "⚪️ If you already know the basics, type /test to start!\n\n"
        "⚪️ If you have passed the initiation, try thematic quizzes:\n\n"
        "🔘 BASE\n"
        "   🫀 Practice basics /practice\n"
        "   🩹 Pain management /pain\n"
        "   🧘🏼‍♀️ About yoga, spirituality, meditation — /yoga\n"
        "   📜 History of yoga — /history\n\n"
        "🔘 OTHER\n"
        "   ▪️ Yoga exam /exam\n"
        "   ▪️ Test for cultural yoga literacy /culture\n\n"
        "🔘 STUDY\n"
        "   🖼️ Interactive detection of the pose by photo /detect"
    )


# --- Test handling ---
async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("No", callback_data="q1_No"), InlineKeyboardButton("Yes", callback_data="q1_Yes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "1. Is yoga only effective for people who are flexible? (Reference: Light on Yoga)",
        reply_markup=reply_markup
    )
    return Q1

async def test_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]  # Get "Yes" or "No"

    keyboard = [
        [InlineKeyboardButton("No", callback_data="q2_No"), InlineKeyboardButton("Yes", callback_data="q2_Yes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "2. Can the lower back safely bend in a large range of motion? (Reference: Yoga Anatomy)",
        reply_markup=reply_markup
    )
    return Q2

async def test_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("No", callback_data="q3_No"), InlineKeyboardButton("Yes", callback_data="q3_Yes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "3. Is it okay to skip Savasana at the end of a yoga class if you feel like it? (Reference: Light on Yoga)",
        reply_markup=reply_markup
    )
    return Q3

async def test_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("No", callback_data="q4_No"), InlineKeyboardButton("Yes", callback_data="q4_Yes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "4. Is it recommended to have a full meal half an hour before yoga practice? (Reference: The Heart of Yoga)",
        reply_markup=reply_markup
    )
    return Q4

async def test_q5_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data['q4'] = query.data.split('_')[1]
    await update.callback_query.message.reply_text(
        "5. Name one classic yoga text referenced in modern yoga classes.",
        reply_markup=ReplyKeyboardRemove()
    )
    return Q5

async def test_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    return await test_end(update, context)

async def test_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score=1
    query = update.message

    # Check answers (example)
    correct_answers = {'q1': 'No', 'q2': 'No', 'q3': 'No', 'q4': 'No'}
    correct_answers_print = {'q1': 'No', 'q2': 'No', 'q3': 'No', 'q4': 'No'}
    explanations={
        'q1': "Correct answer: No. Yoga is beneficial for everyone, regardless of flexibility. The focus is on mindful movement, breath, and attention. (Light on Yoga)",
        'q2': "Correct answer: No. Anatomically, the lower back has a limited range of safe extension. Most movement should be gentle and controlled. (Yoga Anatomy)",
        'q3': "Correct answer: No. Savasana is an essential part of practice, allowing the body and mind to integrate the benefits. Skipping it can reduce the effectiveness of the session. (Light on Yoga)",
        'q4': "Correct answer: No. It is recommended to eat at least 1.5-2 hours before practice. A light snack is acceptable if hungry. (The Heart of Yoga)",
        'q5': "Correct answer: Examples include 'Light on Yoga', 'Yoga Sutras of Patanjali', 'The Heart of Yoga'."
    }
    results = []
    result_message=""
    for q in ['q1', 'q2', 'q3', 'q4']:
        user_answer = context.user_data.get(q)
        explanation_text=explanations[q]
        if user_answer == correct_answers[q]:
            correct = "✅" 
            score+=1 
        else :
            correct = "❌"
        results.append(f"{q.upper()}: {correct_answers_print[q]} {correct} \n\n{explanation_text}\n\n")
    if score == 2:
        result_message="2 in the diary, call your mom to school!\n"
    elif score == 5:
        result_message= "You passed the initiation, congratulations!\n"
    else:
        result_message= "You're almost there, practice a bit more!\n"
    results.append(f"Q5: {context.user_data.get('q5')}✅\n\n{explanations['q5']}\n\n")

    await update.message.reply_text(
        "Thank you for your answers!"+"\n"+result_message+f"Here are your results: {score}/5"+"\n\n" + "\n".join(results)
    )
    return ConversationHandler.END

async def test_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Test cancelled.")
    return ConversationHandler.END

 # --- Exam handling ---
async def exam_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("False", callback_data="q1_False"), InlineKeyboardButton("True", callback_data="q1_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "1. Yoga originated in China.",
        reply_markup=reply_markup
    )
    return T1_Q1

async def exam_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q2_False"), InlineKeyboardButton("True", callback_data="q2_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "2. The word 'asana' means 'breath' in Sanskrit.",
        reply_markup=reply_markup
    )
    return T1_Q2

async def exam_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q3_False"), InlineKeyboardButton("True", callback_data="q3_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "3. Yoga can help improve balance and flexibility.",
        reply_markup=reply_markup
    )
    return T1_Q3

async def exam_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q4_False"), InlineKeyboardButton("True", callback_data="q4_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "4. Savasana is a standing pose.",
        reply_markup=reply_markup
    )
    return T1_Q4

async def exam_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q4'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q5_False"), InlineKeyboardButton("True", callback_data="q5_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "5. Yoga is only for young and flexible people.",
        reply_markup=reply_markup
    )
    return T1_Q5

async def exam_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q5'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q6_False"), InlineKeyboardButton("True", callback_data="q6_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "6. Pranayama is a type of yoga breathing exercise. ",
        reply_markup=reply_markup
    )
    return T1_Q6

async def exam_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q6'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q7_False"), InlineKeyboardButton("True", callback_data="q7_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "7. Yoga can help reduce stress and promote relaxation. ",
        reply_markup=reply_markup
    )
    return T1_Q7

async def exam_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q7'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q8_False"), InlineKeyboardButton("True", callback_data="q8_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "8. The word 'Namaste' is commonly used as a greeting or farewell in yoga classes.",
        reply_markup=reply_markup
    )
    return T1_Q8

async def exam_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q8'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q9_False"), InlineKeyboardButton("True", callback_data="q9_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "9. Yoga is a competitive sport. (True/False)",
        reply_markup=reply_markup
    )
    return T1_Q9

async def exam_q10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q9'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("False", callback_data="q10_False"), InlineKeyboardButton("True", callback_data="q10_True")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "10. Yoga can be practiced by people of all ages.",
        reply_markup=reply_markup
    )
    return T1_Q10

async def exam_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    score=0
    await query.answer()
    context.user_data['q10'] = query.data.split('_')[1]

    # Correct answers
    correct_answers = {
        'q1': 'False',  # Yoga originated in India, not China
        'q2': 'False',  # Asana means posture, not breath
        'q3': 'True',   # Yoga can help improve balance and flexibility
        'q4': 'False',  # Savasana is not a standing pose
        'q5': 'False',  # Yoga is for everyone
        'q6': 'True',   # Pranayama is a yoga breathing exercise
        'q7': 'True',   # Yoga can reduce stress
        'q8': 'True',   # Namaste is a greeting/farewell in yoga
        'q9': 'False',  # Yoga is not a competitive sport
        'q10': 'True'   # Yoga can be practiced by all ages
    }
    user_answer_print = {"False": 'False', "True": 'True'}
    correct_answers_print = {
        q: user_answer_print[correct_answers[q]] for q in correct_answers
    }

    explanations = {
        'q1': "Explanation: Yoga originated in India, not China.",
        'q2': "Explanation: 'Asana' means 'posture' or 'pose' in Sanskrit, not 'breath'.",
        'q3': "Explanation: Yoga is well known for improving balance and flexibility.",
        'q4': "Explanation: Savasana is a relaxation pose performed lying on the back, not standing. ",
        'q5': "Explanation: Yoga is suitable for people of all ages and abilities, not just the young and flexible. ",
        'q6': "Explanation: Pranayama refers to yogic breathing exercises. ",
        'q7': "Explanation: Yoga can help reduce stress and promote relaxation. ",
        'q8': "Explanation: 'Namaste' is a traditional greeting or farewell in yoga classes.",
        'q9': "Explanation: Yoga is a personal practice, not a competitive sport. ",
        'q10': "Explanation: Yoga can be practiced by people of all ages. "
    }

    results = []
    for q in [f'q{i}' for i in range(1, 11)]:
        user_answer = context.user_data.get(q, '—')
        if user_answer == correct_answers[q]:
            correct = "✅" 
            score+=1 
        else :
            correct = "❌"
        correct_text = correct_answers_print[q]
        explanation_text = explanations.get(q, 'No explanation available.')
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Your answer: {user_answer_print.get(user_answer, user_answer)} {correct}\n"
            f"📘 {explanation_text}\n\n"
        )
    if score == 2:
        result_message="2 in the diary, call your mom to school!\n"
    elif score == 10:
        result_message= "Congratulations, you are a yoga honors student!\n"
    else:
        result_message= "You're almost there, practice a bit more!\n"

    await query.message.reply_text(
         "Thank you for your answers!"+"\n"+result_message+f"Here are your results: {score}/{len(correct_answers)}"+"\n\n" + "\n".join(results)
    )
    return ConversationHandler.END

 # --- Culture test handling ---
async def culture_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚪️Culture Test: Complete the phrase!\n\n"
    "❗️ Please write in lowercase, no spaces at the beginning or end.\n"
    "❗️ _ indicates the number of words.")
    await update.message.reply_text("1. Roses are red, _ _ _")
    return C_Q1

async def culture_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1'] = update.message.text
    await update.message.reply_text("2. The early bird _ ")
    return C_Q2

async def culture_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2'] = update.message.text
    await update.message.reply_text("3. Knock knock, _")
    return C_Q3

async def culture_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3'] = update.message.text
    await update.message.reply_text("4. Why did the chicken _")
    return C_Q4

async def culture_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q4'] = update.message.text
    await update.message.reply_text("5. To be or not to _ ")
    return C_Q5

async def culture_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    await update.message.reply_text("6. Life is like a box of _ _ _ _ _")
    return C_Q6

async def culture_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = 0
    context.user_data['q6'] = update.message.text
    results = []
    correct_answers = {
        'q1': 'violets are blue',
        'q2': 'gets the worm',
        'q3': "who's there",
        'q4': 'cross the road',
        'q5': 'be',
        'q6': 'chocolates'
    }
    l = len(correct_answers)
    question_beginning = {
        'q1': 'Roses are red, ',
        'q2': 'The early bird ',
        'q3': 'Knock knock, ',
        'q4': 'Why did the chicken ',
        'q5': 'To be or not to ',
        'q6': 'Life is like a box of '
    }
    explanations = {
        'q1': "A classic poem starter, often used in jokes and memes. (Reference: Internet culture)",
        'q2': "A common saying about being early and getting rewards. (Reference: English proverbs)",
        'q3': "The start of every knock-knock joke. (Reference: Joke culture)",
        'q4': "The setup for the classic chicken joke. (Reference: Stand-up comedy)",
        'q5': "Shakespeare's famous existential question. (Reference: Hamlet)",
        'q6': "A famous movie quote from Forrest Gump. (Reference: Forrest Gump, 1994)"
    }
    for q in [f'q{i}' for i in range(1, l+1)]:
        user_answer = context.user_data[q]
        if user_answer.strip().lower() == correct_answers[q]:
            score += 1
            correct = "✅"
        else:
            correct = "❌"
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Your answer: {question_beginning[q]}{user_answer}. {correct}\n"
            f"✅ ☑️Correct answer: {question_beginning[q]}{correct_answers[q]}.\n"
            f"📘 Explanation: {explanations[q]}\n\n"
        )
    if score == 2:
        result_message = "2 in the diary, call your mom to school!\n"
    elif score == l:
        result_message = "Congratulations, you are a culture honors student!\n"
    else:
        result_message = "You're almost there, practice a bit more!\n"
    await update.message.reply_text(
        "Thank you for your answers!" + "\n" + result_message + f"Here are your results: {score}/{len(correct_answers)}" + "\n\n" + "\n".join(results)+ "\n" +"P.S. Just kidding, it is always beneficial to laugh a bit :)"
    )
    return ConversationHandler.END

async def practice_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗝️ The main goal of this test is self-reflection.\n" \
                                    "🗝️ There is no score at the end, but you can evaluate yourself by comparing with the correct answers.")
    await update.message.reply_text("1. What is yoga? (1-2 sentences)")
    return F_Q1

async def practice_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1'] = update.message.text
    await update.message.reply_text("2. Name one benefit of regular yoga practice.")
    return F_Q2

async def practice_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2'] = update.message.text
    await update.message.reply_text("3. What is the name of the relaxation pose usually done at the end of a yoga class?")
    return F_Q3

async def practice_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3'] = update.message.text
    await update.message.reply_text("4. Should you force your body into a pose if you feel pain? Why or why not?")
    return F_Q4

async def practice_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q4'] = update.message.text
    await update.message.reply_text("5. What is the Sanskrit word for posture or pose in yoga?")
    return F_Q5

async def practice_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    await update.message.reply_text("6. Is yoga only about physical exercise? ")
    return F_Q6

async def practice_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q6'] = update.message.text
    await update.message.reply_text("7. Name one style or type of yoga.")
    return F_Q7

async def practice_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q7'] = update.message.text
    await update.message.reply_text("8. What is the traditional greeting or closing word used in yoga classes?")
    return F_Q8

async def practice_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q8'] = update.message.text
    await update.message.reply_text("9. What is the main focus of breathing exercises in yoga called?")
    return F_Q9

async def practice_q10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q9'] = update.message.text
    await update.message.reply_text("10. Can yoga be practiced by people of all ages? Why or why not?")
    return F_Q10

async def practice_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q10'] = update.message.text
    results = []
    correct_answers = {
        'q1': 'Yoga is a physical, mental, and spiritual practice that originated in ancient India.',
        'q2': 'Improved flexibility, strength, stress reduction, or better focus.',
        'q3': 'Savasana',
        'q4': 'No',
        'q5': 'Asana',
        'q6': 'No',
        'q7': 'Hatha, Vinyasa, Ashtanga, Yin, or any other style',
        'q8': 'Namaste',
        'q9': 'Pranayama',
        'q10': 'Yes'
    }
    explanations = {
        'q1': 'Yoga is more than just exercise; it includes breath, meditation, and ethical principles. (Common knowledge)',
        'q2': 'Yoga can help with flexibility, strength, balance, relaxation, and mental clarity. (Common knowledge)',
        'q3': 'Savasana is the relaxation pose at the end of class. (Common knowledge)',
        'q4': 'You should never force your body into pain during yoga. (Common knowledge)',
        'q5': '"Asana" is the Sanskrit word for posture or pose. (Common knowledge)',
        'q6': 'Yoga includes breathing, meditation, and philosophy, not just physical exercise. (Common knowledge)',
        'q7': 'There are many styles of yoga, such as Hatha, Vinyasa, Ashtanga, Yin, and more. (Common knowledge)',
        'q8': '"Namaste" is a traditional greeting and closing in yoga. (Common knowledge)',
        'q9': 'Breathing exercises in yoga are called "pranayama". (Common knowledge)',
        'q10': 'Yoga can be practiced by people of all ages and abilities. (Common knowledge)'
    }
    for i in range(1, 11):
        q = f'q{i}'
        user_answer = context.user_data.get(q, '')
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Your answer: {user_answer}\n"
            f"☑️ Correct answer: {correct_answers[q]}\n"
            f"📘 {explanations[q]}\n"
        )
    await update.message.reply_text(
        "Thank you for your answers!\nHere are your results:\n\n" + "\n".join(results)
    )
    return ConversationHandler.END

async def pain_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚪️ Common Knowledge Pain & Muscles Quiz! (Fill in the blank)\n\n"
    "❗️ Please answer in lowercase, no spaces at the beginning or end.\n"
    "❗️ _ indicates the number of words.")
    await update.message.reply_text("1. The largest muscle in the human body is the _ _. (2 words)")
    return P_Q1

async def pain_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1'] = update.message.text
    await update.message.reply_text("2. Pain that is sharp, short, and warns you of immediate harm is known as _ pain. (1 word)")
    return P_Q2

async def pain_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2'] = update.message.text
    await update.message.reply_text("3. The tissue connecting muscle to bone is a _. (1 word)")
    return P_Q3

async def pain_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3'] = update.message.text
    await update.message.reply_text("4. Muscle pain is medically referred to as _. (1 word)")
    return P_Q4

async def pain_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q4'] = update.message.text
    await update.message.reply_text("5. The natural painkillers released by your body during exercise and laughter are called _. (1 word)")
    return P_Q5

async def pain_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    await update.message.reply_text("6. Red blood cells mainly carry _. (1 word)")
    return P_Q6

async def pain_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q6'] = update.message.text
    await update.message.reply_text("7. The vitamin produced in the skin from sunlight, important for healthy bones, is _ _. (2 words)")
    return P_Q7

async def pain_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q7'] = update.message.text
    await update.message.reply_text("8. The mineral essential for muscle contraction is _. (1 word)")
    return P_Q8

async def pain_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q8'] = update.message.text
    await update.message.reply_text("9. The muscles at the front of your thigh are called the _. (1 word)")
    return P_Q9

async def pain_q10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q9'] = update.message.text
    await update.message.reply_text("10. The organ responsible for filtering waste from the blood is the _. (1 word)")
    return P_Q10

async def pain_q11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q10'] = update.message.text
    await update.message.reply_text("11. Pain that lasts more than 3 months is called _. (1 word)")
    return P_Q11

async def pain_q12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q11'] = update.message.text
    await update.message.reply_text("12. Pain is always a sign of injury: True or False? (1 word)")
    return P_Q12

async def pain_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q12'] = update.message.text
    l = len(context.user_data)
    score = 0
    user_answer = {
        'q1': f"The largest muscle in the human body is the <u>{context.user_data['q1']}</u>.",
        'q2': f"Pain that is sharp, short, and warns you of immediate harm is known as <u>{context.user_data['q2']}</u> pain.",
        'q3': f"The tissue connecting muscle to bone is a <u>{context.user_data['q3']}</u>.",
        'q4': f"Muscle pain is medically referred to as <u>{context.user_data['q4']}</u>.",
        'q5': f"The natural painkillers released by your body during exercise and laughter are called <u>{context.user_data['q5']}</u>.",
        'q6': f"Red blood cells mainly carry <u>{context.user_data['q6']}</u>.",
        'q7': f"The vitamin produced in the skin from sunlight, important for healthy bones, is <u>{context.user_data['q7']}</u>.",
        'q8': f"The mineral essential for muscle contraction is <u>{context.user_data['q8']}</u>.",
        'q9': f"The muscles at the front of your thigh are called the <u>{context.user_data['q9']}</u>.",
        'q10': f"The organ responsible for filtering waste from the blood is the <u>{context.user_data['q10']}</u>.",
        'q11': f"Pain that lasts more than 3 months is called <u>{context.user_data['q11']}</u>.",
        'q12': f"Pain is always a sign of injury: <u>{context.user_data['q12']}</u>.",
    }

    correct_answers = {
        'q1': 'gluteus maximus',
        'q2': 'acute',
        'q3': 'tendon',
        'q4': 'myalgia',
        'q5': 'endorphins',
        'q6': 'oxygen',
        'q7': 'vitamin d',
        'q8': 'calcium',
        'q9': 'quadriceps',
        'q10': 'kidney',
        'q11': 'chronic',
        'q12': 'false'
    }
    correct_answers_print = {
        'q1': "The largest muscle in the human body is the <u>gluteus maximus</u>. (Reference: Anatomy textbooks)",
        'q2': "Pain that is sharp, short, and warns you of immediate harm is known as <u>acute</u> pain. (Reference: Medical literature)",
        'q3': "The tissue connecting muscle to bone is a <u>tendon</u>. (Reference: Anatomy textbooks)",
        'q4': "Muscle pain is medically referred to as <u>myalgia</u>. (Reference: Medical literature)",
        'q5': "The natural painkillers released by your body during exercise and laughter are called <u>endorphins</u>. (Reference: Physiology textbooks)",
        'q6': "Red blood cells mainly carry <u>oxygen</u>. (Reference: Biology textbooks)",
        'q7': "The vitamin produced in the skin from sunlight, important for healthy bones, is <u>vitamin d</u>. (Reference: Nutrition science)",
        'q8': "The mineral essential for muscle contraction is <u>calcium</u>. (Reference: Physiology textbooks)",
        'q9': "The muscles at the front of your thigh are called the <u>quadriceps</u>. (Reference: Anatomy textbooks)",
        'q10': "The organ responsible for filtering waste from the blood is the <u>kidney</u>. (Reference: Biology textbooks)",
        'q11': "Pain that lasts more than 3 months is called <u>chronic</u>. (Reference: Medical literature)",
        'q12': "Pain is always a sign of injury: <u>False</u>. (Reference: Medical literature)"
    }
    results = []

    for q in [f'q{i}' for i in range(1, l+1)]:
        correct = ""
        user_a = context.user_data[q]
        if q == 'q11':
            if user_a == '50' or user_a == '60':
                correct = "✅"
                score += 1
            else:
                correct = "❌"
        else:
            if user_a.lower() == correct_answers[q]:
                score += 1
                correct = "✅"
            else:
                correct = "❌"
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Your answer: {user_answer[q]} {correct}\n"
            f"☑️ Correct answer: {correct_answers_print[q]} \n"
        )
    if score == 2:
        result_message = "2 in the diary, call your mom to school!\n"
    elif score == l:
        result_message = "Congratulations, you are a yoga honors student!\n"
    else:
        result_message = "You're almost there, practice a bit more!\n"
    await update.message.reply_text(
        "Thank you for your answers!" + "\n" + result_message + f"Here are your results: {score}/{l}" + "\n\n" + "\n".join(results), parse_mode="HTML"
    )
    return ConversationHandler.END

async def yoga_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("A", callback_data="q1_A"), InlineKeyboardButton("B", callback_data="q1_B"), InlineKeyboardButton("C", callback_data="q1_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>1. When did yoga begin to be associated with spiritual practice closely intertwined with meditation?</b>\n\n"
        "A) Since ancient times, as soon as yoga appeared\n"
        "B) When yoga began to be popularized in India\n"
        "C) In the last century, when yoga from India arrived in America and began to gain popularity there",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q1

async def yoga_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("A", callback_data="q2_A"),
         InlineKeyboardButton("B", callback_data="q2_B"),
         InlineKeyboardButton("C", callback_data="q2_C")]
    ]
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "<b>2. Why did Eastern masters adapt yoga practice to the Western style?</b>\n\n"
        "A) Because the practice of yogis had greatly declined and was no longer effective\n"
        "B) Because the masters understood very well what was needed for Western people with their pace and rhythm of life\n"
        "C) Because such adaptation is safer and more effective than the traditional approach",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q2

# Q3
async def yoga_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="q3_A"),
         InlineKeyboardButton("B", callback_data="q3_B"),
         InlineKeyboardButton("C", callback_data="q3_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>3. Yoga gymnastics practice is primarily:</b>\n\n"
        "A) A spiritual tool closely connected with Hinduism or Buddhism\n"
        "B) A practical tool for psychophysical adaptation and mastering control over perception\n"
        "C) A tool to make the body invincible, beautiful, and healthy",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q3

# Q4
async def yoga_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="q4_A"),
         InlineKeyboardButton("B", callback_data="q4_B"),
         InlineKeyboardButton("C", callback_data="q4_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>4. Due to the strong popularization of adapted practice in the 1960s in America, the original essence and principles of yoga were replaced by:</b>\n\n"
        "A) What was easier to sell\n"
        "B) What was more effective and healthier for the body\n"
        "C) What provided more spiritual development",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q4

# Q5
async def yoga_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q4'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="q5_A"),
         InlineKeyboardButton("B", callback_data="q5_B"),
         InlineKeyboardButton("C", callback_data="q5_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>5. Which of these is NOT true?</b>\n\n"
        "A) Yoga gymnastics practice in India is still used to train Indian special forces\n"
        "B) In martial clan lines of China, Korea, and Vietnam, yoga gymnastics was a tool for rapid training of body and psyche\n"
        "C) Yoga gymnastics was practiced only by religious persons",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q5

# Q6
async def yoga_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q5'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="q6_A"),
         InlineKeyboardButton("B", callback_data="q6_B"),
         InlineKeyboardButton("C", callback_data="q6_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>6. The word 'meditato' was created by:</b>\n\n"
        "A) Master Pattabhi Jois of Ashtanga Yoga\n"
        "B) Catholic priest Ignatius Loyola\n"
        "C) Pattabhi's teacher - Krishnamacharya",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q6

# Q7
async def yoga_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q6'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="q7_A"),
         InlineKeyboardButton("B", callback_data="q7_B"),
         InlineKeyboardButton("C", callback_data="q7_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>7. Was there a word 'meditation' in Eastern traditions?</b>\n\n"
        "A) Yes\n"
        "B) No\n"
        "C) Information is still unknown",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q7

# Q8
async def yoga_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q7'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="q8_A"),
         InlineKeyboardButton("B", callback_data="q8_B"),
         InlineKeyboardButton("C", callback_data="q8_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>8. Which of these is NOT true?</b>\n\n"
        "A) In Eastern lineages, meditation was a part given to all students after several years of Hatha yoga training\n"
        "B) 'Meditation' in Eastern lineages was called 'Raja Yoga' – the royal practice, the crown of yoga\n"
        "C) There are Buddhist lineages where meditation is practiced immediately",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q8

# Q9
async def yoga_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q8'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="q9_A"),
         InlineKeyboardButton("B", callback_data="q9_B"),
         InlineKeyboardButton("C", callback_data="q9_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>9. In our work, 'meditation' is:</b>\n\n"
        "A) The goal\n"
        "B) The result\n"
        "C) A separate practice",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q9

async def yoga_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    context.user_data['q9'] = query.data.split('_')[1]
    l=len(context.user_data)
    questions = {
        'q1': {
            'A': 'Since ancient times, as soon as yoga appeared',
            'B': 'When yoga began to be popularized in India',
            'C': 'In the last century, when yoga from India arrived in America and began to gain popularity there'
        },
        'q2': {
            'A': 'Because the practice of yogis had greatly declined and was no longer effective',
            'B': 'Because the masters understood very well what was needed for Western people with their pace and rhythm of life',
            'C': 'Because such adaptation is safer and more effective than the traditional approach'
        },
        'q3': {
            'A': 'A spiritual tool closely connected with Hinduism or Buddhism',
            'B': 'A practical tool for psychophysical adaptation and mastering control over perception',
            'C': 'A tool to make the body invincible, beautiful, and healthy'
        },
        'q4': {
            'A': 'What was easier to sell',
            'B': 'What was more effective and healthier for the body',
            'C': 'What provided more spiritual development'
        },
        'q5': {
            'A': 'Yoga gymnastics practice in India is still used to train Indian special forces',
            'B': 'In martial clan lines of China, Korea, and Vietnam, yoga gymnastics was a tool for rapid training of body and psyche',
            'C': 'Yoga gymnastics was practiced only by religious persons'
        },
        'q6': {
            'A': 'Master Pattabhi Jois of Ashtanga Yoga',
            'B': 'Catholic priest Ignatius Loyola',
            'C': "Pattabhi's teacher - Krishnamacharya"
        },
        'q7': {
            'A': 'Yes',
            'B': 'No',
            'C': 'Information is still unknown'
        },
        'q8': {
            'A': 'In Eastern lineages, meditation was a part given to all students after several years of Hatha yoga training',
            'B': "'Meditation' in Eastern lineages was called 'Raja Yoga' – the royal practice, the crown of yoga", 
            'C': 'There are Buddhist lineages where meditation is practiced immediately'
        },
        'q9': {
            'A': 'The goal',
            'B': 'The result',
            'C': 'A separate practice'
        }
    }

    correct_answers = {
        'q1': 'C',
        'q2': 'B',
        'q3': 'B',
        'q4': 'A',
        'q5': 'C',
        'q6': 'B',
        'q7': 'B',
        'q8': 'A',
        'q9': 'B'
    }
    answer_letters = {'A': 'A', 'B': 'B', 'C': 'C'}
    explanations = {
        'q1': "Correct: C. Yoga became widely associated with spiritual practice and meditation in the last century, especially after its popularization in America. (Reference: The Heart of Yoga, Introduction)",
        'q2': "Correct: B. Eastern masters adapted yoga for Westerners, understanding their lifestyle and needs. (Reference: Light on Yoga, Preface)",
        'q3': "Correct: B. Yoga is primarily a tool for psychophysical adaptation and self-mastery. (Reference: The Heart of Yoga, Chapter 2)",
        'q4': "Correct: A. The commercialization of yoga in the West led to changes in its original principles. (Reference: Yoga Body by Mark Singleton)",
        'q5': "Correct: C. Yoga gymnastics was not practiced only by religious persons. (Reference: Light on Yoga, History section)",
        'q6': "Correct: B. The term 'meditato' was created by Ignatius Loyola, not by yoga masters. (Reference: Meditation: The First and Last Freedom by Osho)",
        'q7': "Correct: B. The word 'meditation' did not exist in Eastern traditions; other terms were used. (Reference: The Heart of Yoga, Chapter 5)",
        'q8': "Correct: A. In Eastern lineages, meditation was taught after years of Hatha yoga training. (Reference: Light on Yoga, Raja Yoga section)",
        'q9': "Correct: B. In modern yoga, meditation is considered the result of practice, not just a separate goal. (Reference: The Heart of Yoga, Chapter 6)"
    }
    score = 0
    results = []
    for q in [f'q{i}' for i in range(1, l+1)]:
        us_ans = context.user_data[q]
        cor_ans = correct_answers[q]
        if us_ans == cor_ans:
            score += 1
            correct = "✅"
        else:
            correct = "❌"
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Your answer: {answer_letters[us_ans]}) {questions[q][us_ans]} {correct}\n"
            f"☑️ Correct answer: {answer_letters[cor_ans]}) {questions[q][cor_ans]}\n"
            f"📘 Explanation: {explanations[q]}\n\n"
        )
    if score == 2:
        result_message = "2 in the diary, call your mom to school!\n"
    elif score == l:
        result_message = "Congratulations, you are a yoga honors student!\n"
    else:
        result_message = "You're almost there, practice a bit more!\n"
    await query.message.reply_text(
        "Thank you for your answers!" + "\n" + result_message + f"Here are your results: {score}/{l}" + "\n\n" + "\n".join(results), parse_mode="HTML"
    )
    return ConversationHandler.END

async def start_history(update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['correct_order']=HISTORY
    shuffled=HISTORY[:]
    random.shuffle(shuffled)
    context.user_data['remaining']=shuffled
    context.user_data['current_order']=[]
    await send_message_history(update, context)

async def send_message_history(update_or_query, context):
    remaining=context.user_data['remaining']
    current_order=context.user_data['current_order']
    keyboard=[
        [InlineKeyboardButton(text=statement, callback_data=f"choose_{statement}")]  for statement in context.user_data['remaining']
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🧩 Click the statements in the correct order:\n\n"
    statements = "<u>🟢 Remaining:</u>\n" + "\n".join(f"<b>▪️ {s}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for s in remaining)
    if current_order:
        text += "<u>⚪️ Your selection:</u>\n" + "\n".join(f"<b>▪️ {s}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for s in current_order) + "\n\n"
    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(text+statements, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update_or_query.edit_message_text(text+statements, reply_markup=reply_markup, parse_mode="HTML")

async def handle_choice_history(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current=context.user_data['current_order'].copy()
    #save selection
    reply = query.data.split('_')[1]
    context.user_data['current_order'].append(reply)

    #check before remove !!
    if reply not in context.user_data['remaining']:
        return
    #remove from list of options
    context.user_data['remaining'].remove(reply)

    #if all tapped check the answer
    l=len(HISTORY)
    score=0
    correct=[]
    if not context.user_data['remaining']:
        for i in range (0, l):
            if HISTORY[i]==context.user_data['current_order'][i]:
                score+=1
                correct.append("✅")
            else:
                correct.append("❌")
        if score == 2:
            result_message="2 in the diary, call your mom to school!\n"
        elif score == l:
            result_message= "Congratulations, you are a yoga honors student!\n"
        else:
            result_message= "You're almost there, practice a bit more!\n"
        await query.message.edit_text(
            "Thank you for your answers!" + "\n" +result_message+
            f"Here is your result: {score}/{l}" + "\n\n" + 
            f"<u>⚪️ Your selection:</u>\n" +
            "\n".join(f"<b>▪️ {s}{correct[i]}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for i, s in enumerate(current)) +
            "\n\n<u>🟢 Correct order:</u>\n" +
            "\n".join([f"<b>▪️ {s}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for s in HISTORY]),
            parse_mode="HTML"
        )
    else:
        await send_message_history(query, context)
    

 # === /broadcast handling (admin only, for example) ===
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 512911472:
        await update.message.reply_text("Ця команда тільки для адміністратора.")
        return
    
    text = " ".join(context.args) or "Тестове повідомлення 📨"

    # replace \n with actual newline
    text = text.replace("\\n", "\n")

    all_users = get_all_users()
    count = 0
    for user_id in all_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
            count += 1
        except Exception as e:
            print(f"Couldn't send the message {user_id}: {e}")
    await update.message.reply_text(f"The message has been sent to {count} users ✅")
async def detection_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧘🏼‍♀️ Send a photo to detect the yoga pose!\n\n" \
                                    "✅ If you are done and you want to finish the detection send /end")
    return D_Q1
async def detection_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['photo']=update.message.photo
    l=len(context.user_data['photo'])
    pose_file_id=context.user_data['photo'][l-1].file_id
    pose_file=await context.bot.get_file(pose_file_id) #await because bot wait's for a file loading from server
    await pose_file.download_to_drive("user_photo.jpg") #await because bot wait's for a network request
    pose_processed=process_image("user_photo.jpg")
    # result=detect_pose(pose_processed)
    result=detect_pose_ai(pose_processed)
    await update.message.reply_text(result)
async def detection_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Detection is finished.✅")
    return ConversationHandler.END


if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    # Conversation handler for test
    test_conv = ConversationHandler(
        entry_points=[CommandHandler('test', test_start)],
        states={
            Q1: [CallbackQueryHandler(test_q2, pattern='^q1_')],
            Q2: [CallbackQueryHandler(test_q3, pattern='^q2_')],
            Q3: [CallbackQueryHandler(test_q4, pattern='^q3_')],
            Q4: [CallbackQueryHandler(test_q5_prompt, pattern='^q4_')], 
            Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, test_q5)],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )

    # Conversation handler for exam
    exam_conv = ConversationHandler(
        entry_points=[CommandHandler('exam', exam_start)],
        states={
            T1_Q1: [CallbackQueryHandler(exam_q2, pattern='^q1_')],
            T1_Q2: [CallbackQueryHandler(exam_q3, pattern='^q2_')],
            T1_Q3: [CallbackQueryHandler(exam_q4, pattern='^q3_')],
            T1_Q4: [CallbackQueryHandler(exam_q5, pattern='^q4_')],
            T1_Q5: [CallbackQueryHandler(exam_q6, pattern='^q5_')],
            T1_Q6: [CallbackQueryHandler(exam_q7, pattern='^q6_')],
            T1_Q7: [CallbackQueryHandler(exam_q8, pattern='^q7_')], 
            T1_Q8: [CallbackQueryHandler(exam_q9, pattern='^q8_')],
            T1_Q9: [CallbackQueryHandler(exam_q10, pattern='^q9_')],
            T1_Q10: [CallbackQueryHandler(exam_end, pattern='^q10_')], 
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )
    # Conversation handler for culture test
    culture_conv = ConversationHandler(
        entry_points=[CommandHandler('culture', culture_start)],
        states={
            C_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q2)],
            C_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q3)],
            C_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q4)],
            C_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q5)],
            C_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q6)],
            C_Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_end)],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )
    # Conversation handler for practice test
    practice_conv = ConversationHandler(
        entry_points=[CommandHandler('practice', practice_start)],
        states={
            F_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q2)],
            F_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q3)],
            F_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q4)],
            F_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q5)],
            F_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q6)],
            F_Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q7)],
            F_Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q8)],
            F_Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q9)],
            F_Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_q10)],
            F_Q10: [MessageHandler(filters.TEXT & ~filters.COMMAND, practice_end)],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )
    # Conversation handler for pain test
    pain_conv = ConversationHandler(
        entry_points=[CommandHandler('pain', pain_start)],
        states={
            P_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q2)],
            P_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q3)],
            P_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q4)],
            P_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q5)],
            P_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q6)],
            P_Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q7)],
            P_Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q8)],
            P_Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q9)],
            P_Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q10)],
            P_Q10: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q11)],
            P_Q11: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q12)],
            P_Q12: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_end)],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )
    # Conversation handler for yoga test
    yoga_conv = ConversationHandler(
        entry_points=[CommandHandler('yoga', yoga_start)],
        states={
            T2_Q1: [CallbackQueryHandler(yoga_q2, pattern='^q1_')],
            T2_Q2: [CallbackQueryHandler(yoga_q3, pattern='^q2_')],
            T2_Q3: [CallbackQueryHandler(yoga_q4, pattern='^q3_')],
            T2_Q4: [CallbackQueryHandler(yoga_q5, pattern='^q4_')], 
            T2_Q5: [CallbackQueryHandler(yoga_q6, pattern='^q5_')],
            T2_Q6: [CallbackQueryHandler(yoga_q7, pattern='^q6_')],
            T2_Q7: [CallbackQueryHandler(yoga_q8, pattern='^q7_')],
            T2_Q8: [CallbackQueryHandler(yoga_q9, pattern='^q8_')], 
            T2_Q9: [CallbackQueryHandler(yoga_end, pattern='^q9_')], 
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )
    #Conversation handler for pose detection
    pose_conv=ConversationHandler(
        entry_points=[CommandHandler('detect', detection_start)],
        states={
            D_Q1:[MessageHandler(filters.PHOTO & ~filters.COMMAND, detection_process)]
        },
        fallbacks=[CommandHandler('end', detection_end)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(test_conv)
    app.add_handler(exam_conv)
    app.add_handler(culture_conv)
    app.add_handler(practice_conv)
    app.add_handler(CommandHandler("broadcast", broadcast))  # /broadcast Hello everyone!
    app.add_handler(pain_conv)
    app.add_handler(yoga_conv)
    app.add_handler(CommandHandler("history", start_history))
    app.add_handler(CallbackQueryHandler(handle_choice_history, pattern="^choose_"))
    app.add_handler(pose_conv)

    print("Bot started")
    app.run_polling()
