# -*- coding: utf-8 -*- 

############################ PC Ver. 25 (2020. 7. 4.) ##################################
#########################################################################################
#########################################################################################
#########################################################################################
###### 개발환경 : python 3.7.3														######
######		   discord = 1.0.1														######
######		   discord.py = 1.3.3													######
######		   gtts = 2.0.3															######
###### 모듈설치 : pip install setuptools --upgrade									######
######		   pip install websockets==6.0											######
######		   pip install discord													######
######		   pip install discord.py[voice]										######
######		   pip install gtts														######
######		   pip install pyssml													######
######		   pip install pywin32													######
######		   pip install pyinstaller												######
######		   pip install oauth2client												######
######		   pip install gspread													######
######		   pip install PyOpenSSL												######
#########################################################################################
#########################################################################################
#########################################################################################


import sys
import os
import win32con
import win32api
import win32gui
import asyncio
import discord
import datetime
import random
import re
import time
import logging
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from gtts import gTTS
import gspread #정산
from oauth2client.service_account import ServiceAccountCredentials #정산
from io import StringIO
import urllib.request
from math import ceil, floor

log_stream = StringIO()    
logging.basicConfig(stream=log_stream, level=logging.WARNING)

if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')

##################### 로깅 ###########################
#ilsanglog = logging.getLogger('discord')
#ilsanglog.setLevel(level = logging.WARNING)
#handler = logging.FileHandler(filename = 'discord.log', encoding='utf-8',mode='a')
#handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
#ilsanglog.addHandler(handler)
#####################################################

basicSetting = []
bossData = []
fixed_bossData = []

bossNum = 0
fixed_bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0
LoadChk = 0

bossTime = []
tmp_bossTime = []

fixed_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
fixed_bossFlag = []
fixed_bossFlag0 = []
bossMungFlag = []
bossMungCnt = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []

katalkData = []
InitkatalkData = []
indexBossname = []
FixedBossDateData = []
indexFixedBossname = []

client = discord.Client()
client = commands.Bot(command_prefix="", help_command = None, description='일상디코봇')

#기본 설정 호출 및 초기 설정 셋팅
def init():
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt

	global voice_client1
	
	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	global LoadChk

	global katalkData
	global InitkatalkData
	global indexBossname
	global indexFixedBossname
	global FixedBossDateData

	global endTime

	global gc #정산
	global credentials #정산

	global regenembed
	global command
	global kill_Data
	global kill_Time
	global item_Data

	global tmp_racing_unit
	
	command = []
	tmp_bossData = []
	tmp_fixed_bossData = []
	tmp_commandData = []
	katalkData = []
	InitkatalkData = []
	indexBossname = []
	FixedBossDateData = []
	indexFixedBossname = []
	kill_Data = {}
	tmp_kill_Data = []
	item_Data = {}
	tmp_item_Data = []
	f = []
	fb = []
	fk = []
	fc = []
	fi = []
	tmp_racing_unit = []

	inidata = open('test_setting.ini', 'r', encoding = 'utf-8')
	boss_inidata = open('boss.ini', 'r', encoding = 'utf-8')
	fixed_initdata = open('fixed_boss.ini', 'r', encoding = 'utf-8')
	command_inidata = open('command.ini', 'r', encoding = 'utf-8')
	kill_inidata = open('kill_list.ini', 'r', encoding = 'utf-8')
	item_inidata = open('item_list.ini', 'r', encoding = 'utf-8')

	inputData = inidata.readlines()
	boss_inputData = boss_inidata.readlines()
	fixed_inputData = fixed_initdata.readlines()
	command_inputData = command_inidata.readlines()
	kill_inputData = kill_inidata.readlines()
	item_inputData = item_inidata.readlines()

	for i in range(len(inputData)):
		InitkatalkData.append(inputData[i])

	for i in range(len(boss_inputData)):
		katalkData.append(boss_inputData[i])

	for i in range(len(fixed_inputData)):
		FixedBossDateData.append(fixed_inputData[i])

	del(boss_inputData[0])
	del(fixed_inputData[0])
	del(command_inputData[0])
	del(kill_inputData[0])
	del(item_inputData[0])

	index = 0
	index_fixed = 0

	for value in katalkData:
		if value.find('bossname') != -1:
			indexBossname.append(index)
		index = index + 1

	for value in FixedBossDateData:
		if value.find('bossname') != -1:
			indexFixedBossname.append(index_fixed)
		index_fixed = index_fixed + 1
	
	for i in range(inputData.count('\n')):
		inputData.remove('\n')

	for i in range(boss_inputData.count('\n')):
		boss_inputData.remove('\n')

	for i in range(fixed_inputData.count('\n')):
		fixed_inputData.remove('\n')

	for i in range(command_inputData.count('\n')):
		command_inputData.remove('\n')

	for i in range(kill_inputData.count('\n')):
		kill_inputData.remove('\n')

	for i in range(item_inputData.count('\n')):
		item_inputData.remove('\n')
	
	############## 보탐봇 초기 설정 리스트 #####################
	basicSetting.append(inputData[0][12:])     #basicSetting[0] : bot_token
	basicSetting.append(inputData[10][15:])     #basicSetting[1] : before_alert
	basicSetting.append(inputData[12][10:])     #basicSetting[2] : mungChk
	basicSetting.append(inputData[11][16:])     #basicSetting[3] : before_alert1
	basicSetting.append(inputData[15][14:16])  #basicSetting[4] : restarttime 시
	basicSetting.append(inputData[15][17:])    #basicSetting[5] : restarttime 분
	basicSetting.append(inputData[3][15:])     #basicSetting[6] : voice채널 ID
	basicSetting.append(inputData[4][14:])     #basicSetting[7] : text채널 ID
	basicSetting.append(inputData[1][16:])     #basicSetting[8] : 카톡챗방명
	basicSetting.append(inputData[2][13:])     #basicSetting[9] : 카톡챗On/Off
	basicSetting.append(inputData[5][16:])     #basicSetting[10] : 사다리 채널 ID
	basicSetting.append(inputData[14][14:])    #basicSetting[11] : !q 표시 보스 수
	basicSetting.append(inputData[16][16:])    #basicSetting[12] : restart 주기
	basicSetting.append(inputData[6][17:])     #basicSetting[13] : 정산 채널 ID
	basicSetting.append(inputData[17][12:])    #basicSetting[14] : 스프레드시트 파일 이름
	basicSetting.append(inputData[18][11:])    #basicSetting[15] : json 파일명
	basicSetting.append(inputData[19][12:])    #basicSetting[16] : 시트 이름
	basicSetting.append(inputData[20][12:])    #basicSetting[17] : 입력 셀
	basicSetting.append(inputData[21][13:])    #basicSetting[18] : 출력 셀
	basicSetting.append(inputData[13][13:])    #basicSetting[19] : 멍삭제횟수
	basicSetting.append(inputData[7][14:])     #basicSetting[20] : kill채널 ID
	basicSetting.append(inputData[8][16:])     #basicSetting[21] : racing채널 ID
	basicSetting.append(inputData[9][14:])     #basicSetting[22] : item채널 ID

	############## 보탐봇 명령어 리스트 #####################
	for i in range(len(command_inputData)):
		tmp_command = command_inputData[i][12:].rstrip('\n')
		fc = tmp_command.split(', ')
		command.append(fc)
		fc = []
		#command.append(command_inputData[i][12:].rstrip('\n'))     #command[0] ~ [28] : 명령어

	################## 척살 명단 ###########################
	for i in range(len(kill_inputData)):
		tmp_kill_Data.append(kill_inputData[i].rstrip('\n'))
		fk.append(tmp_kill_Data[i][:tmp_kill_Data[i].find(' ')])
		fk.append(tmp_kill_Data[i][tmp_kill_Data[i].find(' ')+1:])
		kill_Data[fk[0]] = int(fk[1])
		fk = []

	################## 아이템 목록 ###########################
	for i in range(len(item_inputData)):
		tmp_item_Data.append(item_inputData[i].rstrip('\n'))
		fi.append(tmp_item_Data[i][:tmp_item_Data[i].find(' ')])
		fi.append(tmp_item_Data[i][tmp_item_Data[i].find(' ')+1:])
		item_Data[fi[0]] = int(fi[1])
		fi = []

	tmp_killtime = datetime.datetime.now().replace(hour=int(5), minute=int(0), second = int(0))
	kill_Time = datetime.datetime.now()

	if tmp_killtime < kill_Time :
		kill_Time = tmp_killtime + datetime.timedelta(days=int(1))
	else:
		kill_Time = tmp_killtime

	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	if basicSetting[6] != "":
		basicSetting[6] = int(basicSetting[6])
		
	if basicSetting[7] != "":
		basicSetting[7] = int(basicSetting[7])

	if basicSetting[10] != "":
		basicSetting[10] = int(basicSetting[10])
		
	if basicSetting[13] != "":
		basicSetting[13] = int(basicSetting[13])

	if basicSetting[20] != "":
		basicSetting[20] = int(basicSetting[20])

	if basicSetting[21] != "":
		basicSetting[21] = int(basicSetting[21])

	if basicSetting[22] != "":
		basicSetting[22] = int(basicSetting[22])


	bossNum = int(len(boss_inputData)/6) 

	fixed_bossNum = int(len(fixed_inputData)/7) 

	tmp_now = datetime.datetime.now()
	
	if int(basicSetting[12]) == 0 :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		endTime = endTime + datetime.timedelta(days=int(1000))
	else :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		if endTime < tmp_now :			
			endTime = endTime + datetime.timedelta(days=int(basicSetting[12]))
		
	for i in range(bossNum):
		tmp_bossData.append(boss_inputData[i*6:i*6+6])
	
	for i in range(fixed_bossNum):
		tmp_fixed_bossData.append(fixed_inputData[i*7:i*7+7]) 

	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()

	for j in range(fixed_bossNum):
		for i in range(len(tmp_fixed_bossData[j])):
			tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()

	############## 일반보스 정보 리스트 #####################
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])		  #bossData[0] : 보스명
		f.append(tmp_bossData[j][1][10:tmp_len])  #bossData[1] : 시
		f.append(tmp_bossData[j][2][13:])		  #bossData[2] : 멍/미입력
		f.append(tmp_bossData[j][3][20:])		  #bossData[3] : 분전 알림멘트
		f.append(tmp_bossData[j][4][13:])		  #bossData[4] : 젠 알림멘트
		f.append(tmp_bossData[j][1][tmp_len+1:])  #bossData[5] : 분
		f.append(tmp_bossData[j][5][13:])		  #bossData[6] : 카톡On/Off		
		f.append('')							  #bossData[7] : 메세지
		bossData.append(f)
		f = []
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('99:99:99')
		tmp_bossDateString.append('9999-99-99')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)

	tmp_fixed_now = datetime.datetime.now()

	############## 고정보스 정보 리스트 #####################
	for j in range(fixed_bossNum):
		tmp_fixed_len = tmp_fixed_bossData[j][1].find(':')
		tmp_fixedGen_len = tmp_fixed_bossData[j][2].find(':')
		fb.append(tmp_fixed_bossData[j][0][11:])			      #fixed_bossData[0] : 보스명
		fb.append(tmp_fixed_bossData[j][1][11:tmp_fixed_len])     #fixed_bossData[1] : 시
		fb.append(tmp_fixed_bossData[j][1][tmp_fixed_len+1:])     #fixed_bossData[2] : 분
		fb.append(tmp_fixed_bossData[j][4][20:])			      #fixed_bossData[3] : 분전 알림멘트
		fb.append(tmp_fixed_bossData[j][5][13:])			      #fixed_bossData[4] : 젠 알림멘트
		fb.append(tmp_fixed_bossData[j][6][13:])			      #fixed_bossData[5] : 카톡On/Off		
		fb.append(tmp_fixed_bossData[j][2][12:tmp_fixedGen_len])  #fixed_bossData[6] : 젠주기-시
		fb.append(tmp_fixed_bossData[j][2][tmp_fixedGen_len+1:])  #fixed_bossData[7] : 젠주기-분
		fb.append(tmp_fixed_bossData[j][3][12:16])                #fixed_bossData[8] : 시작일-년	
		fb.append(tmp_fixed_bossData[j][3][17:19])                #fixed_bossData[9] : 시작일-월
		fb.append(tmp_fixed_bossData[j][3][20:22])                #fixed_bossData[10] : 시작일-일	
		fixed_bossData.append(fb)
		fb = []
		fixed_bossFlag.append(False)
		fixed_bossFlag0.append(False)
		fixed_bossTime.append(tmp_fixed_now.replace(year = int(fixed_bossData[j][8]), month = int(fixed_bossData[j][9]), day = int(fixed_bossData[j][10]), hour=int(fixed_bossData[j][1]), minute=int(fixed_bossData[j][2]), second = int(0)))
		if fixed_bossTime[j] < tmp_fixed_now :
			while fixed_bossTime[j] < tmp_fixed_now :
				fixed_bossTime[j] = fixed_bossTime[j] + datetime.timedelta(hours=int(fixed_bossData[j][6]), minutes=int(fixed_bossData[j][7]), seconds = int(0))

	################# 이모지 로드 ######################
	emo_inidata = open('emoji.ini', 'r', encoding = 'utf-8')
	emo_inputData = emo_inidata.readlines()
	emo_inidata.close()

	for i in range(len(emo_inputData)):
		tmp_emo = emo_inputData[i][8:].rstrip('\n')
		if tmp_emo != "":
			tmp_racing_unit.append(tmp_emo)

	inidata.close()
	boss_inidata.close()
	fixed_initdata.close()
	command_inidata.close()	
	kill_inidata.close()

	################# 리젠보스 시간 정렬 ######################
	regenData = []
	regenTime = []
	regenbossName = []
	outputTimeHour = []
	outputTimeMin = []

	for i in range(bossNum):
		if bossData[i][2] == "1":
			f.append(bossData[i][0] + "R")
		else:
			f.append(bossData[i][0])
		f.append(bossData[i][1] + bossData[i][5])
		regenData.append(f)
		regenTime.append(bossData[i][1] + bossData[i][5])
		f = []
		
	regenTime = sorted(list(set(regenTime)))
	
	for j in range(len(regenTime)):
		for i in range(len(regenData)):
			if regenTime[j] == regenData[i][1] :
				f.append(regenData[i][0])
		regenbossName.append(f)
		outputTimeHour.append(int(regenTime[j][:2]))
		outputTimeMin.append(int(regenTime[j][2:]))
		f = []

	regenembed = discord.Embed(
			title='----- 보스별 리스폰 시간-----',
			description= ' ')
	for i in range(len(regenTime)):
		if outputTimeMin[i] == 0 :
			regenembed.add_field(name=str(outputTimeHour[i]) + '시간', value= '```'+ ', '.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)
		else :
			regenembed.add_field(name=str(outputTimeHour[i]) + '시간' + str(outputTimeMin[i]) + '분', value= '```' + ','.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)
	regenembed.set_footer(text = 'R : 멍 보스')
	
	##########################################################

	if basicSetting[15] != "":
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] #정산
		credentials = ServiceAccountCredentials.from_json_keyfile_name(basicSetting[15], scope) #정산

