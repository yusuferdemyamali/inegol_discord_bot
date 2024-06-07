import discord
from discord import app_commands
from discord.ext import commands
import pymongo
from config import *
import datetime
import pytz
import locale
import asyncio
import os
import google.generativeai as genai
from discord.ui import Button, View
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
locale.setlocale(locale.LC_ALL, 'turkish') 

genai.configure(api_key= gemini_api)

client = pymongo.MongoClient(url)
db = client.user_data
collection = db.jailed_members
bot = commands.Bot(command_prefix=prefix, intents=intents)


istanbul_zaman = pytz.timezone("Europe/Istanbul")
istanbul_tarih = datetime.datetime.now(istanbul_zaman)
tarih = istanbul_tarih.strftime("%d/%m/%Y %H.%M.%S")


#GPT
@bot.tree.command(name="gpt", description="gpt")
async def gpt(interaction: discord.Interaction, yazi: str):
    await interaction.response.defer()
    generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    ]

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings = safety_settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(yazi)
    await asyncio.sleep(delay=0)
    await interaction.followup.send(response.text)

#Kayıt
@bot.tree.context_menu(name="Kayıt")
async def kayit(interaction: discord.Interaction, member: discord.Member):
    istanbul_zaman2 = pytz.timezone("Europe/Istanbul")
    istanbul_tarih2 = datetime.datetime.now(istanbul_zaman2)
    tarih2 = istanbul_tarih2.strftime("%d/%m/%Y")
    role = interaction.guild.get_role(kayit_yetkili)
    role2 = interaction.guild.get_role(birinci_klan_rol_id)
    role3 = interaction.guild.get_role(ikinci_klan_rol_id)
    role4 = interaction.guild.get_role(ucuncu_klan_rol_id)
    role5 = interaction.guild.get_role(dorduncu_klan_rol_id)
    role6 = interaction.guild.get_role(besinci_klan_rol_id)
    role7 = interaction.guild.get_role(altinci_klan_rol_id)
    member2 = member.id
    hex = {"Member_id": member2}
    hex2 = {"Staff_id": interaction.user.id}
    hex3 = {"$inc": {"birinciklan_reg": +1}}
    hex4 = {"$inc": {"ikinciklan_reg": +1}}
    hex5 = {"$inc": {"Total_reg": +1}}
    hex6 = {"$inc": {"ucuncuklan_reg": +1}}
    hex7 = {"$inc": {"dorduncuklan_reg": +1}}
    hex8 = {"$inc": {"besinciklan_reg": +1}}
    hex9 = {"$inc": {"altinciklan_reg": +1}}
    user_list = db.user_info.find(hex)
    mes = '\nKayıt datası:'
    for i in user_list:
        mes = mes + '\n' + ', ' + i['Klan'] + ', ' + i['Date'] + '\n-----------------------------'
    if role not in interaction.user.roles:
        embed = discord.Embed(
            title = "Erişim Reddedildi",
            description = f'{interaction.user.mention} Bu komutu kullanma iznin yok.',
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(f'{interaction.user.mention}', embed=embed)
    elif db.black_list.count_documents(hex) > 0:
        await interaction.response.send_message(f"https://tenor.com/view/hello-bears-gif-4039502")
    elif interaction.user.id == member.id:
        await interaction.response.send_message(f'{interaction.user.mention} Kendini kayıt edemezsin.', ephemeral=True)
    elif role2 in member.roles:
        await interaction.response.send_message(f'{member.mention} üyesi zaten kayıtlı', ephemeral=True)
    elif role3 in member.roles:
        await interaction.response.send_message(f'{member.mention} üyesi zaten kayıtlı', ephemeral=True)
    elif role4 in member.roles:
        await interaction.response.send_message(f'{member.mention} üyesi zaten kayıtlı', ephemeral=True)
    elif role5 in member.roles:
        await interaction.response.send_message(f'{member.mention} üyesi zaten kayıtlı', ephemeral=True)    
    elif role6 in member.roles:
        await interaction.response.send_message(f'{member.mention} üyesi zaten kayıtlı', ephemeral=True)    
    elif role7 in member.roles:
        await interaction.response.send_message(f'{member.mention} üyesi zaten kayıtlı', ephemeral=True)    
    else:
        button1 = Button(label="birinciklan", style=discord.ButtonStyle.green, custom_id="birinciklan")
        button2 = Button(label="ikinciklan", style=discord.ButtonStyle.green, custom_id="ikinciklan")
        button3 = Button(label="ucuncuklan", style=discord.ButtonStyle.green, custom_id="ucuncuklan")
        button4 = Button(label="dorduncuklan", style=discord.ButtonStyle.green, custom_id="dorduncuklan")
        button5 = Button(label="besinciklan", style=discord.ButtonStyle.green, custom_id="besinciklan")
        button6 = Button(label="altinciklan", style=discord.ButtonStyle.green, custom_id="altinciklan")

        async def button1_callback(interaction):
            role = interaction.guild.get_role(birinci_klan_rol_id)
            role2 = interaction.guild.get_role(kayitsiz_rol_id)
            role3 = interaction.guild.get_role(supheli_rol_id)
            log_ch = interaction.guild.get_channel(log_kanal_id)
            nick = member.display_name
            kayit_embed = discord.Embed(
                title = "Kayıt işlemi başarılı",
                description = f'``{member}`` adlı kullanıcı birinciklan olarak kaydedildi\nüyeye <@&{birinci_klan_rol_id}> rolünü verdim.',
                colour = discord.Colour.green()
            )
            log_embed = discord.Embed(
                title = "Bir kayıt işlemi yapıldı",
                description = f'● Kayıt yetkilisi: ``{interaction.user}``\n● Kayıt yetkilisi id: ``{interaction.user.id}``\n● Kayıt olan üye: ``{member}``\n● Kayıt olan üye id: ``{member.id}``\n● Klan: ``birinciklan``\n● Kayıt tarihi: ``{tarih}``',
                colour = discord.Colour.blue()
            )
            await member.add_roles(role)
            await member.remove_roles(role2)
            await member.remove_roles(role3)
            await interaction.response.edit_message(embed=kayit_embed, view=None)
            await log_ch.send(embed=log_embed)
            try:
                await member.send("kaydını yaptim he takil.")
            except:
                print("kullanıca dm atılmıo")
            db.user_info.insert_one(
                {
                    "Staff_id": interaction.user.id,
                    "Member_id": member.id,
                    "Klan": "birinciklan",
                    "Nick": nick,
                    "Date": tarih2,
                }
            )
            if db.register_data.count_documents(hex2) == 0:
                    db.register_data.insert_one(
                        {
                            "Staff_id": interaction.user.id,
                            "Total_reg": 1,
                            "birinciklan_reg": 1,
                            "ikinciklan_reg": 0,
                            "ucuncuklan_reg": 0,
                            "dorduncuklan_reg": 0,
                            "besinciklan_reg": 0,
                            "altinciklan_reg": 0,
                            "Status": "open",
                        }
                    )
            elif db.register_data.count_documents(hex2) > 0:
                db.register_data.update_one(hex2, hex3)
                db.register_data.update_one(hex2, hex5) 
            
        async def button2_callback(interaction):
            role = interaction.guild.get_role(ikinci_klan_rol_id)
            role2 = interaction.guild.get_role(kayitsiz_rol_id)
            role3 = interaction.guild.get_role(supheli_rol_id)
            log_ch = interaction.guild.get_channel(log_kanal_id)
            nick = member.display_name
            kayit_embed = discord.Embed(
                title = "Kayıt işlemi başarılı",
                description = f'``{member}`` adlı kullanıcı ikinciklan olarak kaydedildi\nüyeye <@&{ikinci_klan_rol_id}> rolünü verdim.',
                colour = discord.Colour.green()
            )
            log_embed = discord.Embed(
                title = "Bir kayıt işlemi yapıldı",
                description = f'● Kayıt yetkilisi: ``{interaction.user}``\n● Kayıt yetkilisi id: ``{interaction.user.id}``\n● Kayıt olan üye: ``{member}``\n● Kayıt olan üye id: ``{member.id}``\n● Kayıt tarihi: ``{tarih}``',
                colour = discord.Colour.blue()
            )
            await member.add_roles(role)
            await member.remove_roles(role2)
            await member.remove_roles(role3)
            await interaction.response.edit_message(embed=kayit_embed, view=None)
            await log_ch.send(embed=log_embed)
            try:
                await member.send("kaydını yaptim he takil.")
            except:
                print("kullanıca dm atılmıo")
            db.user_info.insert_one(
                {
                    "Staff_id": interaction.user.id,
                    "Member_id": member.id,
                    "Klan": "ikinciklan",
                    "Nick": nick,
                    "Date": tarih2,
                }
            )
            if db.register_data.count_documents(hex2) == 0:
                    db.register_data.insert_one(
                        {
                            "Staff_id": interaction.user.id,
                            "Total_reg": 1,
                            "birinciklan_reg": 0,
                            "ikinciklan_reg": 1,
                            "ucuncuklan_reg": 0,
                            "dorduncuklan_reg": 0,
                            "besinciklan_reg": 0,
                            "altinciklan_reg": 0,
                            "Status": "open",
                        }
                    )
            elif db.register_data.count_documents(hex2) > 0:
                db.register_data.update_one(hex2, hex4)
                db.register_data.update_one(hex2, hex5) 

        async def button3_callback(interaction):
            role = interaction.guild.get_role(ucuncu_klan_rol_id)
            role2 = interaction.guild.get_role(kayitsiz_rol_id)
            role3 = interaction.guild.get_role(supheli_rol_id)
            log_ch = interaction.guild.get_channel(log_kanal_id)
            nick = member.display_name
            kayit_embed = discord.Embed(
                title = "Kayıt işlemi başarılı",
                description = f'``{member}`` adlı kullanıcı ucuncuklan olarak kaydedildi\nüyeye <@&{ucuncu_klan_rol_id}> rolünü verdim.',
                colour = discord.Colour.green()
            )
            log_embed = discord.Embed(
                title = "Bir kayıt işlemi yapıldı",
                description = f'● Kayıt yetkilisi: ``{interaction.user}``\n● Kayıt yetkilisi id: ``{interaction.user.id}``\n● Kayıt olan üye: ``{member}``\n● Kayıt olan üye id: ``{member.id}``\n● Klan: ``ucuncuklan``\n● Kayıt tarihi: ``{tarih}``',
                colour = discord.Colour.blue()
            )
            await member.add_roles(role)
            await member.remove_roles(role2)
            await member.remove_roles(role3)
            await interaction.response.edit_message(embed=kayit_embed, view=None)
            await log_ch.send(embed=log_embed)
            try:
                await member.send("kaydını yaptim he takil.")
            except:
                print("kullanıca dm atılmıo")
            db.user_info.insert_one(
                {
                    "Staff_id": interaction.user.id,
                    "Member_id": member.id,
                    "Klan": "ucuncuklan",
                    "Nick": nick,
                    "Date": tarih2,
                }
            )
            if db.register_data.count_documents(hex2) == 0:
                    db.register_data.insert_one(
                        {
                            "Staff_id": interaction.user.id,
                            "Total_reg": 1,
                            "birinciklan_reg": 0,
                            "ikinciklan_reg": 0,
                            "ucuncuklan_reg": 1,
                            "dorduncuklan_reg": 0,
                            "besinciklan_reg": 0,
                            "altinciklan_reg": 0,
                            "Status": "open",
                        }
                    )
            elif db.register_data.count_documents(hex2) > 0:
                db.register_data.update_one(hex2, hex6)
                db.register_data.update_one(hex2, hex5)         

        async def button4_callback(interaction):
            role = interaction.guild.get_role(dorduncu_klan_rol_id)
            role2 = interaction.guild.get_role(kayitsiz_rol_id)
            role3 = interaction.guild.get_role(supheli_rol_id)
            log_ch = interaction.guild.get_channel(log_kanal_id)
            nick = member.display_name
            kayit_embed = discord.Embed(
                title = "Kayıt işlemi başarılı",
                description = f'``{member}`` adlı kullanıcı dorduncuklan olarak kaydedildi\nüyeye <@&{dorduncu_klan_rol_id}> rolünü verdim.',
                colour = discord.Colour.green()
            )
            log_embed = discord.Embed(
                title = "Bir kayıt işlemi yapıldı",
                description = f'● Kayıt yetkilisi: ``{interaction.user}``\n● Kayıt yetkilisi id: ``{interaction.user.id}``\n● Kayıt olan üye: ``{member}``\n● Kayıt olan üye id: ``{member.id}``\n● Klan: ``dorduncuklan``\n● Kayıt tarihi: ``{tarih}``',
                colour = discord.Colour.blue()
            )
            await member.add_roles(role)
            await member.remove_roles(role2)
            await member.remove_roles(role3)
            await interaction.response.edit_message(embed=kayit_embed, view=None)
            await log_ch.send(embed=log_embed)
            try:
                await member.send("kaydını yaptim he takil.")
            except:
                print("kullanıca dm atılmıo")
            db.user_info.insert_one(
                {
                    "Staff_id": interaction.user.id,
                    "Member_id": member.id,
                    "Klan": "dorduncuklan",
                    "Nick": nick,
                    "Date": tarih2,
                }
            )
            if db.register_data.count_documents(hex2) == 0:
                    db.register_data.insert_one(
                        {
                            "Staff_id": interaction.user.id,
                            "Total_reg": 1,
                            "birinciklan_reg": 0,
                            "ikinciklan_reg": 0,
                            "ucuncuklan_reg": 0,
                            "dorduncuklan_reg": 1,
                            "besinciklan_reg": 0,
                            "altinciklan_reg": 0,
                            "Status": "open",
                        }
                    )
            elif db.register_data.count_documents(hex2) > 0:
                db.register_data.update_one(hex2, hex7)
                db.register_data.update_one(hex2, hex5)                 

        async def button5_callback(interaction):
            role = interaction.guild.get_role(besinci_klan_rol_id)
            role2 = interaction.guild.get_role(kayitsiz_rol_id)
            role3 = interaction.guild.get_role(supheli_rol_id)
            log_ch = interaction.guild.get_channel(log_kanal_id)
            nick = member.display_name
            kayit_embed = discord.Embed(
                title = "Kayıt işlemi başarılı",
                description = f'``{member}`` adlı kullanıcı besinciklan olarak kaydedildi\nüyeye <@&{besinci_klan_rol_id}> rolünü verdim.',
                colour = discord.Colour.green()
            )
            log_embed = discord.Embed(
                title = "Bir kayıt işlemi yapıldı",
                description = f'● Kayıt yetkilisi: ``{interaction.user}``\n● Kayıt yetkilisi id: ``{interaction.user.id}``\n● Kayıt olan üye: ``{member}``\n● Kayıt olan üye id: ``{member.id}``\n● Klan: ``besinciklan``\n● Kayıt tarihi: ``{tarih}``',
                colour = discord.Colour.blue()
            )
            await member.add_roles(role)
            await member.remove_roles(role2)
            await member.remove_roles(role3)
            await interaction.response.edit_message(embed=kayit_embed, view=None)
            await log_ch.send(embed=log_embed)
            try:
                await member.send("kaydını yaptim he takil.")
            except:
                print("kullanıca dm atılmıo")
            db.user_info.insert_one(
                {
                    "Staff_id": interaction.user.id,
                    "Member_id": member.id,
                    "Klan": "besinciklan",
                    "Nick": nick,
                    "Date": tarih2,
                }
            )
            if db.register_data.count_documents(hex2) == 0:
                    db.register_data.insert_one(
                        {
                            "Staff_id": interaction.user.id,
                            "Total_reg": 1,
                            "birinciklan_reg": 0,
                            "ikinciklan_reg": 0,
                            "ucuncuklan_reg": 0,
                            "dorduncuklan_reg": 0,
                            "besinciklan_reg": 1,
                            "altinciklan_reg": 0,
                            "Status": "open",
                        }
                    )
            elif db.register_data.count_documents(hex2) > 0:
                db.register_data.update_one(hex2, hex8)
                db.register_data.update_one(hex2, hex5)           
                

        async def button6_callback(interaction):
            role = interaction.guild.get_role(altinci_klan_rol_id)
            role2 = interaction.guild.get_role(kayitsiz_rol_id)
            role3 = interaction.guild.get_role(supheli_rol_id)
            log_ch = interaction.guild.get_channel(log_kanal_id)
            nick = member.display_name
            kayit_embed = discord.Embed(
                title = "Kayıt işlemi başarılı",
                description = f'``{member}`` adlı kullanıcı altinciklan olarak kaydedildi\nüyeye <@&{altinci_klan_rol_id}> rolünü verdim.',
                colour = discord.Colour.green()
            )
            log_embed = discord.Embed(
                title = "Bir kayıt işlemi yapıldı",
                description = f'● Kayıt yetkilisi: ``{interaction.user}``\n● Kayıt yetkilisi id: ``{interaction.user.id}``\n● Kayıt olan üye: ``{member}``\n● Kayıt olan üye id: ``{member.id}``\n● Klan: ``altinciklan``\n● Kayıt tarihi: ``{tarih}``',
                colour = discord.Colour.blue()
            )
            await member.add_roles(role)
            await member.remove_roles(role2)
            await member.remove_roles(role3)
            await interaction.response.edit_message(embed=kayit_embed, view=None)
            await log_ch.send(embed=log_embed)
            try:
                await member.send("kaydını yaptim he takil.")
            except:
                print("kullanıca dm atılmıo")
            db.user_info.insert_one(
                {
                    "Staff_id": interaction.user.id,
                    "Member_id": member.id,
                    "Klan": "altinciklan",
                    "Nick": nick,
                    "Date": tarih2,
                }
            )
            if db.register_data.count_documents(hex2) == 0:
                    db.register_data.insert_one(
                        {
                            "Staff_id": interaction.user.id,
                            "Total_reg": 1,
                            "birinciklan_reg": 0,
                            "ikinciklan_reg": 0,
                            "ucuncuklan_reg": 0,
                            "dorduncuklan_reg": 0,
                            "besinciklan_reg": 0,
                            "altinciklan_reg": 1,
                            "Status": "open",
                        }
                    )
            elif db.register_data.count_documents(hex2) > 0:
                db.register_data.update_one(hex2, hex9)
                db.register_data.update_one(hex2, hex5)        


        

        button1.callback = button1_callback
        button2.callback = button2_callback
        button3.callback = button3_callback
        button4.callback = button4_callback
        button5.callback = button5_callback
        button6.callback = button6_callback

        view = View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)
        view.add_item(button6)
        inegol_register_embed = discord.Embed(
            title = "inegol kayıt sistemi",
            description = f'Lütfen etiketlediğin üyenin klanını seç.``{mes}``',
            colour = discord.Colour.random()
        )
        inegol_register_embed.set_footer(text=f'1 dakika içerisinde butonlar deaktif hale gelecektir\n{footer}')
        await interaction.response.send_message(embed=inegol_register_embed, view=view, ephemeral=True)

