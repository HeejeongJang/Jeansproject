{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import logging\n",
    "from telegram import ForceReply ,ReplyKeyboardRemove, Update, ReplyKeyboardMarkup\n",
    "from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler\n",
    "\n",
    "import pandas as pd\n",
    "\n",
    "import time\n",
    "from telegram import ChatAction\n",
    "from telegram import InlineKeyboardButton, InlineKeyboardMarkup\n",
    "from telegram.ext import Updater\n",
    "from telegram.ext import CommandHandler, CallbackQueryHandler\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import cx_Oracle\n",
    "\n",
    "from sqlalchemy.orm import sessionmaker\n",
    "from sqlalchemy import *\n",
    "\n",
    "from telegram import InlineKeyboardButton as BT\n",
    "from telegram import InlineKeyboardMarkup as MU\n",
    "\n",
    "import findpolicy\n",
    "\n",
    "from konlpy.tag import Mecab \n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "# mecab 실행\n",
    "\n",
    "mecab = Mecab(dicpath=r\"C:\\Mecab\\mecab-ko-dic\") # dictation path 설정 / mecab-ko-dic이 mecab의 단어사전임"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 오라클 엔진 가동 - 엔진만 가동하면 table은 불러올 수 있음.\n",
    "engine = create_engine('oracle://c##biganalysis:1234@localhost:1521/orcl')\n",
    "\n",
    "# Session을 실행시켜야 쿼리 실행 가능\n",
    "\n",
    "Session = sessionmaker()\n",
    "Session.configure(bind=engine)\n",
    "session = Session()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import telegram\n",
    "\n",
    "token = '2133514246:AAGGBP1skx5GyvRBW9AzL7_QKe87-JdZIrw'\n",
    "id = '2033550924'\n",
    "mc = '2033550924'# ID\n",
    "\n",
    "bot = telegram.Bot(token = token)\n",
    "updates = bot.getUpdates()\n",
    "for u in updates:\n",
    "    print(u.message)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#버튼 목록\n",
    "\n",
    "# 상담글 저장 동의 버튼\n",
    "agree1_first = BT(text = '예', callback_data = '예')\n",
    "agree2_first = BT(text = '아니오', callback_data = '아니오')\n",
    "agree_mu_first = MU(inline_keyboard = [[agree1_first, agree2_first]])\n",
    "\n",
    "# 개인정보 동의 버튼\n",
    "agree1 = BT(text = '동의', callback_data = '동의')\n",
    "agree2 = BT(text = '비동의', callback_data = '비동의')\n",
    "agree_mu = MU(inline_keyboard = [[agree1, agree2]])\n",
    "\n",
    "#자격요건 - 나이\n",
    "age1 = BT(text = '15 미만', callback_data = '00-15')\n",
    "age2 = BT(text = '15-18', callback_data = '15-18')\n",
    "age3 = BT(text = '19-24', callback_data = '19-24')\n",
    "age4 = BT(text = '25-34', callback_data = '25-34')\n",
    "age5 = BT(text = '35-39', callback_data = '35-39')\n",
    "age6 = BT(text = '40이상', callback_data = '40~99')\n",
    "age_mu = MU(inline_keyboard = [[age1, age2, age3],[age4, age5, age6]])\n",
    "\n",
    "#자격요건 - 지역\n",
    "reg1 = BT(text = '강원도', callback_data = '강원도')\n",
    "reg2 = BT(text = '경기도', callback_data = '경기도')\n",
    "reg3= BT(text = '경상남도', callback_data = '경상남도')\n",
    "reg4 = BT(text = '경상북도', callback_data = '경상북도')\n",
    "reg5 = BT(text = '광주광역시', callback_data = '광주광역시')\n",
    "reg6 = BT(text = '대구광역시', callback_data = '대구광역시')\n",
    "reg7 = BT(text = '대전광역시', callback_data = '대전광역시')\n",
    "reg8 = BT(text = '부산광역시', callback_data = '부산광역시')\n",
    "reg9 = BT(text = '서울특별시', callback_data = '서울특별시')\n",
    "reg10 = BT(text = '세종시', callback_data = '세종시')\n",
    "reg11 = BT(text = '울산광역시', callback_data = '울산광역시')\n",
    "reg12 = BT(text = '인천광역시', callback_data = '인천광역시')\n",
    "reg13 = BT(text = '전라남도', callback_data = '전라남도')\n",
    "reg14 = BT(text = '전라북도', callback_data = '전라북도')\n",
    "reg15 = BT(text = '제주도', callback_data = '제주도')\n",
    "reg16 = BT(text = '충청남도', callback_data = '충청남도')\n",
    "reg17 = BT(text = '충청북도', callback_data = '충청북도')\n",
    "reg18 = BT(text = '전국', callback_data = '전국')\n",
    "reg_mu = MU(inline_keyboard = [[reg1, reg2,reg3],\n",
    "                              [reg4, reg5,reg6],\n",
    "                              [reg7, reg8,reg9],\n",
    "                              [reg10, reg11,reg12],\n",
    "                              [reg13, reg14,reg15],\n",
    "                              [reg16, reg17,reg18]])\n",
    "\n",
    "# 자격요건 - 학력\n",
    "edu1 = BT(text = '고교 재학', callback_data = '고교 재학')\n",
    "edu2 = BT(text = '고졸', callback_data = '고졸')\n",
    "edu3 = BT(text = '대학 재학', callback_data = '대학 재학')\n",
    "edu4 = BT(text = '대졸', callback_data = '대졸')\n",
    "edu5 = BT(text = '대학원 재학', callback_data = '대학원 재학')\n",
    "edu6 = BT(text = '대학원 졸업', callback_data = '대학원 졸업')\n",
    "edu7 = BT(text = '제한없음', callback_data = '제한없음')\n",
    "edu_mu = MU(inline_keyboard = [[edu1, edu2, edu3],\n",
    "                              [edu4, edu5, edu6],\n",
    "                              [edu7]])\n",
    "\n",
    "# 자격요건 - 취업여부\n",
    "work1 = BT(text = '미취업자', callback_data = '미취업자')\n",
    "work2 = BT(text = '재직자', callback_data = '재직자')\n",
    "work3 = BT(text = '제한없음', callback_data = '제한없음')\n",
    "work_mu = MU(inline_keyboard = [[work1, work2, work3]]) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "policy = pd.read_csv('using_data/policy_content.csv', encoding = 'euc-kr')\n",
    "condition = pd.read_csv('using_data/policy_condition_real_final.csv', encoding = 'euc-kr')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "bot = telegram.Bot(token = token)\n",
    "updates = bot.getUpdates()\n",
    "\n",
    "def start(update, context):\n",
    "    bot.sendMessage(chat_id=update.effective_chat.id, text='안녕하세요. 당신에게 딱 맞는 취업정책! 청바지👖입니다! \\n취업 정책 찾기 힘드셨나요? \\n자격 요건 알아보기 번거로우셨나요? \\n그럼 잘 오셨어요. \\n저희가 찾아드릴게요 😎')\n",
    "    bot.sendMessage(chat_id=update.effective_chat.id, text=\"추천에 앞서 저희가 더 나은 서비스로 발전하기 위해 당신의 상담글을 저장하고 싶습니다. \\n저희 서비스는 철저한 익명이 보장됩니다.\\n/agree 버튼을 눌러주세요~\")\n",
    "\n",
    "updater = Updater(token=token, use_context=True) \n",
    "dispatcher = updater.dispatcher \n",
    "\n",
    "def btn_agree_first(update, context):\n",
    "    agree_markup = agree_mu_first # make markup\n",
    "    update.message.reply_text(\"상담글 저장에 동의하십니까?\", reply_markup=agree_markup)\n",
    "\n",
    "get_handler_first = CommandHandler('agree', btn_agree_first)\n",
    "updater.dispatcher.add_handler(get_handler_first)                               \n",
    "        \n",
    "###########\n",
    "\n",
    "# def Question(update, context): \n",
    "#     context.bot.send_message(chat_id=update.effective_chat.id, text= '취업 관련 고민을 적어주세요!')\n",
    "\n",
    "def echo(update, context): \n",
    "    your_policy = findpolicy.find_your_policy(update.message.text).reset_index(drop = True)\n",
    "    text1 = '당신에게 추천드리는 정책은..\\n「{}」 입니다!\\n\\n● 정책 내용: \\n{} \\n\\n● 지원 상세내용: \\n{} \\n\\n↓정책명을 검색해보세요! \\n{}'.format(your_policy.iloc[0,1], your_policy.iloc[0,2], your_policy.iloc[0,3], your_policy.iloc[0,4])\n",
    "    text2 = '혹시 마음에 들지 않으시다면 그 외의 추천 정책입니다! \\n\\n◆ 2순위:「{}」 \\n정책 검색 → {} \\n\\n◆ 3순위:「{}」 \\n정책 검색 → {} \\n\\n◆ 4순위:「{}」 \\n정책 검색 → {} \\n\\n◆ 5순위:「{}」 \\n정책 검색 → {}'.format(your_policy.iloc[1,1],your_policy.iloc[1,4],your_policy.iloc[2,1],your_policy.iloc[2,4],your_policy.iloc[3,1],your_policy.iloc[3,4],your_policy.iloc[4,1],your_policy.iloc[4,4])\n",
    "    text3 = '도움이 되셨나요?😊 \\n추천된 정책의 지원대상인지 간단히 확인해드릴 수 있어요.\\n확인을 원하시면 /info 를 클릭해주세요. \\n약간의 개인정보를 요구합니다.'\n",
    "    context.bot.send_message(chat_id=update.effective_chat.id, text = text1)\n",
    "    context.bot.send_message(chat_id=update.effective_chat.id, text = text2)\n",
    "    context.bot.send_message(chat_id=update.effective_chat.id, text = text3)\n",
    "    \n",
    "    query = \"insert into text_table(test) values('{}')\".format(update.message.text)\n",
    "\n",
    "    session.execute(query)\n",
    "    session.execute(\"commit\")\n",
    "\n",
    "################################\n",
    "    \n",
    "def btn_agree(update, context):\n",
    "    agree_markup = agree_mu # make markup\n",
    "    update.message.reply_text(\"개인정보 수집에 동의하십니까?\", reply_markup=agree_markup)\n",
    "    \n",
    "def callback_get(update, context):\n",
    "    \n",
    "    if update.callback_query.data == '예' :\n",
    "        context.bot.edit_message_text(text=\"동의하셨습니다. 취업 관련 고민을 적어주세요!\",\n",
    "                                      chat_id=update.callback_query.message.chat_id,\n",
    "                                      message_id=update.callback_query.message.message_id)\n",
    "    \n",
    "    if update.callback_query.data == '아니오' :\n",
    "        context.bot.edit_message_text(text=\"비동의하셨습니다.. 저희 서비스는 상담글 수집을 원하지 않으시다면 아직 이용하시기 힘드십니다.. \\n 이용을 원하신다면 다시 /agree 를 선택하셔 동의해주시기 바랍니다.\",\n",
    "                                      chat_id=update.callback_query.message.chat_id,\n",
    "                                      message_id=update.callback_query.message.message_id)\n",
    "    \n",
    "    \n",
    "    # 동의 -> 나이\n",
    "    agree_list = ['동의','비동의']\n",
    "    if update.callback_query.data in agree_list :\n",
    "        context.bot.edit_message_text(text=\"{}를 선택하셨습니다\".format(update.callback_query.data),\n",
    "                                      chat_id=update.callback_query.message.chat_id,\n",
    "                                      message_id=update.callback_query.message.message_id)\n",
    "        context.bot.sendMessage(mc, '나이를 선택하세요.', reply_markup = age_mu)\n",
    "    \n",
    "    # 나이 -> 지역\n",
    "    age_list = ['00-15', '15-18', '19-24', '25-34', '35-39', '40~99']\n",
    "    if update.callback_query.data in age_list:\n",
    "        context.bot.edit_message_text(text=\"{}\".format(update.callback_query.data),\n",
    "                                      chat_id=update.callback_query.message.chat_id,\n",
    "                                      message_id=update.callback_query.message.message_id)\n",
    "        context.bot.sendMessage(mc, '지역을 선택하세요.', reply_markup = reg_mu)\n",
    "\n",
    "    \n",
    "    # 지역 -> 최종학력\n",
    "    reg_list = ['강원도','경기도','경상남도','경상북도','광주광역시','대구광역시','대전광역시','부산광역시','서울특별시',\n",
    "                '세종시','울산광역시','인천광역시','전라남도','전라북도','제주도','충청남도','충청북도','전국']\n",
    "    if update.callback_query.data in reg_list:\n",
    "        context.bot.edit_message_text(text=\"{}\".format(update.callback_query.data),\n",
    "                                      chat_id=update.callback_query.message.chat_id,\n",
    "                                      message_id=update.callback_query.message.message_id)\n",
    "        context.bot.sendMessage(mc, '최종학력을 선택하세요', reply_markup = edu_mu)\n",
    "\n",
    "    \n",
    "    # 최종학력 -> 취업여부\n",
    "    edu_list = ['고교 재학','고졸', '대학 재학','대졸', '대학원 재학', '대학원 졸업', '제한없음']\n",
    "    if update.callback_query.data in edu_list:\n",
    "        context.bot.edit_message_text(text=\"{}\".format(update.callback_query.data),\n",
    "                                      chat_id=update.callback_query.message.chat_id,\n",
    "                                      message_id=update.callback_query.message.message_id)\n",
    "        context.bot.sendMessage(mc, '취업여부를 선택하세요.', reply_markup = work_mu)\n",
    "\n",
    "\n",
    "    #취업여부 -> 텍스트 입력\n",
    "    work_list = ['미취업자', '재직자', '제한없음']\n",
    "    if update.callback_query.data in work_list:\n",
    "        context.bot.edit_message_text(text=\"{}\".format(update.callback_query.data),\n",
    "                                      chat_id=update.callback_query.message.chat_id,\n",
    "                                      message_id=update.callback_query.message.message_id)\n",
    "        context.bot.sendMessage(mc, \"추천된 정책의 지원대상인지 확인하고 싶으시다면 /condition 을 클릭하세요!\")\n",
    "    \n",
    "    if update.callback_query.data in age_list:\n",
    "        session.execute(\"UPDATE test2 SET age = '{}'\".format(update.callback_query.data))\n",
    "        session.execute(\"commit\")\n",
    "        \n",
    "    if update.callback_query.data in reg_list:\n",
    "        session.execute(\"UPDATE test2 SET region = '{}'\".format(update.callback_query.data))\n",
    "        session.execute(\"commit\")\n",
    "        \n",
    "    if update.callback_query.data in edu_list:\n",
    "        session.execute(\"UPDATE test2 SET edu = '{}'\".format(update.callback_query.data))\n",
    "        session.execute(\"commit\")\n",
    "        \n",
    "    if update.callback_query.data in work_list:\n",
    "        session.execute(\"UPDATE test2 SET work = '{}'\".format(update.callback_query.data))\n",
    "        session.execute(\"commit\")\n",
    "\n",
    "def check_condition(update, context): \n",
    "    your_policy = findpolicy.find_your_policy(update.message.text).reset_index(drop = True)\n",
    "    your_policy = condition.loc[condition['index'] == your_policy['index'][0]]\n",
    "    df_list = list(pd.read_sql('select * from test2', engine).iloc[0])       # 사용자 자격요건\n",
    "    temp_list = list(your_policy.iloc[0])   # 추천된 정책 5개 중 1위\n",
    "\n",
    "    if (int(df_list[0][:2]) >= temp_list[2] and int(df_list[0][-2:]) <= temp_list[3])\\\n",
    "        &(df_list[1] == temp_list[4] or temp_list[4] == '전국')\\\n",
    "        &(df_list[2] == temp_list[5] or temp_list[5] == '제한없음')\\\n",
    "        &(df_list[3] == temp_list[7] or temp_list[7] == '제한없음'):\n",
    "        context.bot.send_message(chat_id=update.effective_chat.id, text= '추천 정책의 지원대상입니다~🥳 \\n다만 입력한 정보외의 추가적인 제한 사항이 있을 수 있으니 해당 페이지 확인을 부탁드립니다~👌')\n",
    "    else:\n",
    "        context.bot.send_message(chat_id=update.effective_chat.id, text= '아쉽게도 지원대상이 아니세요😭')\n",
    "\n",
    "dispatcher.add_handler(CommandHandler(\"start\", start))\n",
    "        \n",
    "echo_handler = MessageHandler(Filters.text & (~Filters.command), echo) \n",
    "dispatcher.add_handler(echo_handler)\n",
    "\n",
    "get_handler = CommandHandler('info', btn_agree)\n",
    "updater.dispatcher.add_handler(get_handler)                             \n",
    "updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))\n",
    "\n",
    "dispatcher.add_handler(CommandHandler(\"condition\", check_condition))\n",
    "\n",
    "def filtering(인자):\n",
    "    df_list = list(df.iloc[0])       # 사용자 자격요건\n",
    "    temp_list = list(temp.iloc[3])   # 추천된 정책 5개 중 1위\n",
    "\n",
    "    if (int(df_list[0][:2]) >= temp_list[2] and int(df_list[0][-2:]) <= temp_list[3])\\\n",
    "        &(df_list[1] == temp_list[4] or temp_list[4] == '전국')\\\n",
    "        &(df_list[2] == temp_list[5] or temp_list[5] == '제한없음')\\\n",
    "        &(df_list[3] == temp_list[7] or temp_list[7] == '제한없음'):\n",
    "        print('가능') # sendmessage로 수정\n",
    "    else:\n",
    "        print('불가능') # sendmessage로 수정\n",
    "\n",
    "updater.start_polling() \n",
    "updater.idle()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