init()

token = basicSetting[0]

channel = ''

async def task():
	await client.wait_until_ready()
	
	global channel

	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt

	global voice_client1

	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type

	global endTime
	global kill_Time

	if chflg == 1 : 
		if voice_client1.is_connected() == False :
			voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
			if voice_client1.is_connected() :
				print("명치복구완료!")
				await dbLoad()
				await client.get_channel(channel).send( '< 다시 왔습니다! >', tts=False)

	while True:
		############ 워닝잡자! ############
		if log_stream.getvalue().find("Awaiting") != -1:
			log_stream.truncate(0)
			log_stream.seek(0)
			await client.get_channel(channel).send( '< 디코접속에러! 잠깐 나갔다 올께요! >', tts=False)
			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
			raise SystemExit

		log_stream.truncate(0)
		log_stream.seek(0)
		##################################
		
		now = datetime.datetime.now()
		priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))
		
		if channel != '':
			################ 보탐봇 재시작 ################ 
			if endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') == now.strftime('%Y-%m-%d ') + now.strftime('%H:%M:%S'):
				await dbSave()
				await FixedBossDateSave()
				await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
				await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
				endTime = endTime + datetime.timedelta(days=int(basicSetting[12]))
				await voice_client1.disconnect()
				#await client.get_channel(channel).send( '<보탐봇 화장실 갔다올 시간! 접속완료 후 명령어 입력 해주세요!>', tts=False)
				print("보탐봇재시작!")
				
				os.system('restart.bat')
			
			################ 킬 목록 초기화 ################ 
			if kill_Time.strftime('%Y-%m-%d ') + kill_Time.strftime('%H:%M') == now.strftime('%Y-%m-%d ') + now.strftime('%H:%M'):
				kill_Time = kill_Time + datetime.timedelta(days=int(1))
				await init_data_list('kill_list.ini', '-----척살명단-----')
			
			################ 고정 보스 확인 ################ 
			for i in range(fixed_bossNum):

				################ before_alert1 ################ 
				if fixed_bossTime[i] <= priv0 and fixed_bossTime[i] > priv:
					if basicSetting[3] != '0':
						if fixed_bossFlag0[i] == False:
							fixed_bossFlag0[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + fixed_bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + fixed_bossData[i][3], basicSetting[9], fixed_bossData[i][5])
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림1.mp3')
				
				################ before_alert ################ 
				if fixed_bossTime[i] <= priv and fixed_bossTime[i] > now:
					if basicSetting[1] != '0' :
						if fixed_bossFlag[i] == False:
							fixed_bossFlag[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + fixed_bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + fixed_bossData[i][3], basicSetting[9], fixed_bossData[i][5])
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림.mp3')

				################ 보스 젠 시간 확인 ################
				if fixed_bossTime[i] <= now :
					fixed_bossTime[i] = fixed_bossTime[i]+datetime.timedelta(hours=int(fixed_bossData[i][6]), minutes=int(fixed_bossData[i][7]), seconds = int(0))
					fixed_bossFlag0[i] = False
					fixed_bossFlag[i] = False
					embed = discord.Embed(
							description= "```" + fixed_bossData[i][0] + fixed_bossData[i][4] + "```" ,
							color=0x00ff00
							)
					await client.get_channel(channel).send( embed=embed, tts=False)
					KakaoSendMSG(basicSetting[8], '보탐봇 : ' + fixed_bossData[i][0] + fixed_bossData[i][4], basicSetting[9], fixed_bossData[i][5])
					await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '젠.mp3')

			################ 일반 보스 확인 ################ 
			for i in range(bossNum):

				################ before_alert1 ################ 
				if bossTime[i] <= priv0 and bossTime[i] > priv:
					if basicSetting[3] != '0':
						if bossFlag0[i] == False:
							bossFlag0[i] = True
							if bossData[i][7] != '' :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3] +' [' +  bossTimeString[i] + ']' + '\n<' + bossData[i][7] + '>```', tts=False)
							else :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3] +' [' +  bossTimeString[i] + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3], basicSetting[9], bossData[i][6])
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림1.mp3')
				
				################ before_alert ################ 
				if bossTime[i] <= priv and bossTime[i] > now:
					if basicSetting[1] != '0' :
						if bossFlag[i] == False:
							bossFlag[i] = True
							if bossData[i][7] != '' :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3] +' [' +  bossTimeString[i] + ']' + '\n<' + bossData[i][7] + '>```', tts=False)
							else :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3] +' [' +  bossTimeString[i] + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3], basicSetting[9], bossData[i][6])
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림.mp3')
				
				################ 보스 젠 시간 확인 ################ 
				if bossTime[i] <= now :
					#print ('if ', bossTime[i])
					#print("보스시간 : ", bossTime[i], " 현재시간 : ", now, " 보스명 : ",  bossData[i][0])
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					tmp_bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
					tmp_bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					bossTime[i] = now+datetime.timedelta(days=365)

					if bossData[i][7] != '' :
						embed = discord.Embed(
								description= "```" + bossData[i][0] + bossData[i][4] + '\n<' + bossData[i][7] + '>```' ,
								color=0x00ff00
								)
					else : 
						embed = discord.Embed(
								description= "```" + bossData[i][0] + bossData[i][4] + "```" ,
								color=0x00ff00
								)
					await client.get_channel(channel).send( embed=embed, tts=False)
					KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + bossData[i][4], basicSetting[9], bossData[i][6])
					await PlaySound(voice_client1, './sound/' + bossData[i][0] + '젠.mp3')

				################ 보스 자동 멍 처리 ################ 
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						#print (bossData[i][0], bossTime[i]+datetime.timedelta(days=-365), aftr)
						if basicSetting[2] != '0':
							if int(basicSetting[19]) <= bossMungCnt[i] and int(basicSetting[19]) != 0:
								bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365)
								tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365)
								bossTimeString[i] = '99:99:99'
								bossDateString[i] = '9999-99-99'
								tmp_bossTimeString[i] = '99:99:99'
								tmp_bossDateString[i] = '9999-99-99'
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = 0
								if bossData[i][2] == '0':
									await client.get_channel(channel).send(f'```자동 미입력 횟수 {basicSetting[19]}회 초과! [{bossData[i][0]}] 삭제!```', tts=False)
									print ('자동미입력 횟수초과 <' + bossData[i][0] + ' 삭제완료>')
								else:
									await client.get_channel(channel).send(f'```자동 멍처리 횟수 {basicSetting[19]}회 초과! [{bossData[i][0]}] 삭제!```', tts=False)
									print ('자동멍처리 횟수초과 <' + bossData[i][0] + ' 삭제완료>')
								await dbSave()
								
							else:
								################ 미입력 보스 ################ 
								if bossData[i][2] == '0':
									await client.get_channel(channel).send('```' + bossData[i][0] + ' 미입력 됐습니다.```', tts=False)
									KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' 미입력 됐습니다.', basicSetting[9], bossData[i][6])
									await PlaySound(voice_client1, './sound/' + bossData[i][0] + '미입력.mp3')
									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									bossMungCnt[i] = bossMungCnt[i] + 1
									tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
									tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
									tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
									embed = discord.Embed(
										description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
										color=0xff0000
										)
									await client.get_channel(channel).send( embed=embed, tts=False)
									await dbSave()
								################ 멍 보스 ################ 
								else :
									await client.get_channel(channel).send('```' + bossData[i][0] + ' 멍 입니다.```')
									KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' 멍 입니다.', basicSetting[9], bossData[i][6])
									await PlaySound(voice_client1, './sound/' + bossData[i][0] + '멍.mp3')
									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									bossMungCnt[i] = bossMungCnt[i] + 1
									tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
									tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
									tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
									embed = discord.Embed(
										description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
										color=0xff0000
										)
									await client.get_channel(channel).send( embed=embed, tts=False)
									await dbSave()
											
		await asyncio.sleep(1) # task runs every 60 seconds

#mp3 파일 생성함수(gTTS 이용, 남성목소리)
async def MakeSound(saveSTR, filename):
	tts = gTTS(saveSTR, lang = 'ko')
	tts.save('./' + filename + '.wav')
	'''
	try:
		encText = urllib.parse.quote(saveSTR)
		#print(encText)
		urllib.request.urlretrieve("https://clova.ai/proxy/voice/api/tts?text=" + encText + "%0A&voicefont=1&format=wav",filename + '.wav')
	except Exception as e:
		print (e)
		tts = gTTS(saveSTR, lang = 'ko')
		tts.save('./' + filename + '.wav')
		pass
	'''

#mp3 파일 재생함수
async def PlaySound(voiceclient, filename):
	source = discord.FFmpegPCMAudio(filename)
	try:
		voiceclient.play(source)
	except discord.errors.ClientException:
		while voiceclient.is_playing():
			await asyncio.sleep(1)
	while voiceclient.is_playing():
		await asyncio.sleep(1)
	voiceclient.stop()
	source.cleanup()

