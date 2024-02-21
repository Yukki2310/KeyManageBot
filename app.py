import sys
from os import getenv
import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

# 管理用discordチャンネルのid
textchannel = "Channel_Id"
# 制御用フラグ
keyState = 0

##
## 初期化
##
@bot.event
async def on_ready():
    global keyState
    keyState = 0

    # 管理チャンネルを取得
    botRoom = bot.get_channel(textchannel)

    # 初期メッセージを送信
    embed = discord.Embed( # Embedを定義する
                        title="鍵貸し出し待機中",# タイトル
                        color=0x87cefa # フレーム色指定
                        )
    embed.add_field(name="鍵を借りたら，下のリアクションボタンを押してください",value="") # フィールドを追加。

    await botRoom.send(embed=embed)

    # 送信したメッセージを取得し、リアクションをつける
    infomessage = await botRoom.fetch_message(botRoom.last_message_id)
    await infomessage.add_reaction("\N{Key}")

##
##  リアクションへの反応
##
@bot.event
async def on_raw_reaction_add(payload):
    global keyState

    # 管理チャンネルを取得
    botRoom = bot.get_channel(textchannel)
    # リアクションが押されたチャンネルとメッセージを取得
    react_channel = bot.get_channel(payload.channel_id)
    react_message = await react_channel.fetch_message(payload.message_id)

    #
    # 鍵貸し出し時
    #
    # 管理チャンネルとリアクションが押されたチャンネルが一致
    # リアクションを押したメンバがbotではない
    # 貸し出しフラグfalse
    # 開放フラグfalse
    if (textchannel == payload.channel_id and
            payload.member.bot is False and
            keyState == 0):

        #リアクションしたメンバを鍵の持ち主に
        owner = payload.member
        #UTCを取得
        dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)

        # 貸し出しメッセージを送信
        embed = discord.Embed(
                            title="鍵持ち出し中",
                            color=0x90ee90
                            )
        embed.add_field(name="【" + str(dt_now.hour) + "時" + str(dt_now.minute) + "分" + "】",
                        value=owner.display_name + "が鍵を借りました。部室を開けたら，下のリアクションボタンを押してください。") # フィールドを追加。
        await botRoom.send(embed=embed)

        #送信したメッセージを取得し、リアクションをつける
        infomessage = await botRoom.fetch_message(botRoom.last_message_id)
        await infomessage.add_reaction("\N{Key}")

        #貸し出しフラグを切り替え
        keyState = 1
        
        return
    
    #
    # 解錠時
    #
    # 管理チャンネルとリアクションが押されたチャンネルが一致
    # リアクションを押したメンバがbotではない
    # 貸し出しフラグtrue
    # 開放フラグfalse
    if (textchannel == payload.channel_id and
            payload.member.bot is False and
            keyState == 1):

        # リアクションしたメンバを鍵の持ち主に
        owner = payload.member
        # UTCを取得
        dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)

        # 解錠メッセージを送信
        embed = discord.Embed(
                            title="部室開錠中",
                            color=0x1e90ff
                            )
        embed.add_field(name="【" + str(dt_now.hour) + "時" + str(dt_now.minute) + "分" + "】",
                        value=owner.display_name + "が部室を開けました。施錠したら，下のリアクションボタンを押してください。")
        await botRoom.send(embed=embed)
        
        #　送信したメッセージを取得し、リアクションをつける
        infomessage = await botRoom.fetch_message(botRoom.last_message_id)
        await infomessage.add_reaction("\N{Key}")

        #　貸し出しフラグを切り替え
        keyState = 2
        
        return

    #
    # 施錠時
    #
    # 管理チャンネルとリアクションが押されたチャンネルが一致
    # リアクションを押したメンバがbotではない
    # 貸し出しフラグtrue
    # 開放フラグtrue
    if (textchannel == payload.channel_id and
            payload.member.bot is False and
            keyState == 2):

        #リアクションしたメンバを鍵の持ち主に
        owner = payload.member
        #UTCを取得
        dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)

        #施錠メッセージを送信
        embed = discord.Embed( # Embedを定義する
                            title="部室施錠中",# タイトル
                            color=0xffff00 # フレーム色指定
                            )
        embed.add_field(name="【" + str(dt_now.hour) + "時" + str(dt_now.minute) + "分" + "】",
                        value=owner.display_name + "が部室を施錠しました。鍵を返却したら，下のリアクションボタンを押してください。") # フィールドを追加。
        await botRoom.send(embed=embed)
        
        
        #送信したメッセージを取得し、リアクションをつける
        infomessage = await botRoom.fetch_message(botRoom.last_message_id)
        await infomessage.add_reaction("\N{Key}")

        #貸し出しフラグを切り替え
        keyState = 3
        
        return

    #
    # 鍵返却時
    #
    # 管理チャンネルとリアクションが押されたチャンネルが一致
    # リアクションを押したメンバがbotではない
    # 貸し出しフラグtrue
    # 開放フラグfalse
    if (textchannel == payload.channel_id and
            payload.member.bot is False and
            keyState == 3):

        #リアクションしたメンバを鍵の返却者に
        owner = payload.member
        
        #UTCを取得
        dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        
        #返却メッセージを送信
        embed = discord.Embed( # Embedを定義する
                            title="鍵返却完了",# タイトル
                            color=0xff6347 # フレーム色指定
                            )
        embed.add_field(name="【" + str(dt_now.hour) + "時" + str(dt_now.minute) + "分" + "】",
                        value=owner.display_name + "が鍵を返却しました。") # フィールドを追加。
        await botRoom.send(embed=embed)

        #初期状態に戻る
        await on_ready()

# Botのトークンを指定
token = getenv('TOKEN')
bot.run(token)