#topr
@bot.tree.command(name="topkayit", description="Kayıt verilerine göre sıralama yapar")
async def topr(interaction: discord.Interaction):
    istanbul_zaman2 = pytz.timezone("Europe/Istanbul")
    istanbul_tarih2 = datetime.datetime.now(istanbul_zaman2)
    tarih2 = istanbul_tarih2.strftime("%d/%m/%Y")
    mes = 'Kayıt verileri'
    hex = {"Status": "open"}
    bos = []
    bos2 = []
    user = str(interaction.user.id)
    reg_list = db.register_data.find(hex).sort("Total_reg", -1)
    if db.register_data.count_documents(hex) == 0:
        await interaction.response.send_message("Kayıt verisi sıfırlandığı için sıralama başarısız")
    elif db.register_data.count_documents(hex) == 1:
        for i in reg_list:
            kayit_sayi = str(i['Total_reg'])
            staff = str(i['Staff_id'])
            bos.append(kayit_sayi)
            bos2.append(staff)
        if user in bos2:  
            embed = discord.Embed(
                title = "Top 1",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n\n{interaction.user.mention}: {bos2.index(user)+1}. sıradasın',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        elif user not in bos2:
            embed = discord.Embed(
                title = "Top 1",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n\n{interaction.user.mention}: kayıt verilerin bulunamadığı için sıran tespit edilemedi',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
    elif db.register_data.count_documents(hex) == 2:
        for i in reg_list:
            kayit_sayi = str(i['Total_reg'])
            staff = str(i['Staff_id'])
            bos.append(kayit_sayi)
            bos2.append(staff)
        if user in bos2:  
            embed = discord.Embed(
                title = "top 2",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n\n{interaction.user.mention}: {bos2.index(user)+1}. sıradasın',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        elif user not in bos2:
            embed = discord.Embed(
                title = "top 2",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n\n{interaction.user.mention}: kayıt verilerin bulunamadığı için sıran tespit edilemedi',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Bir hata var")
    elif db.register_data.count_documents(hex) == 3:
        for i in reg_list:
            kayit_sayi = str(i['Total_reg'])
            staff = str(i['Staff_id'])
            bos.append(kayit_sayi)
            bos2.append(staff)
        if user in bos2:  
            embed = discord.Embed(
                title = "top 3",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n3. <@{bos2[2]}>: {bos[2]} \n\n{interaction.user.mention}: {bos2.index(user)+1}. sıradasın',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        elif user not in bos2:
            embed = discord.Embed(
                title = "top 3",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n3. <@{bos2[2]}>: {bos[2]} \n\n{interaction.user.mention}: kayıt verilerin bulunamadığı için sıran tespit edilemedi',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Bir hata var")
    elif db.register_data.count_documents(hex) == 4:
        for i in reg_list:
            kayit_sayi = str(i['Total_reg'])
            staff = str(i['Staff_id'])
            bos.append(kayit_sayi)
            bos2.append(staff)
        if user in bos2:  
            embed = discord.Embed(
                title = "top 4",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n3. <@{bos2[2]}>: {bos[2]} \n4. <@{bos2[3]}>: {bos[3]} \n\n{interaction.user.mention}: {bos2.index(user)+1}. sıradasın',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        elif user not in bos2:
            embed = discord.Embed(
                title = "top 4",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n3. <@{bos2[2]}>: {bos[2]} \n4. <@{bos2[3]}>: {bos[3]} \n\n{interaction.user.mention}: kayıt verilerin bulunamadığı için sıran tespit edilemedi',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Bir hata var")
    elif db.register_data.count_documents(hex) >= 5:
        for i in reg_list:
            kayit_sayi = str(i['Total_reg'])
            staff = str(i['Staff_id'])
            bos.append(kayit_sayi)
            bos2.append(staff)
        if user in bos2:  
            embed = discord.Embed(
                title = "top 5",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n3. <@{bos2[2]}>: {bos[2]} \n4. <@{bos2[3]}>: {bos[3]} \n5. <@{bos2[4]}>: {bos[4]}\n{interaction.user.mention}: {bos2.index(user)+1}. sıradasın',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        elif user not in bos2:
            embed = discord.Embed(
                title = "top 5",
                description = f'1. <@{bos2[0]}>: {bos[0]} \n2. <@{bos2[1]}>: {bos[1]} \n3. <@{bos2[2]}>: {bos[2]} \n4. <@{bos2[3]}>: {bos[3]} \n5. <@{bos2[4]}>: {bos[4]}\n{interaction.user.mention}: kayıt verilerin bulunamadığı için sıran tespit edilemedi',
                colour = discord.Colour.random()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Bir hata var")
    else:
        embed = discord.Embed(
            title = "Bir hata var",
            description = "Tespit edilemeyen bir hata oldu lütfen daha sonra tekrar deneyiniz.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
#rstat
@bot.tree.command(name="kayıtstat", description="Etiketlediğiniz üyenin ya da sizin kayıt verilerini gösterir.")
@app_commands.describe(member = "istatistiği görüntülenecek kullanıcıyı seçin")
async def rstat(interaction: discord.Interaction, member: discord.Member=None):
    istanbul_zaman2 = pytz.timezone("Europe/Istanbul")
    istanbul_tarih2 = datetime.datetime.now(istanbul_zaman2)
    tarih2 = istanbul_tarih2.strftime("%d/%m/%Y")
    role = interaction.guild.get_role(kayit_yetkili)
    if role not in interaction.user.roles:
        await interaction.response.send_message("Bu komutu kullanma iznin yok")
    elif role in interaction.user.roles:
        if member == None:
            member = interaction.user
        member2 = member.id
        hex = {"Staff_id": member2}
        staff_list = db.register_data.find(hex)
        if db.register_data.count_documents(hex) == 0:
            embed = discord.Embed(
                title = "Veri bulunamadı",
                description = f'{member} kullanıcısının kayıt verileri bulunamadı',
                colour = discord.Colour.red()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif db.register_data.count_documents(hex) == 1:
            for i in staff_list:
                embed = discord.Embed(
                    title = f'Kayıt verileri sıralandı',
                    description = f'**{member} yetkilisinin kayıt verileri**\n\nToplam kayıt: ' + str(i['Total_reg']) + '\nbirinciklan kayıt: ' + str(i['birinciklan_reg']) + '\nikinciklan kayıt: ' + str(i['ikinciklan_reg']) + '\nucuncuklan kayıt: ' + str(i['ucuncuklan_reg'])  + '\ndorduncuklan kayıt: ' + str(i['dorduncuklan_reg']) + '\nbesinciklan kayıt: ' + str(i['besinciklan_reg']),
                    colour = discord.Colour.random()
                )
                embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
                await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Bir hata var", ephemeral=True)

#black list
@bot.tree.context_menu(name="Blacklist")
async def blacklist(interaction: discord.Interaction, member: discord.Member):
    istanbul_zaman2 = pytz.timezone("Europe/Istanbul")
    istanbul_tarih2 = datetime.datetime.now(istanbul_zaman2)
    tarih2 = istanbul_tarih2.strftime("%d/%m/%Y")
    role = interaction.guild.get_role(yonetici_id)
    log_ch = interaction.guild.get_channel(bl_log_kanal_id)
    member2 = member.id
    hex = {"Member_id": member2}
    if role not in interaction.user.roles:
        embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Bu komutu kullanmak için yeterli izinlere sahip değilsin",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
        await interaction.response.send_message(embed=embed)
        await log_ch.send(embed=embed)
    elif db.black_list.count_documents(hex) > 0:
        button1 = Button(label="Onayla", style=discord.ButtonStyle.green, custom_id="onay", emoji="✔️")
        button2 = Button(label="İptal et", style=discord.ButtonStyle.red, custom_id="iptal", emoji="❌")
        async def button1_callback(interaction):
            db.black_list.delete_one(hex)
            embed = discord.Embed(
                title = "İşlem başarılı",
                description = f'{member.mention} **üyesi artık kara listede değil**\n\n● Yetkili id: {interaction.user.id}\n● Üye id: {member.id}\n● Sebep: oyle gerekti\n● Tarih: {tarih2}',
                colour = discord.Colour.green()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.edit_message(embed=embed, view=None)
            await log_ch.send(embed=embed)
        
        async def button2_callback(interaction):
            embed = discord.Embed(
                title = "İşlem iptal edildi",
                description = "Black list işlemi iptal edildi",
                colour = discord.Colour.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
        
        button1.callback = button1_callback
        button2.callback = button2_callback

        view = View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        inegol_bl_embed = discord.Embed(
            title = "inegol black list system",
            description = f'{member.mention} üyesini kara listeden çıkarmak istediğine emin misin?\n\nİşlemi onaylıyorsan yeşil butona bas\nİşlemi iptal etmek istiyorsan kırmızı butona bas',
            colour = discord.Colour.random()
        )
        inegol_bl_embed.set_footer(text=f'1 dakika içerisinde butonlar deaktif hale gelecektir\n{footer}')
        await interaction.response.send_message(embed=inegol_bl_embed, view=view, ephemeral=True)
            
    elif db.black_list.count_documents(hex) == 0:
        button1 = Button(label="Onayla", style=discord.ButtonStyle.green, custom_id="onay", emoji="✔️")
        button2 = Button(label="İptal et", style=discord.ButtonStyle.red, custom_id="iptal", emoji="❌")
        async def button1_callback(interaction):
            db.black_list.insert_one(
                {
                    "Staff_id": interaction.user.id,
                    "Member_id": member2,
                    "Date": tarih2,
                }
            )
            embed = discord.Embed(
                title = "İşlem başarılı",
                description = f'{member.mention} **üyesi artık kara listede**\n\n● Yetkili id: {interaction.user.id}\n● Üye id: {member.id}\n● Sebep: oyle gerekti \n● Tarih: {tarih2}',
                colour = discord.Colour.red()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.edit_message(embed=embed, view=None)
            await log_ch.send(embed=embed)
        
        async def button2_callback(interaction):
            embed = discord.Embed(
                title = "İşlem iptal edildi",
                description = "Black list işlemi iptal edildi",
                colour = discord.Colour.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

        button1.callback = button1_callback
        button2.callback = button2_callback

        view = View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        inegol_bl_embed = discord.Embed(
            title = "İnegöl black list system",
            description = f'{member.mention} üyesini kara listeye almak istediğine emin misin?\n\nİşlemi onaylıyorsan yeşil butona bas\nİşlemi iptal etmek istiyorsan kırmızı butona bas',
            colour = discord.Colour.random()
        )
        inegol_bl_embed.set_footer(text=f'1 dakika içerisinde butonlar deaktif hale gelecektir\n{footer}')
        await interaction.response.send_message(embed=inegol_bl_embed, view=view, ephemeral=True)

    else:
        print("bl komutunda bir şeyler ters gitti")

#kayit sifirla
@bot.tree.command(name="kayıtsıfırla", description="Etiketlediğiniz yetkilinin kayıt ettiği kişi sayısını sıfırlar")
@app_commands.describe(member = "işlem yapılacak yetkiliyi etiketleyiniz.")
async def kayitres(interaction: discord.Interaction, member: discord.Member):
    istanbul_zaman2 = pytz.timezone("Europe/Istanbul")
    istanbul_tarih2 = datetime.datetime.now(istanbul_zaman2)
    tarih2 = istanbul_tarih2.strftime("%d/%m/%Y")
    role = interaction.guild.get_role(yonetici_id)
    log_ch = interaction.guild.get_channel(data_log_kanal_id)
    member2 = member.id
    hex = {"Staff_id": member2}
    if role not in interaction.user.roles:
        embed = discord.Embed(
            title = "Erişim Reddedildi",
            description = f'{interaction.user.mention} Bu komutu kullanma iznin yok.',
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
        await interaction.response.send_message(embed=embed)
    elif db.register_data.count_documents(hex) == 1:
        button1 = Button(label="Onayla", style=discord.ButtonStyle.green, custom_id="onay", emoji="✔️")
        button2 = Button(label="İptal et", style=discord.ButtonStyle.red, custom_id="iptal", emoji="❌")
        async def button1_callback(interaction):
            db.register_data.delete_one(hex)
            embed = discord.Embed(
                title = "İşlem başarılı",
                description = f'{interaction.user.mention} tarafından {member.mention} üyesinin **kayıt sayısı** sıfırlandı',
                colour = discord.Colour.green()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.edit_message(embed=embed, view=None)
            await log_ch.send(embed=embed)

        async def button2_callback(interaction):
            embed = discord.Embed(
                title = "İşlem iptal edildi",
                description = "Kayıt sıfırlama işlemi iptal edildi",
                colour = discord.Colour.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

        button1.callback = button1_callback
        button2.callback = button2_callback

        view = View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        inegol_kres_embed = discord.Embed(
            title = "İnegöl system",
            description = f'{member.mention} üyesinin kayıt sayısını sıfırlamak istediğine emin misin?\n\nİşlemi onaylıyorsan yeşil butona bas\nİşlemi iptal etmek istiyorsan kırmızı butona bas',
            colour = discord.Colour.random()
        )
        inegol_kres_embed.set_footer(text=f'1 dakika içerisinde butonlar deaktif hale gelecektir\n{footer}')
        await interaction.response.send_message(embed=inegol_kres_embed, view=view, ephemeral=True)

    elif db.register_data.count_documents(hex) == 0:
        embed = discord.Embed(
            title = "İşlem başarılı",
            description = f'{member.mention} üyesinin kayıt sayısı zaten daha önceden sıfırlandı',
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
        await interaction.response.send_message(embed=embed)
    elif db.register_data.count_documents(hex) > 1:
        button1 = Button(label="Onayla", style=discord.ButtonStyle.green, custom_id="onay", emoji="✔️")
        button2 = Button(label="İptal et", style=discord.ButtonStyle.red, custom_id="iptal", emoji="❌")
        async def button1_callback(interaction):
            db.register_data.delete_many(hex)
            embed = discord.Embed(
                title = "İşlem başarılı",
                description = f'{interaction.user.mention} tarafından {member.mention} üyesinin **kayıt sayısı** sıfırlandı',
                colour = discord.Colour.green()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.edit_message(embed=embed, view=None)
            await log_ch.send(embed=embed)

        async def button2_callback(interaction):
            embed = discord.Embed(
                title = "İşlem iptal edildi",
                description = "Kayıt sıfırlama işlemi iptal edildi",
                colour = discord.Colour.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

        button1.callback = button1_callback
        button2.callback = button2_callback

        view = View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        inegol_kres_embed = discord.Embed(
            title = "İnegöl system",
            description = f'{member.mention} üyesinin kayıt sayısını sıfırlamak istediğine emin misin?\n\nİşlemi onaylıyorsan yeşil butona bas\nİşlemi iptal etmek istiyorsan kırmızı butona bas',
            colour = discord.Colour.random()
        )
        inegol_kres_embed.set_footer(text=f'1 dakika içerisinde butonlar deaktif hale gelecektir\n{footer}')
        await interaction.response.send_message(embed=inegol_kres_embed, view=view, ephemeral=True)
    else:
        await interaction.response.send_message("Bir hata var", ephemeral=True)

#isim geçmişi sıfırla
@bot.tree.command(name="isimres", description="Etiketlediğiniz kişinin isim geçmişini sıfırlar")
@app_commands.describe(member = "işlem yapılacak yetkiliyi etiketleyiniz.")
async def isimres(interaction: discord.Interaction, member: discord.Member):
    istanbul_zaman2 = pytz.timezone("Europe/Istanbul")
    istanbul_tarih2 = datetime.datetime.now(istanbul_zaman2)
    tarih2 = istanbul_tarih2.strftime("%d/%m/%Y")
    role = interaction.guild.get_role(yonetici_id)
    log_ch = interaction.guild.get_channel(data_log_kanal_id)
    member2 = member.id
    hex = {"Member_id": member2}
    if role not in interaction.user.roles:
        embed = discord.Embed(
            title = "Erişim Reddedildi",
            description = f'{interaction.user.mention} Bu komutu kullanma iznin yok.',
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
        await interaction.response.send_message(embed=embed)
    elif db.user_info.count_documents(hex) == 1:
        button1 = Button(label="Onayla", style=discord.ButtonStyle.green, custom_id="onay", emoji="✔️")
        button2 = Button(label="İptal et", style=discord.ButtonStyle.red, custom_id="iptal", emoji="❌")
        async def button1_callback(interaction):
            db.user_info.delete_one(hex)
            embed = discord.Embed(
                title = "İşlem başarılı",
                description = f'{interaction.user.mention} tarafından {member.mention} üyesinin **isim geçmişi** sıfırlandı',
                colour = discord.Colour.green()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.edit_message(embed=embed, view=None)
            await log_ch.send(embed=embed)

        async def button2_callback(interaction):
            embed = discord.Embed(
                title = "İşlem iptal edildi",
                description = "İsim sıfırlama işlemi iptal edildi",
                colour = discord.Colour.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

        button1.callback = button1_callback
        button2.callback = button2_callback

        view = View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        inegol_kres_embed = discord.Embed(
            title = "İnegöl system",
            description = f'{member.mention} üyesinin isim geçmişini sıfırlamak istediğine emin misin?\n\nİşlemi onaylıyorsan yeşil butona bas\nİşlemi iptal etmek istiyorsan kırmızı butona bas',
            colour = discord.Colour.random()
        )
        inegol_kres_embed.set_footer(text=f'1 dakika içerisinde butonlar deaktif hale gelecektir\n{footer}')
        await interaction.response.send_message(embed=inegol_kres_embed, view=view, ephemeral=True)

    elif db.user_info.count_documents(hex) == 0:
        db.user_info.delete_one(hex)
        embed = discord.Embed(
            title = "İşlem başarılı",
            description = f'{member.mention} üyesinin kayıtlı isim geçmişi bulunamadı',
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
        await interaction.response.send_message(embed=embed)
    elif db.user_info.count_documents(hex) > 1:
        button1 = Button(label="Onayla", style=discord.ButtonStyle.green, custom_id="onay", emoji="✔️")
        button2 = Button(label="İptal et", style=discord.ButtonStyle.red, custom_id="iptal", emoji="❌")
        async def button1_callback(interaction):
            db.user_info.delete_many(hex)
            embed = discord.Embed(
                title = "İşlem başarılı",
                description = f'{interaction.user.mention} tarafından {member.mention} üyesinin **isim geçmişi** sıfırlandı',
                colour = discord.Colour.green()
            )
            embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}  \n{tarih2}')
            await interaction.response.edit_message(embed=embed, view=None)
            await log_ch.send(embed=embed)

        async def button2_callback(interaction):
            embed = discord.Embed(
                title = "İşlem iptal edildi",
                description = "İsim sıfırlama işlemi iptal edildi",
                colour = discord.Colour.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

        button1.callback = button1_callback
        button2.callback = button2_callback

        view = View(timeout=60)
        view.add_item(button1)
        view.add_item(button2)
        inegol_kres_embed = discord.Embed(
            title = "İnegöl system",
            description = f'{member.mention} üyesinin isim geçmişini sıfırlamak istediğine emin misin?\n\nİşlemi onaylıyorsan yeşil butona bas\nİşlemi iptal etmek istiyorsan kırmızı butona bas',
            colour = discord.Colour.random()
        )
        inegol_kres_embed.set_footer(text=f'1 dakika içerisinde butonlar deaktif hale gelecektir\n{footer}')
        await interaction.response.send_message(embed=inegol_kres_embed, view=view, ephemeral=True)

@bot.tree.command(name="jail", description="Etiketlenilen kişiyi jaile atar.")
async def tutsak_et(interaction: discord.Interaction, member: discord.Member, dakika: int = 0,  sebep: str = "Sebep belirtilmemiş"):
    tutsak_role = interaction.guild.get_role(tutsak_rol_id)
    jail_log_ch = interaction.guild.get_channel(jail_log)
    jail_yetki_role = interaction.guild.get_role(jail_yetki)
    saniyes = dakika * 60
    if jail_yetki_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Bu komutu kullanmak için yeterli izinlere sahip değilsin",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        await jail_log_ch.send(embed=embed)
    elif tutsak_rol_id in member.roles:
                embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Üye zaten jailde bulunuyor.",
            colour = discord.Colour.red()
        )
    
    elif jail_yetki_role in member.roles:
        embed = discord.Embed(
            title="jail işlemi başarısız",
            description=f"yetkilileri jailleyemezsin",
            colour= discord.Colour.red()
            )
        embed.set_author(icon_url=bot.user.display_avatar, name=f"{bot.user.display_name}")
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(icon_url= interaction.user.display_avatar, text=f"{interaction.user.display_name} yetkili jailleyemezsin.")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message(f"jail işlemi başarısız.", ephemeral=True)
        
    

    else:
        await member.add_roles(tutsak_role)
        embed = discord.Embed(
                    title="jail işlemi Başarılı",
                    description=f"**Yetkili ID: **``{interaction.user.id}``\n**Yetkili Adı: **``{interaction.user.display_name}``\n**Cezalı ID: **``{member.id}``\n**Cezalı Adı: **``{member.display_name}``\n**Ceza Sebebi: **``{sebep}``\n**Ceza Süresi: ** ``{dakika} dakika``",
                    colour= discord.Colour.red()
                )
        embed.set_author(icon_url=bot.user.display_avatar, name=f"{bot.user.display_name}")
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(icon_url= interaction.user.display_avatar, text=f"{interaction.user.display_name} tarafından jaile atıldı.")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message(f"jail işlemi başarılı", ephemeral=True)
        await jail_log_ch.send(embed=embed)
        await asyncio.sleep(saniyes)
        await member.remove_roles(tutsak_role)
        if tutsak_role in member.roles:
            await member.remove_roles(tutsak_rol_id)
            embed2 = discord.Embed(
                    title="jail süresi bitti",
                    description=f"**\n**Cezalı ID: **``{member.id}``\n**Cezalı Adı: **``{member.display_name}``\n**Ceza Sebebi: **``{sebep}``\n**Ceza Süren Bitti",
                    colour= discord.Colour.red()
                )
            embed2.set_author(icon_url=bot.user.display_avatar, name=f"{bot.user.display_name}")
            embed2.set_thumbnail(url=member.display_avatar)
            embed2.set_footer(icon_url= interaction.user.display_avatar, text=f"{interaction.user.display_name} tarafından atılmıştı.")
            await jail_log_ch.send(embed=embed2)
        else:
            embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Üye jailden daha önce çıkarılmış.",
            colour = discord.Colour.red()
        )
            


@bot.tree.context_menu(name="jailden Çıkar")
async def tutsak_cikar(interaction: discord.Interaction, member: discord.Member):
    tutsak_role = interaction.guild.get_role(tutsak_rol_id)
    jail_log_ch = interaction.guild.get_channel(jail_log)
    jail_yetki_role = interaction.guild.get_role(jail_yetki)
    if jail_yetki_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Bu komutu kullanmak için yeterli izinlere sahip değilsin",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        await jail_log_ch.send(embed=embed),
    elif tutsak_role not in member.roles:
        embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Üye jailde gözükmüyor.",
            colour = discord.Colour.red()
        )
    elif tutsak_role in member.roles:
        await member.remove_roles(tutsak_role)
        embed2 = discord.Embed(
                    title="jailden çıkarıldın",
                    description=f"**\n**Cezalı ID: **``{member.id}``\n**Cezalı Adı: **``{member.display_name}``\n**Affedildin.",
                    colour= discord.Colour.red()
                )
        embed2.set_author(icon_url=bot.user.display_avatar, name=f"{bot.user.display_name}")
        embed2.set_thumbnail(url=member.display_avatar)
        embed2.set_footer(icon_url= interaction.user.display_avatar, text=f"{interaction.user.display_name} seni affetti.")
        await interaction.response.send_message(f'{member.mention} üyesi jailden çıkarıldı.', ephemeral=True)
        await jail_log_ch.send(embed=embed2)

@bot.tree.context_menu(name="Kalıcı jail")     
async def kalici_jail(interaction: discord.Interaction, member: discord.Member):
    tutsak_role = interaction.guild.get_role(tutsak_rol_id)
    jail_log_ch = interaction.guild.get_channel(jail_log)
    jail_yetki_role = interaction.guild.get_role(yonetici_id)
    if jail_yetki_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Bu komutu kullanmak için yeterli izinlere sahip değilsin",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        await jail_log_ch.send(embed=embed)
    elif tutsak_rol_id in member.roles:
                embed = discord.Embed(
            title = "Erişim reddedildi",
            description = "Üye zaten jailde bulunuyor.",
            colour = discord.Colour.red()
        )
    
    elif jail_yetki_role in member.roles:
        embed = discord.Embed(
            title="jail işlemi başarısız",
            description=f"yetkilileri jailleyemezsin",
            colour= discord.Colour.red()
            )
        embed.set_author(icon_url=bot.user.display_avatar, name=f"{bot.user.display_name}")
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(icon_url= interaction.user.display_avatar, text=f"{interaction.user.display_name} yetkili jaillemeye calisan mal.")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message(f"jail işlemi başarısız.", ephemeral=True)
    else:
        await member.add_roles(tutsak_role)
        embed = discord.Embed(
                    title="jail işlemi Başarılı",
                    description=f"**Yetkili ID: **``{interaction.user.id}``\n**Yetkili Adı: **``{interaction.user.display_name}``\n**Cezalı ID: **``{member.id}``\n**Cezalı Adı: **``{member.display_name}``\n**Ceza Sebebi: oc olmak``\n**Ceza Süresi: ** ``SINIRSIZ``",
                    colour= discord.Colour.red()
                )
        embed.set_author(icon_url=bot.user.display_avatar, name=f"{bot.user.display_name}")
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(icon_url= interaction.user.display_avatar, text=f"{interaction.user.display_name} tarafından jaile atıldı.")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message(f"jail işlemi başarılı", ephemeral=True)
        await jail_log_ch.send(embed=embed)
                
@bot.tree.command(name="generalyetkial", description="Etiketlenen yetkilinin yetkisini alır.")
async def general_yetki_al(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    general_role = interaction.guild.get_role(birinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkilinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.remove_roles(mod_role)
        await member.remove_roles(genel_yetki_role)
        await member.remove_roles(general_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcının yetkisi başarıyla alındı.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="papazyetkial", description="Etiketlenen yetkilinin yetkisini alır.")
async def papaz_yetki_al(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    papaz_role = interaction.guild.get_role(ikinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkilinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.remove_roles(mod_role)
        await member.remove_roles(genel_yetki_role)
        await member.remove_roles(papaz_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcının yetkisi başarıyla alındı.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="zebaniyetkial", description="Etiketlenen yetkilinin yetkisini alır.")
async def zebani_yetki_al(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    zebani_role = interaction.guild.get_role(dorduncu_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkilinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.remove_roles(mod_role)
        await member.remove_roles(genel_yetki_role)
        await member.remove_roles(zebani_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcının yetkisi başarıyla alındı.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="basmelekyetkial", description="Etiketlenen yetkilinin yetkisini alır.")
async def basmelek_yetki_al(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    basmelek_role = interaction.guild.get_role(besinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkilinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.remove_roles(mod_role)
        await member.remove_roles(genel_yetki_role)
        await member.remove_roles(basmelek_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcının yetkisi başarıyla alındı.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="evliyayetkial", description="Etiketlenen yetkilinin yetkisini alır.")
async def evliya_yetki_al(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    evliya_role = interaction.guild.get_role(altinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkilinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.remove_roles(mod_role)
        await member.remove_roles(genel_yetki_role)
        await member.remove_roles(evliya_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcının yetkisi başarıyla alındı.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ermisyetkial", description="Etiketlenen yetkilinin yetkisini alır.")
async def ermis_yetki_al(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    ermis_role = interaction.guild.get_role(yedinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkilinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.remove_roles(mod_role)
        await member.remove_roles(genel_yetki_role)
        await member.remove_roles(ermis_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcının yetkisi başarıyla alındı.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="generalyetkiver", description="Etiketlenen kişiyi yetkili yapar..")
async def general_yetki_ver(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    general_role = interaction.guild.get_role(birinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.add_roles(mod_role)
        await member.add_roles(genel_yetki_role)
        await member.add_roles(general_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcı artık yetkili.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="papazyetkiver", description="Etiketlenen kişiyi yetkili yapar..")
async def papaz_yetki_ver(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    papaz_role = interaction.guild.get_role(ikinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.add_roles(mod_role)
        await member.add_roles(genel_yetki_role)
        await member.add_roles(papaz_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcı artık yetkili.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="zebaniyetkiver", description="Etiketlenen kişiyi yetkili yapar..")
async def zebani_yetki_ver(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    zebani_role = interaction.guild.get_role(dorduncu_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.add_roles(mod_role)
        await member.add_roles(genel_yetki_role)
        await member.add_roles(zebani_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcı artık yetkili.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="basmelekyetkiver", description="Etiketlenen kişiyi yetkili yapar..")
async def basmelek_yetki_ver(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    basmelek_role = interaction.guild.get_role(besinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.add_roles(mod_role)
        await member.add_roles(genel_yetki_role)
        await member.add_roles(basmelek_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcı artık yetkili.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="evliyayetkiver", description="Etiketlenen kişiyi yetkili yapar..")
async def evliya_yetki_ver(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    evliya_role = interaction.guild.get_role(altinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkinin üzerinde kullanamazsın",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.add_roles(mod_role)
        await member.add_roles(genel_yetki_role)
        await member.add_roles(evliya_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcı artık yetkili.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ermisyetkiver", description="Etiketlenen kişiyi yetkili yapar..")
async def evliya_yetki_ver(interaction: discord.Interaction, member: discord.Member):
    ustad_role = interaction.guild.get_role(admin_rol_id)
    mod_role = interaction.guild.get_role(mod_rol_id)
    genel_yetki_role = interaction.guild.get_role(genel_yetki_rol_id)
    ermis_role = interaction.guild.get_role(yedinci_klan_mod_rol_id)
    if ustad_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif ustad_role in member.roles:
        embed = discord.Embed(
            title = "hata",
            description = "yetkiliye yetki veremezsin",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await member.add_roles(mod_role)
        await member.add_roles(genel_yetki_role)
        await member.add_roles(ermis_role)
        embed = discord.Embed(
            title = "basarili.",
            description = "kullanıcı artık yetkili.",
            colour = discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.context_menu(name="Kayıt Sil")     
async def kayitsil(interaction: discord.Interaction, member: discord.Member):
    kayitsiz_role = interaction.guild.get_role(kayitsiz_rol_id)
    log_ch = interaction.guild.get_channel(supheli_kanal_id)
    yetkili_role = interaction.guild.get_role(genel_yetki_rol_id)
    birinciklan_role = interaction.guild.get_role(birinci_klan_rol_id)
    ikinciklan_role = interaction.guild.get_role(ikinci_klan_rol_id)
    besinciklan_role = interaction.guild.get_role(besinci_klan_rol_id)
    ucuncuklan_role = interaction.guild.get_role(ucuncu_klan_rol_id)
    dorduncuklan_role = interaction.guild.get_role(dorduncu_klan_rol_id)
    altinciklan_role = interaction.guild.get_role(altinci_klan_rol_id)

    if yetkili_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "sen yetkili misin de bu komudu kullanıon.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif yetkili_role in member.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkilinin kaydını alamazsın.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    elif birinciklan_role in member.roles:
        await member.remove_roles(birinciklan_role)
        await member.add_roles(kayitsiz_role)
        embed = discord.Embed(
            title = "basarili",
            description = "kullanıcının kaydı başarıla silindi.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        log_embed = discord.Embed(
                title = "Bir kayıt silme işlemi yapıldı",
                description = f'● Yetkili: ``{interaction.user}``\n● Yetkili id: ``{interaction.user.id}``\n● Kaydı silinen üye: ``{member}``\n● Kaydı silinen üye id: ``{member.id}``',
                colour = discord.Colour.blue()
            )
        await log_ch.send(embed=log_embed)
    elif ikinciklan_role in member.roles: 
        await member.remove_roles(ikinciklan_role)
        await member.add_roles(kayitsiz_role)
        embed = discord.Embed(
            title = "basarili",
            description = "kullanıcının kaydı başarıla silindi.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        log_embed = discord.Embed(
                title = "Bir kayıt silme işlemi yapıldı",
                description = f'● Yetkili: ``{interaction.user}``\n● Yetkili id: ``{interaction.user.id}``\n● Kaydı silinen üye: ``{member}``\n● Kaydı silinen üye id: ``{member.id}``',
                colour = discord.Colour.blue()
            )
        await log_ch.send(embed=log_embed)
    elif besinciklan_role in member.roles:
        await member.remove_roles(besinciklan_role)
        await member.add_roles(kayitsiz_role)
        embed = discord.Embed(
            title = "basarili",
            description = "kullanıcının kaydı başarıla silindi.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        log_embed = discord.Embed(
                title = "Bir kayıt silme işlemi yapıldı",
                description = f'● Yetkili: ``{interaction.user}``\n● Yetkili id: ``{interaction.user.id}``\n● Kaydı silinen üye: ``{member}``\n● Kaydı silinen üye id: ``{member.id}``',
                colour = discord.Colour.blue()
            )
        await log_ch.send(embed=log_embed)
    elif dorduncuklan_role in member.roles:
        await member.remove_roles(dorduncuklan_role)
        await member.add_roles(kayitsiz_role)
        embed = discord.Embed(
            title = "basarili",
            description = "kullanıcının kaydı başarıla silindi.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        log_embed = discord.Embed(
                title = "Bir kayıt silme işlemi yapıldı",
                description = f'● Yetkili: ``{interaction.user}``\n● Yetkili id: ``{interaction.user.id}``\n● Kaydı silinen üye: ``{member}``\n● Kaydı silinen üye id: ``{member.id}``',
                colour = discord.Colour.blue()
            )
        await log_ch.send(embed=log_embed)
    elif ucuncuklan_role in member.roles:
        await member.remove_roles(ucuncuklan_role)
        await member.add_roles(kayitsiz_role)
        embed = discord.Embed(
            title = "basarili",
            description = "kullanıcının kaydı başarıla silindi.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        log_embed = discord.Embed(
                title = "Bir kayıt silme işlemi yapıldı",
                description = f'● Yetkili: ``{interaction.user}``\n● Yetkili id: ``{interaction.user.id}``\n● Kaydı silinen üye: ``{member}``\n● Kaydı silinen üye id: ``{member.id}``',
                colour = discord.Colour.blue()
            )
        await log_ch.send(embed=log_embed)
    elif altinciklan_role in member.roles:    
        await member.remove_roles(altinciklan_role)
        await member.add_roles(kayitsiz_role)
        embed = discord.Embed(
            title = "basarili",
            description = "kullanıcının kaydı başarıla silindi.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
        log_embed = discord.Embed(
                title = "Bir kayıt silme işlemi yapıldı",
                description = f'● Yetkili: ``{interaction.user}``\n● Yetkili id: ``{interaction.user.id}``\n● Kaydı silinen üye: ``{member}``\n● Kaydı silinen üye id: ``{member.id}``',
                colour = discord.Colour.blue()
            )
        await log_ch.send(embed=log_embed)
        
@bot.tree.command(name="botkonustur", description="botu konusturur")
async def botkonustur(interaction: discord.Interaction,botkonustur: str = "kaanın anasını sikeiym"):
    yetkili_role = interaction.guild.get_role(genel_yetki_rol_id)
    if yetkili_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkin yok botu nasil konusturacan.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"{botkonustur}")
        msg = await interaction.original_response()

@bot.tree.command(name="oylama", description="oylama yapar")
async def oylama(interaction: discord.Interaction,oylama: str = "neyi oyluyoz"):
    yetkili_role = interaction.guild.get_role(genel_yetki_rol_id)
    if yetkili_role not in interaction.user.roles:
        embed = discord.Embed(
            title = "hata.",
            description = "yetkın yok ne oylaması.",
            colour = discord.Colour.red()
        )
        embed.set_footer(text=f'Komutu kullanan kişi: {interaction.user}')
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"Oylama: {oylama}")
        msg = await interaction.original_response()
        await msg.add_reaction('👍')  # Evet
        await msg.add_reaction('👎')  # Hayır
        
@bot.event
async def on_member_join(member):
    age = member.created_at.strftime("%d/%m/%Y %H.%M.%S")
    bugün = datetime.datetime.now()
    yil = int(member.created_at.strftime("%Y"))
    ay = int(member.created_at.strftime("%m"))
    gun = int(member.created_at.strftime("%d"))
    acilis = datetime.datetime(yil, ay, gun)

    result = db.collection.find_one({"_id": member.id})
    if result:
        result = db.collection.find_one({"_id": member.id})
    if result and result.get("jailed"):
        role = discord.utils.get(member.guild.roles, name="tutsakrolünüyaz")
        await member.add_roles(role)
        await member.send("cezalıyken sunucumuzdan çıkarsan tekrardan cezalı olursun.")

    ay2 = datetime.datetime.strftime(acilis, '%B')
    fark = bugün - acilis
    bekleme_suresi = supheli_hesap_suresi - fark.days
    if fark.days < supheli_hesap_suresi:
        role = member.guild.get_role(supheli_rol_id)
        channel = member.guild.get_channel(supheli_kanal_id)
        nick = (f'Şüpheli hesap')
        embed = discord.Embed(
            title = "Şüpheli Hesap",
            description = f'● Hesap adı: ``{member}``\n● Hesap id: ``{member.id}``\n● kuruluş tarihi: ``{gun} {ay2} {yil}``\n● Geçen süre: ``{fark.days} gün``\n● Kalan süre: ``{bekleme_suresi} gün``',
            colour = discord.Colour.red()
        )
        await member.add_roles(role)
        await member.edit(nick=nick)
        await channel.send(embed=embed)
        await member.send(f'Sunucuya kayıt olmak için hesabının en az {supheli_hesap_suresi} gün önce açılmış olması lazım yani {bekleme_suresi} gün daha beklemelisin. ')
    else:
        role = member.guild.get_role(kayitsiz_rol_id)
        channel = member.guild.get_channel(kayit_bilgilendirme_ch)
        nick = (f'isim')
        embed = discord.Embed(
            title = "Aramıza yeni bir üye katıldı",
            description = f'{member.mention} hoşgeldin 🔱\n\nhesabın ``{gun} {ay2} {yil}`` tarihinde oluşturulmuş\n\n <@&{kayit_yetkili}> rolüne sahip yetkililerimiz seni birazdan kaydedecekler.',
            colour = discord.Colour.green()
        )
        await member.add_roles(role)
        await channel.send(f'<@&{kayit_yetkili}> {member.mention}',embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(bb_kanal_id)
    bb_embed = discord.Embed(
        title = "Bir üye sunucumuzdan ayrıldı",
        description = f'{member} adlı üye sunucumuzdan ayrıldı.',
        colour = discord.Colour.red()
    )
    await channel.send(embed=bb_embed)
     
    existing_member = db.collection.find_one({"_id": member.id})
    if existing_member:
        # Eğer üye zaten varsa, tutsaklık durumunu güncelle
        jailed = False
        for role in member.roles:
            if role.name == "TUTSAK":
                jailed = True
                break
        db.collection.update_one({"_id": member.id}, {"$set": {"jailed": jailed}})
    else:
        # Eğer üye yoksa, MongoDB'ye ekle
        jailed = False
        for role in member.roles:
            if role.name == "TUTSAK":
                jailed = True
                break
        db.collection.insert_one({"_id": member.id, "jailed": jailed})

@bot.event
async def on_presence_update(before, after):
    role = before.guild.get_role(kayitsiz_rol_id)
    channel = bot.get_channel(kayit_bilgilendirme_ch)
    if role in before.roles:
        if before.status is discord.Status.offline and after.status is not discord.Status.offline:
            await channel.send(f'{before.mention} tekrardan aktif oldun ama hala kayıta gelmedin seni bekliyorum')
    else:
        pass
    
@bot.event 
async def on_ready():
    print(bot.user.name)
    print("Bot Açılma Saati: ", tarih)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ananı"))
    try:
        synced = await bot.tree.sync()
        print(f'Entegre edilen slash Komut sayısı: {len(synced)}')
    except Exception as e:
        print(e)

bot.run(token)