#my_bot.db 저장하기
async def dbSave():
	global bossData
	global bossNum
	global bossTime
	global bossTimeString
	global bossDateString
	global bossMungFlag
	global bossMungCnt

	for i in range(bossNum):
		for j in range(bossNum):
			if bossTimeString[i] and bossTimeString[j] != '99:99:99':
				if bossTimeString[i] == bossTimeString[j] and i != j:
					tmp_time1 = bossTimeString[j][:6]
					tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
					if tmp_time2 < 10 :
						tmp_time22 = '0' + str(tmp_time2)
					elif tmp_time2 == 60 :
						tmp_time22 = '00'
					else :
						tmp_time22 = str(tmp_time2)
					bossTimeString[j] = tmp_time1 + tmp_time22

	datelist1 = bossTime

	datelist = list(set(datelist1))

	information1 = '----- 보스탐 정보 -----\n'

	for timestring in sorted(datelist):
		for i in range(bossNum):
			if timestring == bossTime[i]:
				if bossTimeString[i] != '99:99:99' or bossMungFlag[i] == True:
					if bossMungFlag[i] == True :
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][7] + '\n'
						else : 
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (멍 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][7] + '\n'
					else:
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][7] + '\n'
						else : 
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][7] + '\n'
	
	file = open("my_bot.db", 'w')
	file.write(information1)
	file.close()

#my_bot.db 불러오기
async def dbLoad():
	global LoadChk
	try:
		file = open('my_bot.db', 'r')
		beforeBossData = file.readlines()
		
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				startPos = beforeBossData[i+1].find('-')
				endPos = beforeBossData[i+1].find('(')
				if beforeBossData[i+1][startPos+2:endPos] == bossData[j][0] :
					tmp_mungcnt = 0
					
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')
					tmp_msglen = beforeBossData[i+1].find('*')
					
					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]
					
					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
					
					now2 = datetime.datetime.now()
					tmp_now = now2

					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					tmp_now_chk = tmp_now + datetime.timedelta(minutes = int(basicSetting[2]))

					if tmp_now_chk < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while tmp_now_chk < now2 :
							tmp_now_chk = tmp_now_chk + deltaTime
							tmp_now = tmp_now + deltaTime
							tmp_mungcnt = tmp_mungcnt + 1

					if tmp_now_chk > now2 > tmp_now: #젠중.
						bossMungFlag[j] = True
						tmp_bossTime[j] = tmp_now
						tmp_bossTimeString[j] = tmp_bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = tmp_bossTime[j].strftime('%Y-%m-%d')
						bossTimeString[j] = '99:99:99'
						bossDateString[j] = '9999-99-99'
						bossTime[j] = tmp_bossTime[j] + datetime.timedelta(days=365)
					else:
						tmp_bossTime[j] = bossTime[j] = tmp_now
						tmp_bossTimeString[j] = bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')

					bossData[j][7] = beforeBossData[i+1][tmp_msglen+2:len(beforeBossData[i+1])-1]
					if beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3] != 0 and beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] == ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					elif beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] != ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] + beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					else:
						bossMungCnt[j] = 0

		file.close()

		LoadChk = 0
		print ("<불러오기 완료>")
	except IOError:
		LoadChk = 1
		print ("보스타임 정보가 없습니다.")

#고정보스 날짜저장
async def FixedBossDateSave():
	global fixed_bossData
	global fixed_bossTime
	global fixed_bossNum
	global FixedBossDateData
	global indexFixedBossname

	for i in range(fixed_bossNum):
		FixedBossDateData[indexFixedBossname[i] + 3] = 'startDate = '+ fixed_bossTime[i].strftime('%Y-%m-%d') + '\n'

	outputfixedbossData = open('fixed_boss.ini', 'w', encoding = 'utf-8')
	outputfixedbossData.writelines(FixedBossDateData)
	outputfixedbossData.close()

#사다리함수
async def LadderFunc(number, ladderlist, channelVal):
	if number < len(ladderlist):
		result_ladder = random.sample(ladderlist, number)
		result_ladderSTR = ','.join(map(str, result_ladder))
		embed = discord.Embed(
			title = "----- 당첨! -----",
			description= '```' + result_ladderSTR + '```',
			color=0xff00ff
			)
		await channelVal.send(embed=embed, tts=False)
	else:
		await channelVal.send('```추첨인원이 총 인원과 같거나 많습니다. 재입력 해주세요```', tts=False)

#data초기화
async def init_data_list(filename, first_line : str = "-----------"):
	file = open(filename, 'w', encoding = 'utf-8')
	file.writelines(first_line)
	file.close()
	print ('< 데이터 초기화 >')

#data저장
async def data_list_Save(filename, first_line : str = "-----------",  save_data : dict = {}):

	output_list = first_line+ '\n'
	for key, value in save_data.items():
		output_list += str(key) + ' ' + str(value) + '\n'

	file = open(filename, 'w', encoding = 'utf-8')
	file.writelines(output_list)	
	file.close()

#카톡메세지
def KakaoSendMSG(ChatRoom, SendMSG, allSend, bossSend):
	if allSend == "1" and bossSend == "1":
		kakao = win32gui.FindWindow(None, ChatRoom)
		kakaoED = win32gui.FindWindowEx(kakao, None, "RichEdit20W", None)
		
		if kakaoED == 0:
			kakaoED = win32gui.FindWindowEx(kakao, None, "RichEdit50W", None)

		if kakao != None and kakaoED != 0:	
			try :
				win32gui.SendMessage(kakaoED, win32con.WM_SETTEXT, 0, SendMSG)
				win32gui.PostMessage(kakaoED, win32con.WM_KEYDOWN, win32con.VK_RETURN, None)
				win32gui.PostMessage(kakaoED, win32con.WM_KEYUP, win32con.VK_RETURN, None)
			except :
				print('카톡창이 닫혀 있거나 방이름이 다릅니다. 카톡 창을 확인해 주세요!')
				pass
		else :
			print('카톡창이 닫혀 있거나 방이름이 다릅니다. 카톡 창을 확인해 주세요!')


#카톡알림설정저장
def KakaoAlertSave(saveBossName, AlertStatus):
	global katalkData
	global indexBossname

	for value in indexBossname:
		if katalkData[value].find(saveBossName) != -1:
			katalkData[value + 5] = 'kakaoOnOff = '+ AlertStatus + '\n'

	outputkatalkData = open('boss.ini', 'w', encoding = 'utf-8')
	outputkatalkData.writelines(katalkData)
	outputkatalkData.close()

#초성추출 함수

def convertToInitialLetters(text):
	CHOSUNG_START_LETTER = 4352
	JAMO_START_LETTER = 44032
	JAMO_END_LETTER = 55203
	JAMO_CYCLE = 588

	def isHangul(ch):
		return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER
	
	def isBlankOrNumber(ch):
		return ord(ch) == 32 or ord(ch) >= 48 and ord(ch) <= 57

	def convertNomalInitialLetter(ch):
		dic_InitalLetter = {4352:"ㄱ"
							,4353:"ㄲ"
							,4354:"ㄴ"
							,4355:"ㄷ"
							,4356:"ㄸ"
							,4357:"ㄹ"
							,4358:"ㅁ"
							,4359:"ㅂ"
							,4360:"ㅃ"
							,4361:"ㅅ"
							,4362:"ㅆ"
							,4363:"ㅇ"
							,4364:"ㅈ"
							,4365:"ㅉ"
							,4366:"ㅊ"
							,4367:"ㅋ"
							,4368:"ㅌ"
							,4369:"ㅍ"
							,4370:"ㅎ"
							,32:" "
							,48:"0"
							,49:"1"
							,50:"2"
							,51:"3"
							,52:"4"
							,53:"5"
							,54:"6"
							,55:"7"
							,56:"8"
							,57:"9"
		}
		return dic_InitalLetter[ord(ch)]

	result = ""
	for ch in text:
		if isHangul(ch): #한글이 아닌 글자는 걸러냅니다.
			result += convertNomalInitialLetter(chr((int((ord(ch)-JAMO_START_LETTER)/JAMO_CYCLE))+CHOSUNG_START_LETTER))
		elif isBlankOrNumber(ch):
			result += convertNomalInitialLetter(chr(int(ord(ch))))

	return result

def handle_exit():
	#print("Handling")
	client.loop.run_until_complete(client.logout())

	for t in asyncio.Task.all_tasks(loop=client.loop):
		if t.done():
			#t.exception()
			try:
				#print ('try :   ', t)
				t.exception()
			except asyncio.CancelledError:
				#print ('cancel :   ', t)
				continue
			continue
		t.cancel()
		try:
			client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
			t.exception()
		except asyncio.InvalidStateError:
			pass
		except asyncio.TimeoutError:
			pass
		except asyncio.CancelledError:
			pass

@client.event
async def on_ready():
	global basicSetting
	
	global channel

	global voice_client1
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chkvoicechannel
	global chflg

	global endTime
	global setting_channel_name
	global all_guilds
			
	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")

	all_guilds = client.guilds
	all_channels = client.get_all_channels()

	for channel1 in all_channels:
		channel_type.append(str(channel1.type))
		channel_info.append(channel1)
	
	for i in range(len(channel_info)):
		if channel_type[i] == "text":
			channel_name.append(str(channel_info[i].name))
			channel_id.append(str(channel_info[i].id))
			
	for i in range(len(channel_info)):
		if channel_type[i] == "voice":
			channel_voice_name.append(str(channel_info[i].name))
			channel_voice_id.append(str(channel_info[i].id))

	await dbLoad()

	if str(basicSetting[6]) in channel_voice_id and str(basicSetting[7]) in channel_id:
		voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
		channel = basicSetting[7]
		
		setting_channel_name = client.get_channel(basicSetting[7]).name

		print('< 접속시간 [' + datetime.datetime.now().strftime('%Y-%m-%d ') + datetime.datetime.now().strftime('%H:%M:%S') + '] >')
		print('< 텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료 >')
		print('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료 >')
		if basicSetting[10] != "":
			if str(basicSetting[10]) in channel_id:
				print('< 사다리채널 [' + client.get_channel(int(basicSetting[10])).name + '] 접속완료 >')
			else:
				basicSetting[10] = ""
				print(f"사다리채널 ID 오류! [{command[33][0]} 사다리] 명령으로 재설정 바랍니다.")
		if basicSetting[13] != "":
			if str(basicSetting[13]) in channel_id:
				print('< 정산채널 [' + client.get_channel(int(basicSetting[13])).name + '] 접속완료>')
			else:
				basicSetting[13] = ""
				print(f"정산채널 ID 오류! [{command[33][0]} 정산] 명령으로 재설정 바랍니다.")
		if basicSetting[20] != "":
			if str(basicSetting[20]) in channel_id:
				print('< 척살채널 [' + client.get_channel(int(basicSetting[20])).name + '] 접속완료>')
			else:
				basicSetting[20] = ""
				print(f"척살채널 ID 오류! [{command[33][0]} 척살] 명령으로 재설정 바랍니다.")
		if basicSetting[21] != "":
			if str(basicSetting[21]) in channel_id:
				print('< 경주채널 [' + client.get_channel(int(basicSetting[21])).name + '] 접속완료>')
			else:
				basicSetting[21] = ""
				print(f"경주채널 ID 오류! [{command[33][0]} 경주] 명령으로 재설정 바랍니다.")
		if basicSetting[22] != "":
			if str(basicSetting[22]) in channel_id:
				print('< 아이템채널 [' + client.get_channel(int(basicSetting[22])).name + '] 접속완료>')
			else:
				basicSetting[22] = ""
				print(f"아이템채널 ID 오류! [{command[33][0]} 아이템] 명령으로 재설정 바랍니다.")
		if int(basicSetting[12]) != 0 :
			print('< 보탐봇 재시작 시간 [' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + '] >')
			print('< 보탐봇 재시작 주기 [' + basicSetting[12] + '일] >')
		else :
			print('< 보탐봇 재시작 설정안됨 >')
		chflg = 1
	else:
		basicSetting[6] = ""
		basicSetting[7] = ""
		print(f"설정된 채널 값이 없거나 잘못 됐습니다. **[{command[0][0]}]** 명령어 먼저 입력하여 사용해주시기 바랍니다.")

	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=command[1][0], type=1), afk = False)

while True:
	################ 보탐봇 입장 ################
	@commands.has_permissions(manage_messages=True)
	@client.command(name=command[0][0], aliases=command[0][1:])
	async def join_(ctx):
		global basicSetting
		global chflg
		global voice_client1

		if basicSetting[7] == "":
			channel = ctx.message.channel.id #메세지가 들어온 채널 ID

			print ('[ ', basicSetting[7], ' ]')
			print ('] ', ctx.message.channel.name, ' [')

			inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
			inputData_text = inidata_text.readlines()
			inidata_text.close()
		
			inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
			for i in range(len(inputData_text)):
				if inputData_text[i].startswith("textchannel ="):
					inputData_text[i] = 'textchannel = ' +str(channel) + '\n'
					basicSetting[7] = channel
			
			inidata_text.writelines(inputData_text)
			inidata_text.close()

			await ctx.send(f"< 텍스트채널 [{ctx.message.channel.name}] 접속완료 >\n< 음성채널 접속 후 [{command[6][0]}] 명령을 사용 하세요 >", tts=False)
			
			print('< 텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료>')
			if basicSetting[6] != "":
				voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
				print('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>')
			if basicSetting[10] != "":
				if str(basicSetting[10]) in channel_id:
					print('< 사다리채널 [' + client.get_channel(int(basicSetting[10])).name + '] 접속완료 >')
				else:
					basicSetting[10] = ""
					print(f"사다리채널 ID 오류! [{command[33][0]} 사다리] 명령으로 재설정 바랍니다.")
			if basicSetting[13] != "":
				if str(basicSetting[13]) in channel_id:
					print('< 정산채널 [' + client.get_channel(int(basicSetting[13])).name + '] 접속완료>')
				else:
					basicSetting[13] = ""
					print(f"정산채널 ID 오류! [{command[33][0]} 정산] 명령으로 재설정 바랍니다.")
			if basicSetting[20] != "":
				if str(basicSetting[20]) in channel_id:
					print('< 척살채널 [' + client.get_channel(int(basicSetting[20])).name + '] 접속완료>')
				else:
					basicSetting[20] = ""
					print(f"척살채널 ID 오류! [{command[33][0]} 척살] 명령으로 재설정 바랍니다.")
			if basicSetting[21] != "":
				if str(basicSetting[21]) in channel_id:
					print('< 경주채널 [' + client.get_channel(int(basicSetting[21])).name + '] 접속완료>')
				else:
					basicSetting[21] = ""
					print(f"경주채널 ID 오류! [{command[33][0]} 경주] 명령으로 재설정 바랍니다.")
			if basicSetting[22] != "":
				if str(basicSetting[22]) in channel_id:
					print('< 아이템채널 [' + client.get_channel(int(basicSetting[22])).name + '] 접속완료>')
				else:
					basicSetting[22] = ""
					print(f"아이템채널 ID 오류! [{command[33][0]} 아이템] 명령으로 재설정 바랍니다.")
			if int(basicSetting[12]) != 0 :
				print('< 보탐봇 재시작 시간 ' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + ' >')
				print('< 보탐봇 재시작 주기 ' + basicSetting[12] + '일 >')
			else :
				print('< 보탐봇 재시작 설정안됨 >')
			
			chflg = 1
		else:
			for guild in all_guilds:
				for text_channel in guild.text_channels:
					if basicSetting[7] == text_channel.id:
						curr_guild_info = guild

			emoji_list : list = ["⭕", "❌"]
			guild_error_message = await ctx.send(f"이미 **[{curr_guild_info.name}]** 서버 **[{setting_channel_name}]** 채널이 명령어 채널로 설정되어 있습니다.\n해당 채널로 명령어 채널을 변경 하시려면 ⭕ 그대로 사용하시려면 ❌ 를 눌러주세요.\n(10초이내 미입력시 기존 설정 그대로 설정됩니다.)", tts=False)

			for emoji in emoji_list:
				await guild_error_message.add_reaction(emoji)

			def reaction_check(reaction, user):
				return (reaction.message.id == guild_error_message.id) and (user.id == ctx.author.id) and (str(reaction) in emoji_list)
			try:
				reaction, user = await client.wait_for('reaction_add', check = reaction_check, timeout = 10)
			except asyncio.TimeoutError:
				return await ctx.send(f"시간이 초과됐습니다. **[{curr_guild_info.name}]** 서버 **[{setting_channel_name}]** 채널에서 사용해주세요!")
			
			if str(reaction) == "⭕":
				await voice_client1.disconnect()
				basicSetting[6] = ""
				basicSetting[7] = int(ctx.message.channel.id)

				print ('[ ', basicSetting[7], ' ]')
				print ('] ', ctx.message.channel.name, ' [')

				inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
				inputData_text = inidata_text.readlines()
				inidata_text.close()
			
				inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
				for i in range(len(inputData_text)):
					if inputData_text[i].startswith("textchannel ="):
						inputData_text[i] = 'textchannel = ' +str(basicSetting[7]) + '\n'
				
				inidata_text.writelines(inputData_text)
				inidata_text.close()

				return await ctx.send(f"명령어 채널이 **[{ctx.author.guild.name}]** 서버 **[{ctx.message.channel.name}]** 채널로 새로 설정되었습니다.\n< 음성채널 접속 후 [{command[6][0]}] 명령을 사용 하세요 >")
			else:
				return await ctx.send(f"명령어 채널 설정이 취소되었습니다.\n**[{curr_guild_info.name}]** 서버 **[{setting_channel_name}]** 채널에서 사용해주세요!")

	################ 보탐봇 메뉴 출력 ################ 	.

	@client.command(name=command[1][0], aliases=command[1][1:])
	async def menu_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			command_list = ''
			command_list += ','.join(command[2]) + '\n'     #!설정확인
			command_list += ','.join(command[3]) + '\n'     #!카톡확인
			command_list += ','.join(command[4]) + '\n'     #!채널확인
			command_list += ','.join(command[5]) + ' [채널명]\n'     #!채널이동
			command_list += ','.join(command[6]) + ' ※ 관리자만 실행 가능\n'     #!소환
			command_list += ','.join(command[7]) + '\n'     #!불러오기
			command_list += ','.join(command[8]) + '\n'     #!초기화
			command_list += ','.join(command[9]) + '\n'     #!명치
			command_list += ','.join(command[10]) + '\n'     #!재시작
			command_list += ','.join(command[11]) + '\n'     #!미예약
			command_list += ','.join(command[12]) + ' [인원] [금액]\n'     #!분배
			command_list += ','.join(command[13]) + ' [뽑을인원수] [아이디1] [아이디2]...\n'     #!사다리
			command_list += ','.join(command[32]) + ' [아이디1] [아이디2]...(최대 12명)\n'     #!경주
			command_list += ','.join(command[14]) + ' [아이디]\n'     #!정산
			command_list += ','.join(command[15]) + ' 또는 ' + ', '.join(command[15]) + '0000, 00:00\n'     #!보스일괄
			command_list += ','.join(command[16]) + '\n'     #!카톡끔
			command_list += ','.join(command[17]) + '\n'     #!카톡켬
			command_list += ','.join(command[18]) + '\n'     #!q
			command_list += ','.join(command[19]) + ' [할말]\n'     #!k
			command_list += ','.join(command[20]) + ' [할말]\n'     #!v
			command_list += ','.join(command[21]) + '\n'     #!카톡보스
			command_list += ','.join(command[22]) + '\n'     #!리젠
			command_list += ','.join(command[23]) + '\n'     #!현재시간
			command_list += ','.join(command[29]) + '\n'     #!킬초기화
			command_list += ','.join(command[30]) + '\n'     #!킬횟수 확인
			command_list += ','.join(command[30]) + ' [아이디]\n'     #!킬
			command_list += ','.join(command[31]) + ' [아이디]\n'     #!킬삭제
			command_list += ','.join(command[38]) + ' [아이디] 또는 ' + ','.join(command[38]) + ' [아이디] [횟수]\n'     #!킬차감
			command_list += ','.join(command[34]) + '\n'     #!아이템 목록 초기화
			command_list += ','.join(command[35]) + '\n'     #!아이템 목록 확인
			command_list += ','.join(command[35]) + ' [아이템] 또는 ' + ','.join(command[35]) + ' [아이템] [개수]\n'     #!아이템 목록 입력
			command_list += ','.join(command[36]) + ' [아이템]\n'     #!아이템 목록에서 삭제
			command_list += ','.join(command[37]) + ' [아이템] 또는 ' + ','.join(command[37]) + ' [아이템] [개수]\n'     #!아이템 차감
			command_list += ','.join(command[24]) + '\n'     #!공지
			command_list += ','.join(command[24]) + ' [공지내용]\n'     #!공지
			command_list += ','.join(command[25]) + '\n'     #!공지삭제
			command_list += ','.join(command[26]) + ' [할말]\n'     #!상태
			command_list += ','.join(command[33]) + ' 사다리, 정산, 척살, 경주, 아이템\n\n'     #!채널설정
			command_list += ','.join(command[27]) + '\n'     #보스탐
			command_list += ','.join(command[28]) + '\n'     #!보스탐
			command_list += '[보스명]컷 또는 [보스명]컷 0000, 00:00\n'
			command_list += '[보스명] 컷 또는 [보스명] 컷 0000, 00:00\n'
			command_list += '[보스명]멍 또는 [보스명]멍 0000, 00:00\n'
			command_list += '[보스명]예상 또는 [보스명]예상 0000, 00:00\n'
			command_list += '[보스명]삭제\n'
			command_list += '[보스명]메모 [할말]\n'
			command_list += '[보스명]카톡켬, [보스명]카톡끔'
			
			embed = discord.Embed(
					title = "----- 명령어 -----",
					description= '```' + command_list + '```',
					color=0xff00ff
					)
			embed.add_field(
					name="----- 추가기능 -----",
					value= '```- [보스명]컷/멍/예상  [할말] : 보스시간 입력 후 빈칸 두번!! 메모 가능\n- [보스명]컷 명령어는 초성으로 입력가능합니다.\n  ex)' + bossData[0][0] + '컷 => ' + convertToInitialLetters(bossData[0][0] +'컷') + ', ' + bossData[0][0] + ' 컷 => ' + convertToInitialLetters(bossData[0][0] +' 컷') + '```'
					)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 보탐봇 기본 설정확인 ################ 
	@client.command(name=command[2][0], aliases=command[2][1:])
	async def setting_(ctx):	
		#print (ctx.message.channel.id)
		if ctx.message.channel.id == basicSetting[7]:
			setting_val = '보탐봇버전 : PC Ver. 25 (2020. 7. 4.)\n'
			setting_val += '음성채널 : ' + client.get_channel(basicSetting[6]).name + '\n'
			setting_val += '텍스트채널 : ' + client.get_channel(basicSetting[7]).name +'\n'
			if basicSetting[10] != "" :
				setting_val += '사다리채널 : ' + client.get_channel(int(basicSetting[10])).name + '\n'
			if basicSetting[13] != "" :
				setting_val += '정산채널 : ' + client.get_channel(int(basicSetting[13])).name + '\n'
			if basicSetting[20] != "" :
				setting_val += '척살채널 : ' + client.get_channel(int(basicSetting[20])).name + '\n'
			if basicSetting[21] != "" :
				setting_val += '경주채널 : ' + client.get_channel(int(basicSetting[21])).name + '\n'
			if basicSetting[22] != "" :
				setting_val += '아이템채널 : ' + client.get_channel(int(basicSetting[22])).name + '\n'
			if basicSetting[8] != "" :
				setting_val += '카톡챗방명 : ' + basicSetting[8] + '\n'
			setting_val += '보스젠알림시간1 : ' + basicSetting[1] + ' 분 전\n'
			setting_val += '보스젠알림시간2 : ' + basicSetting[3] + ' 분 전\n'
			setting_val += '보스멍확인시간 : ' + basicSetting[2] + ' 분 후\n'
			embed = discord.Embed(
					title = "----- 설정내용 -----",
					description= f'```{setting_val}```',
					color=0xff00ff
					)
			embed.add_field(
					name="----- Special Thanks to. -----",
					value= '```총무님, 옹님```'
					)
			await ctx.send(embed=embed, tts=False)
			#print ('보스젠알림시간1 : ', basicSetting[1])
			#print ('보스젠알림시간2 : ', basicSetting[3])
			#print ('보스멍확인시간 : ', basicSetting[2])
		else:
			return

	################ 카톡 설정 확인 ################ 
	@client.command(name=command[3][0], aliases=command[3][1:])
	async def kakaoSetting_(ctx):	
		if ctx.message.channel.id == basicSetting[7]:
			katalkInformation = ''
			if basicSetting[9] == '0' :
				katalkInformation = '전체카톡 : 꺼짐\n'
			else : 
				katalkInformation = '전체카톡 : 켜짐\n'
			
			katalkInformation += '---------------------\n'

			for i in range(bossNum):
				for j in range(bossNum):
					if bossTimeString[i] and bossTimeString[j] != '99:99:99':
						if bossTimeString[i] == bossTimeString[j] and i != j:
							tmp_time1 = bossTimeString[j][:6]
							tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
							if tmp_time2 < 10 :
								tmp_time22 = '0' + str(tmp_time2)
							elif tmp_time2 == 60 :
								tmp_time22 = '00'
							else :
								tmp_time22 = str(tmp_time2)
							bossTimeString[j] = tmp_time1 + tmp_time22

			datelist2 = bossTime

			datelist = list(set(datelist2))
			
			for timestring in sorted(datelist):
				for i in range(bossNum):
					if timestring == bossTime[i]:
						if bossTimeString[i] != '99:99:99' :
							if 	bossData[i][6] == '0':
								katalkInformation += bossData[i][0] + " 카톡 : 꺼짐\n"
							else :
								katalkInformation += bossData[i][0] + " 카톡 : 켜짐\n"
			embed = discord.Embed(
					title = "----- 카톡설정내용 -----",
					description= katalkInformation,
					color=0xff00ff
					)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 서버 채널 확인 ################ 
	@client.command(name=command[4][0], aliases=command[4][1:])
	async def chChk_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			ch_information = []
			cnt = 0
			ch_information.append('')
			for i in range(len(channel_name)):
				if len(ch_information[cnt]) > 900 :
					ch_information.append('')
					cnt += 1
				ch_information[cnt] = ch_information[cnt] + '[' + channel_id[i] + '] ' + channel_name[i] + '\n'

			ch_voice_information = []
			cntV = 0
			ch_voice_information.append('')
			for i in range(len(channel_voice_name)):
				if len(ch_voice_information[cntV]) > 900 :
					ch_voice_information.append('')
					cntV += 1
				ch_voice_information[cntV] = ch_voice_information[cntV] + '[' + channel_voice_id[i] + '] ' + channel_voice_name[i] + '\n'

			if len(ch_information) == 1 and len(ch_voice_information) == 1:
				embed = discord.Embed(
					title = "----- 채널 정보 -----",
					description= '',
					color=0xff00ff
					)
				embed.add_field(
					name="< 택스트 채널 >",
					value= '```' + ch_information[0] + '```',
					inline = False
					)
				embed.add_field(
					name="< 보이스 채널 >",
					value= '```' + ch_voice_information[0] + '```',
					inline = False
					)

				await ctx.send( embed=embed, tts=False)
			else :
				embed = discord.Embed(
					title = "----- 채널 정보 -----\n< 택스트 채널 >",
					description= '```' + ch_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(ch_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send( embed=embed, tts=False)
				embed = discord.Embed(
					title = "< 음성 채널 >",
					description= '```' + ch_voice_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(ch_voice_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_voice_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 텍스트 채널 이동 ################ 
	@client.command(name=command[5][0], aliases=command[5][1:])
	async def chMove_(ctx):	
		global basicSetting
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(len(channel_name)):
				if  channel_name[i] == msg:
					channel = int(channel_id[i])
			
			print (f'[ {client.get_channel(basicSetting[7]).name} ]에서')
			print (f'] {client.get_channel(channel).name} [이동')
					
			if basicSetting[7] != channel:
				inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
				inputData_text = inidata_text.readlines()
				inidata_text.close()
				
				inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')
				for i in range(len(inputData_text)):
					if inputData_text[i].startswith('textchannel ='):
						inputData_text[i] = 'textchannel = ' + str(channel) + '\n'
						basicSetting[7] = channel
							
				inidata_text.writelines(inputData_text)
				inidata_text.close()
			
			await ctx.send( f'명령어 채널이 < {ctx.message.channel.name} >에서 < {client.get_channel(channel).name} > 로 이동되었습니다.', tts=False)
			await client.get_channel(channel).send( f'< {client.get_channel(channel).name} 이동완료 >', tts=False)
		else:
			return

	################ 보탐봇 음성채널 소환 ################ 
	@commands.has_permissions(manage_messages=True)
	@client.command(name=command[6][0], aliases=command[6][1:])
	async def connectVoice_(ctx):
		global voice_client1
		global basicSetting
		if ctx.message.channel.id == basicSetting[7]:
			if ctx.voice_client is None:
				if ctx.author.voice:
					voice_client1 = await ctx.author.voice.channel.connect(reconnect = True)
				else:
					await ctx.send('음성채널에 먼저 들어가주세요.', tts=False)
					return
			else:
				if ctx.voice_client.is_playing():
					ctx.voice_client.stop()

				await ctx.voice_client.move_to(ctx.author.voice.channel)

			voice_channel = ctx.author.voice.channel

			print ('< ', basicSetting[6], ' >')
			print ('> ', client.get_channel(voice_channel.id).name, ' <')
			
			if basicSetting[6] == "":
				inidata_voice = open('test_setting.ini', 'r', encoding = 'utf-8')
				inputData_voice = inidata_voice.readlines()
				inidata_voice.close()
			
				inidata_voice = open('test_setting.ini', 'w', encoding = 'utf-8')				
				for i in range(len(inputData_voice)):
					if inputData_voice[i].startswith('voicechannel ='):
						inputData_voice[i] = 'voicechannel = ' + str(voice_channel.id) + '\n'
						basicSetting[6] = int(voice_channel.id)
						#print ('======', inputData_voice[i])
				
				inidata_voice.writelines(inputData_voice)
				inidata_voice.close()
				
			elif basicSetting[6] != int(voice_channel.id):
				inidata_voice = open('test_setting.ini', 'r', encoding = 'utf-8')
				inputData_voice = inidata_voice.readlines()
				inidata_voice.close()
				
				inidata_voice = open('test_setting.ini', 'w', encoding = 'utf-8')
				for i in range(len(inputData_voice)):
					if inputData_voice[i].startswith('voicechannel ='):
						inputData_voice[i] = 'voicechannel = ' + str(voice_channel.id) + '\n'
						basicSetting[6] = int(voice_channel.id)
						#print ('+++++++', inputData_voice[i])
							
				inidata_voice.writelines(inputData_voice)
				inidata_voice.close()

			await ctx.send( '< 음성채널 [' + client.get_channel(voice_channel.id).name + '] 접속완료>', tts=False)
		else:
			return


	################ my_bot.db에 저장된 보스타임 불러오기 ################ 
	@client.command(name=command[7][0], aliases=command[7][1:])
	async def loadDB_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await dbLoad()

			if LoadChk == 0:
				await ctx.send( '<불러오기 완료>', tts=False)
			else:
				await ctx.send( '<보스타임 정보가 없습니다.>', tts=False)

	################ 저장된 정보 초기화 ################ 
	@client.command(name=command[8][0], aliases=command[8][1:])
	async def initVal_(ctx):
		global basicSetting
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime
		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global fixed_bossFlag
		global fixed_bossFlag0
		global bossMungFlag
		global bossMungCnt

		global katalkData
		global InitkatalkData
		global indexBossname
		global FixedBossDateData
		global indexFixedBossname
			
		if ctx.message.channel.id == basicSetting[7]:
			basicSetting = []
			bossData = []
			fixed_bossData = []

			bossTime = []
			tmp_bossTime = []
			fixed_bossTime = []

			bossTimeString = []
			bossDateString = []
			tmp_bossTimeString = []
			tmp_bossDateString = []

			bossFlag = []
			bossFlag0 = []
			fixed_bossFlag = []
			fixed_bossFlag0 = []
			bossMungFlag = []
			bossMungCnt = []

			katalkData = []
			InitkatalkData = []
			indexBossname = []
			FixedBossDateData = []
			indexFixedBossname = []
			
			init()

			await dbSave()

			await ctx.send( '< 초기화 완료 >', tts=False)
			print ("< 초기화 완료 >")
		else:
			return
			
	################ 명존쎄 ################ 
	@client.command(name=command[9][0], aliases=command[9][1:])
	async def mungchi_(ctx):
		global basicSetting
		global bossTimeString
		global bossDateString
		global bossFlag
		global bossFlag0
		global bossMungFlag

		if ctx.message.channel.id == basicSetting[7]:
			await ctx.send( '< 보탐봇 명치 맞고 숨 고르기 중! 잠시만요! >', tts=False)
			print("명치!")
			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
			await voice_client1.disconnect()
			#client.clear()
			raise SystemExit
		else:
			return	

	################ 보탐봇 재시작 ################ 
	@client.command(name=command[10][0], aliases=command[10][1:])
	async def restart_(ctx):
		global basicSetting
		global bossTimeString
		global bossDateString

		if ctx.message.channel.id == basicSetting[7]:
			if basicSetting[2] != '0':
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
			await voice_client1.disconnect()
			print("보탐봇강제재시작!")
			os.system('restart.bat')
		else:
			return

	################ 미예약 보스타임 출력 ################ 
	@client.command(name=command[11][0], aliases=command[11][1:])
	async def nocheckBoss_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')
			
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1800 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','

			if len(tmp_boss_information) == 1:
				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- 미예약 보스 -----",
						description= tmp_boss_information[0],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
			else:
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1 :
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- 미예약 보스 -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"							
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 분배 결과 출력 ################
	@client.command(name=command[12][0], aliases=command[12][1:])
	async def bunbae_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			separate_money = []
			separate_money = msg.split(" ")
			num_sep = floor(int(separate_money[0]))
			cal_tax1 = floor(float(separate_money[1])*0.05)
			
			real_money = floor(floor(float(separate_money[1])) - cal_tax1)
			cal_tax2 = floor(real_money/num_sep) - floor(float(floor(real_money/num_sep))*0.95)
			if num_sep == 0 :
				await ctx.send('```분배 인원이 0입니다. 재입력 해주세요.```', tts=False)
			else :
				embed = discord.Embed(
					title = "----- 분배결과! -----",
					description= '```1차 세금 : ' + str(cal_tax1) + '\n1차 수령액 : ' + str(real_money) + '\n분배자 거래소등록금액 : ' + str(floor(real_money/num_sep)) + '\n2차 세금 : ' + str(cal_tax2) + '\n인당 실수령액 : ' + str(floor(float(floor(real_money/num_sep))*0.95)) + '```',
					color=0xff00ff
					)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 사다리 결과 출력 ################ 
	@client.command(name=command[13][0], aliases=command[13][1:])
	async def ladder_(ctx):	
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[10]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			ladder = []
			ladder = msg.split(" ")			
			try:
				num_cong = int(ladder[0])
				del(ladder[0])
			except ValueError:
				return await ctx.send('```뽑을 인원은 숫자로 입력바랍니다\nex)!사다리 1 가 나 다 ...```')
			await LadderFunc(num_cong, ladder, ctx)
		else:
			return

	################ 정산확인 ################ 
	@client.command(name=command[14][0], aliases=command[14][1:])
	async def jungsan_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[13]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			if basicSetting[14] != "" and basicSetting[15] != "" and basicSetting[16] != "" and basicSetting[17] != "" and basicSetting[18] != "":
				SearchID = msg
				gc = gspread.authorize(credentials)
				wks = gc.open(basicSetting[14]).worksheet(basicSetting[16])  #정산결과 시트이름

				wks.update_acell(basicSetting[17], SearchID) 

				result = wks.acell(basicSetting[18]).value

				embed = discord.Embed(
						description= '```' + SearchID + ' 님이 받을 다이야는 ' + result + ' 다이야 입니다.```',
						color=0xff00ff
						)
				await ctx.send(embed=embed, tts=False)
		else :
			return

	################ 보스타임 일괄 설정 ################
	@client.command(name=command[15][0], aliases=command[15][1:])
	async def allBossInput_(ctx): 
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(bossNum):
				tmp_msg = msg
				if len(tmp_msg) > 3 :
					if tmp_msg.find(':') != -1 :
						chkpos = tmp_msg.find(':')
						hours1 = tmp_msg[chkpos-2:chkpos]
						minutes1 = tmp_msg[chkpos+1:chkpos+3]
						now2 = datetime.datetime.now()
						tmp_now = datetime.datetime.now()
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						chkpos = len(tmp_msg)-2
						hours1 = tmp_msg[chkpos-2:chkpos]
						minutes1 = tmp_msg[chkpos:chkpos+2]
						now2 = datetime.datetime.now()
						tmp_now = datetime.datetime.now()
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
				else:
					now2 = datetime.datetime.now()
					tmp_now = now2
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 1

				if tmp_now > now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(-1))
					
				if tmp_now < now2 : 
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						bossMungCnt[i] = bossMungCnt[i] + 1
					now2 = tmp_now
					bossMungCnt[i] = bossMungCnt[i] - 1
				else :
					now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							
				tmp_bossTime[i] = bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

			await dbSave()
			await dbLoad()
			await dbSave()
			
			await ctx.send( '<보스 일괄 입력 완료>', tts=False)
			print ("<보스 일괄 입력 완료>")
		else:
			return

	################ 전체 카톡 끔 ################ 
	@client.command(name=command[16][0], aliases=command[16][1:])
	async def allkakaoOn_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			basicSetting[9] = '0'
			InitkatalkData[2] = 'kakaoOnOff = ' + basicSetting[9] +'\n'
			tmp_katalkData = open('test_setting.ini', 'w', encoding = 'utf-8')
			tmp_katalkData.writelines(InitkatalkData)
			tmp_katalkData.close()
			await ctx.send('<카톡 보내기 끔>', tts=False)
		else:
			return

	################ 전체 카톡 켬 ################ 
	@client.command(name=command[17][0], aliases=command[17][1:])
	async def allakakoOff_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			basicSetting[9] = '1'
			InitkatalkData[2] = 'kakaoOnOff = ' + basicSetting[9] +'\n'
			tmp_katalkData = open('test_setting.ini', 'w', encoding = 'utf-8')
			tmp_katalkData.writelines(InitkatalkData)
			tmp_katalkData.close()
			await ctx.send('<카톡 보내기 켬>', tts=False)
		else:
			return

	################ 가장 근접한 보스타임 출력 ################ 
	@client.command(name=command[18][0], aliases=command[18][1:])
	async def nearTimeBoss_(ctx):
		print (ctx.invoked_with)
		if ctx.message.channel.id == basicSetting[7]:
			checkTime = datetime.datetime.now() + datetime.timedelta(days=1)
			
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			sorted_datelist = []
			
			for i in range(bossNum):
				if bossMungFlag[i] != True and bossTimeString[i] != '99:99:99' :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours= 3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			for i in range(bossNum):
				if bossMungFlag[i] != True :
					aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
					aa.append(bossTime[i])                           #output_bossData[1] : 시간
					aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
					aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
					aa.append(bossData[i][7])	                         #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
				aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00)
				aa.append('@')                                       #output_bossData[3] : @
				aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
				aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
				aa.append("")                                        #output_bossData[6] : 메세지
				ouput_bossData.append(aa)
				aa = []

			tmp_sorted_datelist = sorted(datelist)

			for i in range(len(tmp_sorted_datelist)):
				if checkTime > tmp_sorted_datelist[i]:
					sorted_datelist.append(tmp_sorted_datelist[i])

			if len(sorted_datelist) == 0:
				await ctx.send( '<보스타임 정보가 없습니다.>', tts=False)
			else : 
				result_lefttime = ''

				if len(sorted_datelist) > int(basicSetting[11]):
					for j in range(int(basicSetting[11])):
						for i in range(len(ouput_bossData)):
							if sorted_datelist[j] == ouput_bossData[i][1]:
								leftTime = ouput_bossData[i][1] - datetime.datetime.now()

								total_seconds = int(leftTime.total_seconds())
								hours, remainder = divmod(total_seconds,60*60)
								minutes, seconds = divmod(remainder,60)

								result_lefttime += '다음 ' + ouput_bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2]+ ']\n'
				else :
					for j in range(len(sorted_datelist)):
						for i in range(len(ouput_bossData)):						
							if sorted_datelist[j] == ouput_bossData[i][1]:
								leftTime = ouput_bossData[i][1] - datetime.datetime.now()

								total_seconds = int(leftTime.total_seconds())
								hours, remainder = divmod(total_seconds,60*60)
								minutes, seconds = divmod(remainder,60)

								result_lefttime += '다음 ' + ouput_bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2] + ']\n'
								#result_lefttime += bossData[i][0] + '탐[' +  bossTimeString[i] + ']까지 ' + '%02d:%02d:%02d 남았습니다.\n' % (hours,minutes,seconds)

				embed = discord.Embed(
					description= result_lefttime,
					color=0xff0000
					)
				await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 카톡으로 메세지 보내기 ################ 
	@client.command(name=command[19][0], aliases=command[19][1:])
	async def kakaoMsg_(ctx):	
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			sayMessage = msg
			KakaoSendMSG(basicSetting[8], ctx.author.display_name + ' : ' + sayMessage, basicSetting[9], '1')
		else:
			return


	################ 음성파일 생성 후 재생 ################ 		
	@client.command(name=command[20][0], aliases=command[20][1:])
	async def playText_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			sayMessage = msg
			await MakeSound(ctx.message.author.display_name +'님이, ' + sayMessage, './sound/say')
			await ctx.send( "```< " + ctx.author.display_name + " >님이 \"" + sayMessage + "\"```", tts=False)
			await PlaySound(voice_client1, './sound/say.wav')
		else:
			return

	################ 카톡보스타임 출력 ################ 
	@client.command(name=command[21][0], aliases=command[21][1:])
	async def kakaoBoss_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			temp_bossTime1 = []
			ouput_bossData = []
			aa = []
			
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours= 3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					temp_bossTime1.append(bossData[i][0])
				else :
					aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
						aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00)
						aa.append('-')	                                 #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                           #output_bossData[1] : 시간
						aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
						aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
					aa.append(bossData[i][7])	                         #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00)
				aa.append('@')                                       #output_bossData[3] : @
				aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
				aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
				aa.append("")                                        #output_bossData[6] : 메세지
				ouput_bossData.append(aa)
				aa = []

			if len(temp_bossTime1) != 0:
				temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime1))
				temp_bossTimeSTR1 = '```' + temp_bossTimeSTR1 + '```'
			else:
				temp_bossTimeSTR1 = '``` ```'
						
			information = ''
			for timestring in sorted(datelist):
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][5] == 0 :
								information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
						else : 
							if ouput_bossData[i][5] == 0 :
								information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
						
			if len(information) != 0:
				KakaoSendMSG(basicSetting[8], information, basicSetting[9], '1')
			else :
				KakaoSendMSG(basicSetting[8], '보스타임 정보가 없습니다.', basicSetting[9], '1')
		else:
			return

	################ 리젠타임 출력 ################ 
	@client.command(name=command[22][0], aliases=command[22][1:])
	async def regenTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await ctx.send(embed=regenembed, tts=False)
		else:
			return

	################ 현재시간 확인 ################ 
	@client.command(name=command[23][0], aliases=command[23][1:])
	async def currentTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			embed = discord.Embed(
				title = '현재시간은 ' + datetime.datetime.now().strftime('%H') + '시 ' + datetime.datetime.now().strftime('%M') + '분 ' + datetime.datetime.now().strftime('%S')+ '초 입니다.',
				color=0xff00ff
				)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 공지 등록/확인 ################ 
	@client.command(name=command[24][0], aliases=command[24][1:])
	async def notice_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content.split(" ")
			if len(msg) > 1:
				sayMessage = " ".join(msg[1:])
				notice_initdata = open('notice.ini', 'w', encoding = 'utf-8')
				notice_initdata.write(sayMessage)
				notice_initdata.close()
				await ctx.send( '< 공지 등록완료 >', tts=False)
			else :
				notice_initdata = open('notice.ini', 'r', encoding = 'utf-8')
				notice = notice_initdata.read()
				if notice != '' :
					embed = discord.Embed(
							description= str(notice),
							color=0xff00ff
							)
				else :
					embed = discord.Embed(
							description= '등록된 공지가 없습니다.',
							color=0xff00ff
							)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 공지 삭제 ################ 
	@client.command(name=command[25][0], aliases=command[25][1:])
	async def noticeDel_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			notice_initdata = open('notice.ini', 'w', encoding = 'utf-8')
			notice_initdata.write('')
			notice_initdata.close()
			await ctx.send( '< 공지 삭제완료 >', tts=False)
		else:
			return

	################ 봇 상태메세지 변경 ################ 
	@client.command(name=command[26][0], aliases=command[26][1:])
	async def botStatus_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			sayMessage = msg
			await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=sayMessage, type=1), afk = False)
			await ctx.send( '< 상태메세지 [' + sayMessage + ']로 변경완료 >', tts=False)
		else:
			return

	################ 보스타임 출력################ 
	@client.command(name=command[27][0], aliases=command[27][1:])
	async def bossTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours= 3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))
			
			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1000 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','
				else :
					aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
						aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(tmp_bossTime[i].strftime('%H:%M'))
						aa.append('-')	                                 #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                           #output_bossData[1] : 시간
						aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(bossTime[i].strftime('%H:%M')) 
						aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
					aa.append(bossData[i][7])	                         #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(fixed_bossTime[i].strftime('%H:%M'))
				aa.append('@')                                       #output_bossData[3] : @
				aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
				aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
				aa.append("")                                        #output_bossData[6] : 메세지
				ouput_bossData.append(aa)
				aa = []

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1000 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
						else : 
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'

			if len(boss_information) == 1 and len(tmp_boss_information) == 1:
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'
				###########################
				embed = discord.Embed(
						title = "----- 보스탐 정보 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				embed.add_field(
						name="----- 미예약 보스 -----",
						value= tmp_boss_information[0],
						inline = False
						)
				
				await ctx.send( embed=embed, tts=False)
			else : 
				###########################일반보스출력
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- 보스탐 정보 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(boss_information)-1):
					if len(boss_information[i+1]) != 0:
						boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
					else :
						boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)
				###########################미예약보스출력
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- 미예약 보스 -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)

			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
		else:
			return

	################ 보스타임 출력(고정보스포함) ################ 
	@client.command(name=command[28][0], aliases=command[28][1:])
	async def bossTime_fixed_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			fixed_datelist = []
			
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			datelist = list(set(datelist2))

			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1800 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','
				else :
					aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
						aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(tmp_bossTime[i].strftime('%H:%M'))
						aa.append('-')	                                 #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                           #output_bossData[1] : 시간
						aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(bossTime[i].strftime('%H:%M'))
						aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
					aa.append(bossData[i][7])	                         #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				fixed_datelist.append(fixed_bossTime[i])

			fixed_datelist = list(set(fixed_datelist))

			fixedboss_information = []
			cntF = 0
			fixedboss_information.append('')
					
			for timestring1 in sorted(fixed_datelist):
				if len(fixedboss_information[cntF]) > 1800 :
					fixedboss_information.append('')
					cntF += 1
				for i in range(fixed_bossNum):
					if timestring1 == fixed_bossTime[i]:
						if datetime.datetime.now().strftime('%Y-%m-%d') == fixed_bossTime[i].strftime('%Y-%m-%d'):
							tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M:%S') #초빼기 : tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M')
						else:
							tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M:%S') #초빼기 : tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M')
						fixedboss_information[cntF] = fixedboss_information[cntF] + tmp_timeSTR + ' : ' + fixed_bossData[i][0] + '\n'

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1800 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
						else : 
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'

			###########################고정보스출력
			if len(fixedboss_information[0]) != 0:
				fixedboss_information[0] = "```diff\n" + fixedboss_information[0] + "\n```"
			else :
				fixedboss_information[0] = '``` ```'

			embed = discord.Embed(
					title = "----- 고 정 보 스 -----",
					description= fixedboss_information[0],
					color=0x0000ff
					)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(fixedboss_information)-1):
				if len(fixedboss_information[i+1]) != 0:
					fixedboss_information[i+1] = "```diff\n" + fixedboss_information[i+1] + "\n```"
				else :
					fixedboss_information[i+1] = '``` ```'
				
				embed = discord.Embed(
						title = '',
						description= fixedboss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
			###########################일반보스출력
			if len(boss_information[0]) != 0:
				boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
			else :
				boss_information[0] = '``` ```'

			embed = discord.Embed(
					title = "----- 보스탐 정보 -----",
					description= boss_information[0],
					color=0x0000ff
					)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(boss_information)-1):
				if len(boss_information[i+1]) != 0:
					boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
				else :
					boss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= boss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
			###########################미예약보스출력
			if len(tmp_boss_information[0]) != 0:
				if len(tmp_boss_information) == 1:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
			else :
				tmp_boss_information[0] = '``` ```'

			embed = discord.Embed(
				title = "----- 미예약 보스 -----",
				description= tmp_boss_information[0],
				color=0x0000ff
				)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(tmp_boss_information)-1):
				if len(tmp_boss_information[i+1]) != 0:
					if i == len(tmp_boss_information)-2:
						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
					else:
						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"
				else :
					tmp_boss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= tmp_boss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)

			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
		else:
			return

	################ 킬초기화 확인 ################ 
	@client.command(name=command[29][0], aliases=command[29][1:])
	async def killInit_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global kill_Data

			kill_Data = {}

			await init_data_list('kill_list.ini', '-----척살명단-----')
			return await ctx.send( '< 킬 목록 초기화완료 >', tts=False)
		else:
			return

	################ 킬명단 확인 및 추가 ################ 
	@client.command(name=command[30][0], aliases=command[30][1:]) 
	async def killList_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global kill_Data

			if not args:
				kill_output = ''
				for key, value in kill_Data.items():
					kill_output += ':skull_crossbones: ' + str(key) + ' : ' + str(value) + '번 따히!\n'

				if kill_output != '' :
					embed = discord.Embed(
							description= str(kill_output),
							color=0xff00ff
							)
				else :
					embed = discord.Embed(
							description= '등록된 킬 목록이 없습니다. 분발하세요!',
							color=0xff00ff
							)
				return await ctx.send(embed=embed, tts=False)

			if args in kill_Data:
				kill_Data[args] += 1
			else:
				kill_Data[args] = 1
					
			embed = discord.Embed(
					description= ':skull_crossbones: ' + args + ' 따히! [' + str(kill_Data[args]) + '번]\n',
					color=0xff00ff
					)
			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 킬삭제 ################ 
	@client.command(name=command[31][0], aliases=command[31][1:])
	async def killDel_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global kill_Data

			if not args:
				return await ctx.send( '```제대로 된 아이디를 입력해주세요!\n```', tts=False)
			
			if args in kill_Data:
				del kill_Data[args]
				return await ctx.send( ':angel: ' + args + ' 삭제완료!', tts=False)
			else :				
				return await ctx.send( '```킬 목록에 등록되어 있지 않습니다!\n```', tts=False)
		else:
			return

	################ 킬 차감 ################ 
	@client.command(name=command[38][0], aliases=command[38][1:]) 
	async def killSubtract_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global kill_Data
			
			if not args:
				return await ctx.send(f'{command[38][0]} [아이디] 혹은 {command[38][0]} [아이디] [횟수] 양식에 맞춰 입력해주세요!', tts = False)

			input_data = args.split()
			
			if len(input_data) == 1:
				kill_name = args
				count = 1
			elif len(input_data) == 2:
				kill_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'[횟수]는 숫자로 입력바랍니다')
			else:
				return await ctx.send(f'{command[38][0]} [아이디] 혹은 {command[38][0]} [아이디] [횟수] 양식에 맞춰 입력해주세요!', tts = False)

			if kill_name in kill_Data:
				if kill_Data[kill_name] < int(count):
					return await ctx.send( f"등록된 킬 횟수[{str(kill_Data[kill_name])}번]보다 차감 횟수[{str(count)}번]가 많습니다. 킬 횟수에 맞게 재입력 바랍니다.", tts=False)
				else:
					kill_Data[kill_name] -= int(count)
			else:
				return await ctx.send( '```킬 목록에 등록되어 있지 않습니다!\n```', tts=False)
					
			embed = discord.Embed(
					description= f':angel: [{kill_name}] [{str(count)}번] 차감 완료! [잔여 : {str(kill_Data[kill_name])}번]\n',
					color=0xff00ff
					)
			
			if kill_Data[kill_name] == 0:
				del kill_Data[kill_name]

			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 경주 ################ 
	@client.command(name=command[32][0], aliases=command[32][1:])
	async def race_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[21]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			race_info = []
			fr = []
			racing_field = []
			str_racing_field = []
			cur_pos = []
			race_val = []
			random_pos = []
			racing_result = []
			output = ':camera: :camera: :camera: 신나는 레이싱! :camera: :camera: :camera:\n'
			#racing_unit = [':giraffe:', ':elephant:', ':tiger2:', ':hippopotamus:', ':crocodile:',':leopard:',':ox:', ':sheep:', ':pig2:',':dromedary_camel:',':dragon:',':rabbit2:'] #동물스킨
			#racing_unit = [':red_car:', ':taxi:', ':bus:', ':trolleybus:', ':race_car:', ':police_car:', ':ambulance:', ':fire_engine:', ':minibus:', ':truck:', ':articulated_lorry:', ':tractor:', ':scooter:', ':manual_wheelchair:', ':motor_scooter:', ':auto_rickshaw:', ':blue_car:', ':bike:', ':helicopter:', ':steam_locomotive:']  #탈것스킨
			#random.shuffle(racing_unit) 
			racing_member = msg.split(" ")

			racing_unit = []

			emoji = discord.Emoji
			emoji = ctx.message.guild.emojis

			for j in range(len(tmp_racing_unit)):
				racing_unit.append(':' + tmp_racing_unit[j] + ':')
				for i in range(len(emoji)):
					if emoji[i].name == tmp_racing_unit[j].strip(":") and tmp_racing_unit[j] != "" :
						racing_unit[j] = '<:' + tmp_racing_unit[j] + ':' + str(emoji[i].id) + '>'

			random.shuffle(racing_unit)

			field_size = 60
			tmp_race_tab = 35 - len(racing_member)
			if len(racing_member) <= 1:
				await ctx.send('레이스 인원이 2명보다 작습니다.')
				return
			elif len(racing_member) >= 13:
				await ctx.send('레이스 인원이 12명 초과입니다.')
				return
			else :
				race_val = random.sample(range(tmp_race_tab, tmp_race_tab+len(racing_member)), len(racing_member))
				random.shuffle(race_val)
				for i in range(len(racing_member)):
					fr.append(racing_member[i])
					fr.append(racing_unit[i])
					fr.append(race_val[i])
					race_info.append(fr)
					fr = []
					for i in range(field_size):
						fr.append(" ")
					racing_field.append(fr)
					fr = []

				for i in range(len(racing_member)):
					racing_field[i][0] = "|"
					racing_field[i][field_size-2] = race_info[i][1]
					if len(race_info[i][0]) > 5:
						racing_field[i][field_size-1] = "| " + race_info[i][0][:5] + '..'
					else:
						racing_field[i][field_size-1] = "| " + race_info[i][0]
					str_racing_field.append("".join(racing_field[i]))
					cur_pos.append(field_size-2)
				
				for i in range(len(racing_member)):
					output +=  str_racing_field[i] + '\n'

				result_race = await ctx.send(output + ':traffic_light: 3초 후 경주가 시작됩니다!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 2초 후 경주가 시작됩니다!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 1초 후 경주가 시작됩니다!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':checkered_flag:  경주 시작!')								

				for i in range(len(racing_member)):
					test = random.sample(range(2,field_size-2), race_info[i][2])
					while len(test) != tmp_race_tab + len(racing_member)-1 :
						test.append(1)
					test.append(1)
					test.sort(reverse=True)
					random_pos.append(test)

				for j in range(len(random_pos[0])):
					if j%2 == 0:
						output =  ':camera: :camera_with_flash: :camera: 신나는 레이싱! :camera_with_flash: :camera: :camera_with_flash:\n'
					else :
						output =  ':camera_with_flash: :camera: :camera_with_flash: 신나는 레이싱! :camera: :camera_with_flash: :camera:\n'
					str_racing_field = []
					for i in range(len(racing_member)):
						temp_pos = cur_pos[i]
						racing_field[i][random_pos[i][j]], racing_field[i][temp_pos] = racing_field[i][temp_pos], racing_field[i][random_pos[i][j]]
						cur_pos[i] = random_pos[i][j]
						str_racing_field.append("".join(racing_field[i]))

					await asyncio.sleep(1) 

					for i in range(len(racing_member)):
						output +=  str_racing_field[i] + '\n'
					
					await result_race.edit(content = output + ':checkered_flag:  경주 시작!')
				
				for i in range(len(racing_field)):
					fr.append(race_info[i][0])
					fr.append((race_info[i][2]) - tmp_race_tab + 1)
					racing_result.append(fr)
					fr = []

				result = sorted(racing_result, key=lambda x: x[1])

				result_str = ''
				for i in range(len(result)):
					if result[i][1] == 1:
						result[i][1] = ':first_place:'
					elif result[i][1] == 2:
						result[i][1] = ':second_place:'
					elif result[i][1] == 3:
						result[i][1] = ':third_place:'
					elif result[i][1] == 4:
						result[i][1] = ':four:'
					elif result[i][1] == 5:
						result[i][1] = ':five:'
					elif result[i][1] == 6:
						result[i][1] = ':six:'
					elif result[i][1] == 7:
						result[i][1] = ':seven:'
					elif result[i][1] == 8:
						result[i][1] = ':eight:'
					elif result[i][1] == 9:
						result[i][1] = ':nine:'
					elif result[i][1] == 10:
						result[i][1] = ':keycap_ten:'
					else:
						result[i][1] = ':x:'
					result_str += result[i][1] + "  " + result[i][0] + "  "
					
				#print(result)
				await asyncio.sleep(1)
				return await result_race.edit(content = output + ':tada: 경주 종료!\n' + result_str)
		else:
			return

	################ 채널설정 ################ 	
	@client.command(name=command[33][0], aliases=command[33][1:])
	async def set_channel_(ctx):
		global basicSetting

		msg = ctx.message.content[len(ctx.invoked_with)+1:]
		channel = ctx.message.channel.id #메세지가 들어온 채널 ID

		if msg == '사다리' : #사다리 채널 설정
			inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
			inputData_text = inidata_text.readlines()
			inidata_text.close()
		
			inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
			for i in range(len(inputData_text)):
				if inputData_text[i].startswith('ladderchannel'):
					inputData_text[i] = 'ladderchannel = ' +str(channel) + '\n'
					basicSetting[10] = channel
			
			inidata_text.writelines(inputData_text)
			inidata_text.close()

			print(f'< 사다리채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 사다리채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		elif msg == '정산' :
			inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
			inputData_text = inidata_text.readlines()
			inidata_text.close()
		
			inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
			for i in range(len(inputData_text)):
				if inputData_text[i].startswith('jungsanchannel'):
					inputData_text[i] = 'jungsanchannel = ' +str(channel) + '\n'
					basicSetting[13] = channel
			
			inidata_text.writelines(inputData_text)
			inidata_text.close()

			print(f'< 정산채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 정산채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		elif msg == '척살' :
			inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
			inputData_text = inidata_text.readlines()
			inidata_text.close()
		
			inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
			for i in range(len(inputData_text)):
				if inputData_text[i].startswith('killchannel'):
					inputData_text[i] = 'killchannel = ' +str(channel) + '\n'
					basicSetting[20] = channel
			
			inidata_text.writelines(inputData_text)
			inidata_text.close()

			print(f'< 척살채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 척살채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		elif msg == '경주' :
			inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
			inputData_text = inidata_text.readlines()
			inidata_text.close()
		
			inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
			for i in range(len(inputData_text)):
				if inputData_text[i].startswith('racingchannel'):
					inputData_text[i] = 'racingchannel = ' +str(channel) + '\n'
					basicSetting[21] = channel
			
			inidata_text.writelines(inputData_text)
			inidata_text.close()

			print(f'< 경주채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 경주채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		elif msg == '아이템' :
			inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
			inputData_text = inidata_text.readlines()
			inidata_text.close()
		
			inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
			for i in range(len(inputData_text)):
				if inputData_text[i].startswith('itemchannel'):
					inputData_text[i] = 'itemchannel = ' +str(channel) + '\n'
					basicSetting[22] = channel
			
			inidata_text.writelines(inputData_text)
			inidata_text.close()

			print(f'< 아이템채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 아이템채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		else :
			return await ctx.send(f'```올바른 명령어를 입력해주세요.```', tts=False)

	################ 아이템초기화 확인 ################ 
	@client.command(name=command[34][0], aliases=command[34][1:])
	async def itemInit_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[22]:
			global item_Data

			item_Data = {}

			await init_data_list('item_list.ini', '-----아이템 목록-----')
			return await ctx.send( '< 아이템 목록 초기화완료 >', tts=False)
		else:
			return

	################ 아이템 목록 확인 및 추가 ################ 
	@client.command(name=command[35][0], aliases=command[35][1:]) 
	async def itemList_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[22]:
			global item_Data

			if not args:
				sorted_item_list = sorted(item_Data.items(), key=lambda x: x[0])

				embed = discord.Embed(title = '', description = f'`{client.user.name}\'s 창고`', color = 0x00ff00)

				if len(sorted_item_list) > 0 :
					for item_id, count in sorted_item_list:
						embed.add_field(name = item_id, value = count)
				else :
					embed.add_field(name = '\u200b\n', value = '창고가 비었습니다.\n\u200b')

				embed.set_footer(text = f"전체 아이템 종류  :  {len(item_Data)}개")
				return await ctx.send(embed=embed, tts=False)

			input_data = args.split()
			
			if len(input_data) == 1:
				item_name = args
				count = 1
			elif len(input_data) == 2:
				item_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'아이템 [개수]는 숫자로 입력바랍니다')
			else:
				return await ctx.send(f'{command[35][0]} [아이템명] 혹은 {command[35][0]} [아이템명] [개수] 양식에 맞춰 입력해주세요!', tts = False)	

			if item_name in item_Data:
				item_Data[item_name] += int(count)
			else:
				item_Data[item_name] = int(count)
					
			embed = discord.Embed(
					description= f':inbox_tray: **[{item_name}] [{str(count)}개]** 등록 완료! [잔여 : {str(item_Data[item_name])}개]\n',
					color=0xff00ff
					)
			return await ctx.send(embed=embed, tts=False)

		else:
			return

	################ 아이템 삭제 ################ 
	@client.command(name=command[36][0], aliases=command[36][1:])
	async def itemDel_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[22]:
			global item_Data

			if not args:
				return await ctx.send( f'{command[36][0]} [아이템명] 양식에 맞춰 입력해주세요!', tts = False)

			if args in item_Data:
				del item_Data[args]
				embed = discord.Embed(
					description= ':outbox_tray: ' + args + ' 삭제완료!',
					color=0xff00ff
					)
				return await ctx.send(embed=embed, tts=False)
			else :				
				return await ctx.send( '```아이템 목록에 등록되어 있지 않습니다!\n```', tts=False)
		else:
			return

	################ 아이템 차감 ################ 
	@client.command(name=command[37][0], aliases=command[37][1:]) 
	async def itemSubtract_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[22]:
			global item_Data

			if not args:
				return await ctx.send(f'{command[37][0]} [아이템명] 혹은 {command[37][0]} [아이템명] [개수] 양식에 맞춰 입력해주세요!', tts = False)

			input_data = args.split()
			
			if len(input_data) == 1:
				item_name = args
				count = 1
			elif len(input_data) == 2:
				item_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'아이템 [개수]는 숫자로 입력바랍니다')
			else:
				return await ctx.send(f'{command[37][0]} [아이템명] 혹은 {command[37][0]} [아이템명] [개수] 양식에 맞춰 입력해주세요!', tts = False)	

			if item_name in item_Data:
				if item_Data[item_name] < int(count):
					return await ctx.send( f"등록된 아이템 개수[{str(item_Data[item_name])}개]보다 차감 개수[{str(count)}개]가 많습니다. 등록 개수에 맞게 재입력 바랍니다.", tts=False)
				else:
					item_Data[item_name] -= int(count)
			else:
				return await ctx.send( '```아이템 목록에 등록되어 있지 않습니다!\n```', tts=False)
					
			embed = discord.Embed(
					description= f':outbox_tray: **[{item_name}] [{str(count)}개]** 차감 완료! [잔여 : {str(item_Data[item_name])}개]\n',
					color=0xff00ff
					)
			
			if item_Data[item_name] == 0:
				del item_Data[item_name]

			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ ?????????????? ################ 
	@client.command(name='!오빠')
	async def brother1_(ctx):
		await PlaySound(voice_client1, './sound/오빠.mp3')

	@client.command(name='!언니')
	async def sister_(ctx):
		await PlaySound(voice_client1, './sound/언니.mp3')

	@client.command(name='!형')
	async def brother2_(ctx):
		await PlaySound(voice_client1, './sound/형.mp3')
	
	@client.command(name='!TJ', aliases=['!tj'])
	async def TJ_(ctx):
		resultTJ = random.randrange(1,9)
		await PlaySound(voice_client1, './sound/TJ' + str(resultTJ) +'.mp3')

	@client.event
	async def on_command_error(ctx, error):
		if isinstance(error, CommandNotFound):
			return
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			return
		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			return await ctx.send(f"**[{ctx.message.content}]** 명령을 사용할 권한이 없습니다.!")
		raise error

	@client.event
	async def on_message(msg):
		await client.wait_until_ready()
		
		if msg.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
			return None #동작하지 않고 무시합니다.

		ori_msg = msg

		global channel
		
		global basicSetting
		global bossData
		global fixed_bossData

		global bossNum
		global fixed_bossNum
		global chkvoicechannel
		global chkrelogin

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		global voice_client1
		
		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type
		
		global chflg
		global LoadChk

		global katalkData
		global InitkatalkData
		global indexBossname
		global indexFixedBossname
		global FixedBossDateData

		global gc #정산
		global credentials	#정산
		
		global regenembed
		global command
		global kill_Data

		id = msg.author.id

		if chflg == 1 :
			if client.get_channel(basicSetting[7]).id == msg.channel.id:
				channel = basicSetting[7]
				message = msg

				hello = message.content

				for i in range(bossNum):
					################ 보스 컷처리 ################ 
					# if message.content.startswith(bossData[i][0] +'컷'):
					if message.content.startswith(bossData[i][0] +'컷') or message.content.startswith(convertToInitialLetters(bossData[i][0] +'컷')) or message.content.startswith(bossData[i][0] +' 컷') or message.content.startswith(convertToInitialLetters(bossData[i][0] +' 컷')):
						if hello.find('  ') != -1 :
							bossData[i][7] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][7] = ''

						tmp_msg = bossData[i][0] +'컷'
										
						if len(hello) > len(tmp_msg) + 3 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now()
								tmp_now = datetime.datetime.now()
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]	
								now2 = datetime.datetime.now()
								tmp_now = datetime.datetime.now()
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							now2 = datetime.datetime.now()
							tmp_now = now2
							
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0

						if tmp_now > now2 :
							tmp_now = tmp_now + datetime.timedelta(days=int(-1))
							
						if tmp_now < now2 : 
							deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							while now2 > tmp_now :
								tmp_now = tmp_now + deltaTime
								bossMungCnt[i] = bossMungCnt[i] + 1
							now2 = tmp_now
							bossMungCnt[i] = bossMungCnt[i] - 1
						else :
							now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
									
						tmp_bossTime[i] = bossTime[i] = nextTime = now2
						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
						embed = discord.Embed(
								description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
								color=0xff0000
								)
						await client.get_channel(channel).send( embed=embed, tts=False)
						await dbSave()
						
					################ 보스 멍 처리 ################ 
					if message.content.startswith(bossData[i][0] +'멍') or message.content.startswith(bossData[i][0] +' 멍'):
						if hello.find('  ') != -1 :
							bossData[i][7] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][7] = ''
							
						tmp_msg = bossData[i][0] +'멍'
						tmp_now = datetime.datetime.now()

						if len(hello) > len(tmp_msg) + 3 :
							temptime = tmp_now
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos] 
								minutes1 = hello[chkpos+1:chkpos+3]					
								temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]					
								temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							
							bossMungCnt[i] = 0
							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False

							if temptime > tmp_now :
								temptime = temptime + datetime.timedelta(days=int(-1))

							if temptime < tmp_now :
								deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								while temptime < tmp_now :
									temptime = temptime + deltaTime
									bossMungCnt[i] = bossMungCnt[i] + 1
							else:
								temptime = temptime

							tmp_bossTime[i] = bossTime[i] = temptime				

							tmp_bossTimeString[i] = bossTimeString[i] = temptime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = temptime.strftime('%Y-%m-%d')
							embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
							await client.get_channel(channel).send(embed=embed, tts=False)
							await dbSave()
						else:
							if tmp_bossTime[i] < tmp_now :

								nextTime = tmp_bossTime[i] + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1

								tmp_bossTime[i] = bossTime[i] = nextTime				

								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
										description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
										color=0xff0000
										)
								await client.get_channel(channel).send(embed=embed, tts=False)
								await dbSave()
							else:
								await client.get_channel(channel).send('```' + bossData[i][0] + '탐이 아직 안됐습니다. 다음 ' + bossData[i][0] + '탐 [' + tmp_bossTimeString[i] + '] 입니다```', tts=False)
					
					################ 예상 보스 타임 입력 ################ 

					if message.content.startswith(bossData[i][0] +'예상') or message.content.startswith(bossData[i][0] +' 예상'):
						if hello.find('  ') != -1 :
							bossData[i][7] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][7] = ''
						
						tmp_msg = bossData[i][0] +'예상'
						if len(hello) > len(tmp_msg) + 4 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now()
								tmp_now = datetime.datetime.now()
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]
								now2 = datetime.datetime.now()
								tmp_now = datetime.datetime.now()
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))

							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = 0

							if tmp_now < now2 :
								tmp_now = tmp_now + datetime.timedelta(days=int(1))
										
							tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							embed = discord.Embed(
									description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
									color=0xff0000
									)
							await client.get_channel(channel).send(embed=embed, tts=False)
							await dbSave()
						else:
							await client.get_channel(channel).send('```' + bossData[i][0] + ' 예상 시간을 입력해주세요.```')
						
					################ 보스타임 삭제 ################ 
						
					if message.content == bossData[i][0] +'삭제' or message.content == bossData[i][0] +' 삭제':
						bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365)
						tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365)
						bossTimeString[i] = '99:99:99'
						bossDateString[i] = '9999-99-99'
						tmp_bossTimeString[i] = '99:99:99'
						tmp_bossDateString[i] = '9999-99-99'
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0
						await client.get_channel(channel).send('<' + bossData[i][0] + ' 삭제완료>', tts=False)
						await dbSave()
						print ('<' + bossData[i][0] + ' 삭제완료>')

					################ 보스별 메모 ################ 

					if message.content.startswith(bossData[i][0] +'메모 '):
						
						tmp_msg = bossData[i][0] +'메모 '
						
						bossData[i][7] = hello[len(tmp_msg):]
						await client.get_channel(channel).send('< ' + bossData[i][0] + ' [ ' + bossData[i][7] + ' ] 메모등록 완료>', tts=False)

					if message.content.startswith(bossData[i][0] +'메모삭제'):
						
						bossData[i][7] = ''
						await client.get_channel(channel).send('< ' + bossData[i][0] + ' 메모삭제 완료>', tts=False)

					################ 보스별 카톡 켬/끔 ################ 

					if message.content.startswith(bossData[i][0] +'카톡끔'):
						bossData[i][6] = '0'
						KakaoAlertSave(bossData[i][0], bossData[i][6])
						await client.get_channel(channel).send('< ' + bossData[i][0] + ' 카톡 보내기 끔>', tts=False)

					if message.content.startswith(bossData[i][0] +'카톡켬'):
						bossData[i][6] = '1'
						KakaoAlertSave(bossData[i][0], bossData[i][6])
						await client.get_channel(channel).send('< ' + bossData[i][0] + ' 카톡 보내기 켬>', tts=False)

		await client.process_commands(ori_msg)

	client.loop.create_task(task())
	try:
		client.loop.run_until_complete(client.start(token))
	except SystemExit:
		handle_exit()
	except KeyboardInterrupt:
		handle_exit()

	print("Bot restarting")
	client = discord.Client(loop=client.loop)
	client = commands.Bot(command_prefix="", help_command = None, description='일상디코봇')
	# 일상브랜치 마지막