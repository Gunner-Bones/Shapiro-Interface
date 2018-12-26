import discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, operator, copy, collections
from discord.ext import commands


Client = discord.Client()
bot_prefix= "??"
client = commands.Bot(command_prefix=bot_prefix)

s = None
try: s = open("pass.txt","r")
except: sys.exit("[Error] pass.txt needed for Secret")
sl = []
for l in s: sl.append(l.replace("\n",""))
SECRET = sl[0]

# https://discordapp.com/oauth2/authorize?client_id=509126832495525898&scope=bot

CHAR_SUCCESS = "✅"
CHAR_FAILED = "❌"
CHAR_UP = "🔼"
CHAR_DOWN = "🔽"
CHAR_NEW = "🆕"
CHAR_NEUTRAL = "⏹"

SIMULATED = False

def memberadmin(member):
    for r in member.roles:
       if r.permissions.administrator: return True
    return False

def getrole(s,rn):
    try:
        rid = int(rn)
        return discord.utils.find(lambda r: str(rid) in str(r.id), s.roles)
    except: return discord.utils.find(lambda r: rn.lower() in r.name.lower(), s.roles)

def getmember(s,mn):
    if str(mn).startswith("<@"):
        mid = mn.replace("<@",""); mid = mid.replace(">","")
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
    try:
        mid = int(mn)
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
    except: return discord.utils.find(lambda m: mn.lower() in m.name.lower(), s.members)

def getchannel(s,cn):
    if str(cn).startswith("<#"):
        cid = cn.replace("<#",""); cid = cid.replace(">","")
        return discord.utils.find(lambda m: str(cid) in str(m.id), s.channels)
    try:
        cid = int(cn)
        return discord.utils.find(lambda m: str(cid) in str(m.id), s.channels)
    except: return discord.utils.find(lambda m: cn.lower() in m.name.lower(), s.channels)

def getguild(sid):
    for guild in client.guilds:
        if str(guild.id) == str(sid): return guild
    return None


def datasettings(file,method,line="",newvalue="",newkey=""):
    """
    :param file: (str).txt
    :param method: (str) get,change,remove,add
    :param line: (str)
    :param newvalue: (str)
    :param newkey: (str)
    """
    s = None
    try: s = open(file,"r")
    except: return None
    sl = []
    for l in s: sl.append(l.replace("\n",""))
    for nl in sl:
        if str(nl).startswith(line):
            if method == "get": s.close(); return str(nl).replace(line + "=","")
            elif method == "change": sl[sl.index(nl)] = line + "=" + newvalue; break
            elif method == "remove": sl[sl.index(nl)] = None; break
    if method == "add": sl.append(newkey + "=" + newvalue)
    if method == "get": return None
    s.close()
    s = open(file,"w")
    s.truncate()
    slt = ""
    for nl in sl:
        if nl is not None:
            slt += nl + "\n"
    s.write(slt); s.close(); return None

def alldatakeys(file) -> list:
    s = None
    try: s = open(file,"r")
    except: return []
    sl = []
    for l in s: sl.append(l.replace("\n", ""))
    for nl in sl:
        nla = str(nl).split("=")
        sl[sl.index(nl)] = nla[0]
    s.close()
    for nl in sl:
        if nl == "": sl.remove(nl)
    return sl

def getlatest(file):
    s = None
    try: s = open(file, "r")
    except: return None
    sl = []
    for l in s: sl.append(l.replace("\n", ""))
    for nl in sl:
        nla = str(nl).split("=")
        sl[sl.index(nl)] = nla[0]
    s.close()
    if len(sl) == 0: return None
    return sl[len(sl) - 1]

def getsecondlatest(file):
    s = None
    try:
        s = open(file, "r")
    except:
        return None
    sl = []
    for l in s: sl.append(l.replace("\n", ""))
    for nl in sl:
        nla = str(nl).split("=")
        sl[sl.index(nl)] = nla[0]
    s.close()
    if len(sl) == 0: return None
    return sl[len(sl) - 2]

def strtodatetime(s):
    # Format: 2018-12-25, 14:30
    st = str(s).split("-")
    stm = str(st[1]).split(":")
    return [datetime.date(year=int(st[0]),month=int(st[1]),day=int(st[2])),datetime.time(hour=int(stm[0]),
                                                                                         minute=int(stm[1]))]

def datetostr(d):
    dt = str(d).split(" ")
    return dt[0]

def timetostr(d):
    dt = str(d).split(" "); dt = str(dt[1]).split(":")
    return dt[0] + ":" + dt[1]

def formattoday():
    return datetostr(datetime.datetime.now()) + " " + timetostr(datetime.datetime.now())


def strtolod(s) -> list:
    global DEMONSLIST
    # [{'n':d,'p':d},{'n':d,'p':d}]
    st = str(s).replace("[",""); st = st.replace("]",""); st = st.split("},")
    for t in st:
        sti = t + "}"
        if sti.startswith(" "): sti = sti[1:]
        if sti[len(sti) - 2:] == "}}": sti = sti[:len(sti) - 1]
        sti = ast.literal_eval(sti)
        try: sti['position'] = int(sti['position'])
        except: pass
        try: sti['old pos'] = int(sti['old pos'])
        except: pass
        try: sti['new pos'] = int(sti['new pos'])
        except: pass
        try: sti['dif'] = int(sti['dif'])
        except: pass
        st[st.index(t)] = sti
    return st

def paramquotationlist(p):
    params = []
    while True:
        try:
            p1 = p.index("\""); p = p[:p1] + p[p1 + 1:]
            p2 = p.index("\""); p = p[:p2] + p[p2 + 1:]
            params.append(p[p1:p2])
        except ValueError:
            if params == []: return None
            return params

def paramnumberlist(p):
    params = []; i = -1; nf = False; iq = False; tempparam = [""]
    while True:
        try:
            i += 1
            tp = int(p[i])
            if not iq:
                nf = True
                tempparam[0] += str(tp)
        except ValueError:
            if p[i] == " " and iq: iq = False
            if p[i] == "\"" and not iq: iq = True
            if p[i] == " " and nf:
                params.append(int(tempparam[0]))
                tempparam[0] = ""
                nf = False
        except IndexError:
            if nf:
                params.append(int(tempparam[0]))
                tempparam[0] = ""
            if params == []: return None
            return params

DEMONSLIST = []

def DLC_CHANGES(dl1,dl2) -> list:
    """
    :param dl1: (list)
    :param dl2: (list)
    :return:
    [{'name':'Sonic Wave','old pos':5,'new pos':4,'dif':1,'new':False},
    {'name':'Crimson Planet','old pos':0,'new pos':1,'dif':1,'new':True}]
    """
    if dl1 == dl2: return []
    dllog = []
    for d1 in dl1: dllog.append({'name':d1['name'],'p1':d1['position'],'p2':d1['position']})
    for d2 in dl2:
        dgf = False
        for dg in dllog:
            if dg['name'] == d2['name']:
                dgf = True
                if d2['position'] != dg['p1']:
                    dg['p2'] = d2['position']
        if not dgf: dllog.append({'name':d2['name'],'p1':0,'p2':d2['position']})
    dlchanges = []
    for dg in dllog:
        dgn = False
        dgd = 1
        if dg['p1'] == 0: dgn = True
        else: dgd = dg['p1'] - dg['p2']
        dlchanges.append({'name':dg['name'],'old pos':dg['p1'],'new pos':dg['p2'],'dif':dgd,'new':dgn})
    dln = []
    for dlc in dlchanges:
        if dlc['dif'] != 0: dln.append(dlc)
    dlchanges = dln
    return dlchanges

def DLC_SIMULATECHANGE(dlo,c):
    """
    :param dlo: (list)
    :param c:
    [{'name':'Sonic Wave','new pos':4,'new':False},{'name':'Crimson Planet','new pos':1,'new':True}]
    :return: (list)
    """
    if len(c) == 0: return dlo
    dl = copy.deepcopy(dlo)
    for d in dl:
        for dc in c:
            if d['name'] == dc['name']:
                dcdif = d['position'] - dc['new pos']
                dmoved = []
                if dcdif > 0:
                    for ad in range(dc['new pos'],d['position']):
                        for dr in dl:
                            if dr['position'] == ad and dr['name'] not in dmoved:
                                dr['position'] += 1
                                dmoved.append(dr['name'])
                elif dcdif < 0:
                    for ad in range(d['position'],dc['new pos'] + 1):
                        for dr in dl:
                            if dr['position'] == ad and dr['name'] not in dmoved:
                                dr['position'] -= 1
                                dmoved.append(dr['name'])
                d['position'] = dc['new pos']
    for dc in c:
        if dc['new']:
            dmoved = []
            for ad in range(dc['new pos'],len(dl)):
                for d in dl:
                    if d['position'] == ad and d['name'] not in dmoved:
                        d['position'] += 1
                        dmoved.append(d['name'])
            dcstate = "MAIN"
            if dc['new pos'] > 50: dcstate = "EXTENDED"
            if dc['new pos'] > 100: dcstate = "LEGACY"
            dl.append({'name':dc['name'],'position':dc['new pos'],'state':dcstate})
    return sorted(dl,key=operator.itemgetter('position'))

def DLC_FORMAT(l):
    # {'name':'Sonic Wave','old pos':5,'new pos':4,'dif':1,'new':False}
    dlcm = CHAR_NEUTRAL
    dlcf = ""
    if l['dif'] > 0: dlcm = CHAR_UP; dlcf = "**"
    if l['dif'] < 0: dlcm = CHAR_DOWN; dlcf = "*"

    if l['new']: dlc = CHAR_NEW + " [**" + str(l['new pos']) + "**] **" + l['name'] + "**"
    else: dlc = dlcm + str(l['dif']) + " [" + dlcf + str(l['new pos']) + dlcf + "] " + dlcf + l['name'] + dlcf
    return dlc

def DLC_LISTTOSTR(l,fl):
    lt = ""
    for t in l:
        for ft in fl:
            if t['name'] in ft:
                if t['important'] or t['new']: lt += ft + "\n"
    return lt


def PLAYERDATA(id):
    if id is None: return None
    url = "https://pointercrate.com/api/v1/players/" + str(id)
    rq = urllib.request.Request(url)
    try: rt = str(urllib.request.urlopen(rq).read())
    except: return None
    rt = rt[2:len(rt) - 1]; rt = rt.replace("\\n",""); rt = rt.replace("  ","")
    rj = json.loads(rt)
    return rj['data']

def POINTSFORMULA(data):
    if data is None: return None
    # requires data from PLAYERDATA()
    s = 0
    for d in data['beaten']:
        if int(d['position']) <= 100:
            s += (100 / ((100/5) + ((-100/5) + 1) * math.exp(-0.008*int(d['position']))))
    for d in data['verified']:
        if int(d['position']) <= 100:
            s += (100 / ((100/5) + ((-100/5) + 1) * math.exp(-0.008*int(d['position']))))
    return s

def DEMONSLISTREFRESH():
    global DEMONSLIST
    url1 = "https://pointercrate.com/api/v1/demons?limit=100"
    url2 = "https://pointercrate.com/api/v1/demons?position__gt=101"
    rq1 = urllib.request.Request(url1); rq2 = urllib.request.Request(url2)
    try: rt1 = str(urllib.request.urlopen(rq1).read()); rt2 = str(urllib.request.urlopen(rq2).read())
    except:
        print("[Demons List] Could not access the Demons List!")
        return
    rt1 = rt1[2:len(rt1) - 3]; rt2 = rt2[2:len(rt2) - 3]
    rt1 = rt1.replace("\\n", ""); rt2 = rt2.replace("\\n", "")
    rt1 = rt1.replace("  ", ""); rt2 = rt2.replace("  ", "")
    rj1 = json.loads(rt1); rj2 = json.loads(rt2)
    DEMONSLIST = []
    for d1 in rj1: DEMONSLIST.append(d1)
    for d2 in rj2: DEMONSLIST.append(d2)
    print("[Demons List] Top Demons refreshed")
    # Ex: 2018-12-25 14:30=[demonslist]
    if getlatest("changesdata.txt") is None:
        datasettings(file="changesdata.txt",method="add",newkey=formattoday(),newvalue=str(DEMONSLIST))
    else:
        if datasettings(file="changesdata.txt",method="get",line=getlatest("changesdata.txt")) != str(DEMONSLIST):
            datasettings(file="changesdata.txt",method="add",newkey=formattoday(),newvalue=str(DEMONSLIST))

def inallowedguild(g,m):
    # 0=No Admin needed,1=Admin needed
    allowedguilds = [[162862229065039872,0],[395654171422097420,1],[503422247927808010,1]]
    for ag in allowedguilds:
        if ag[0] == g.id:
            if ag[1] == 1: return memberadmin(m)
            return True
    return False

CURRENTCHANGES = []

@client.event
async def on_ready():
    print("Bot Ready!")
    print("Name: " + client.user.name + ", ID: " + str(client.user.id))
    sl = ""
    DEMONSLISTREFRESH()
    for server in client.guilds: sl += server.name + ", "
    print("Connected Guilds: " + sl[:len(sl) - 2])



@client.event
async def on_guild_join(guild):
    print("[" + client.user.name + "] Server List updated")
    sl = ""
    for server in client.guilds: sl += server.name + ", "
    print("Connected Servers: " + sl[:len(sl) - 2])



@client.event
async def on_message(message):
    global DEMONSLIST; global SIMULATED; global CURRENTCHANGES
    if str(message.content).startswith("??updateschannel "):
        if not memberadmin(message.author):
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send("**Error**: You are not an Administrator!")
        else:
            ucm = str(message.content).replace("??updateschannel ", "")
            ucc = getchannel(message.guild, ucm)
            if ucc is None:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: Invalid channel!")
            else:
                if datasettings(file="changesguilds.txt", method="get", line="UPDATES" + str(message.guild.id)) is None:
                    datasettings(file="changesguilds.txt", method="add", newkey="UPDATES" + str(message.guild.id),
                                 newvalue=str(ucc.id))
                    await message.add_reaction(CHAR_SUCCESS)
                    await message.channel.send("**" + message.author.name + "**: UPDATES CHANNEL set to *" +
                                               ucc.name + "*")
                else:
                    datasettings(file="changesguilds.txt", method="change", line="UPDATES" + str(message.guild.id),
                                 newvalue=str(ucc.id))
                    await message.add_reaction(CHAR_SUCCESS)
                    await message.channel.send("**" + message.author.name + "**: UPDATES CHANNEL changed to *" +
                                               ucc.name + "*")
    if str(message.content).startswith("??changes"):
        if inallowedguild(message.guild,message.author):
            if CURRENTCHANGES != []:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: Already have changes active!")
            else:
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send("**" + message.author.name + "**: Checking for List Changes...")
                DEMONSLISTREFRESH()
                dlchanges = []
                if not SIMULATED: dlchanges = DLC_CHANGES(strtolod(datasettings(file="changesdata.txt", method="get",
                                                                          line=getsecondlatest("changesdata.txt"))),
                                            strtolod(datasettings(file="changesdata.txt", method="get",
                                                                          line=getlatest("changesdata.txt"))))
                else:
                    await message.channel.send("*SIMULATED CHANGES btw*")
                    dlchanges = DLC_CHANGES(DEMONSLIST,strtolod(datasettings(file="changessim.txt", method="get",
                                                                          line=getlatest("changessim.txt"))))
                if dlchanges != []:
                    await message.channel.send("**" + message.author.name + "**: Found Changes!")
                    if len(dlchanges) > 2:
                        dlccdl = []
                        for dlc in dlchanges: dlccdl.append(int(dlc['dif']))
                        dlccdlo = []
                        for di in dlccdl:
                            diov = False
                            for dio in dlccdlo:
                                if dio[0] == di: dio[1] += 1
                                diov = True
                                break
                            if not diov: dlccdlo.append([di,1])
                        diol = [0,1]
                        for dio in dlccdlo:
                            if dio[1] >= diol[1]: diol = dio
                        dlccd = abs(diol[0])
                        for dlc in dlchanges:
                            if dlc['dif'] > dlccd or dlc['dif'] < -dlccd:
                                dlc.update({'important': True})
                            else:
                                dlc.update({'important': False})
                    else:
                        for dlc in dlchanges: dlc.update({'important': True})
                    datasettings(file="changesc.txt", method="add", newkey=formattoday(), newvalue=str(dlchanges))
                    CURRENTCHANGES.append(dlchanges)
                    dlcfcl = []
                    for dlc in dlchanges: dlcfcl.append(DLC_FORMAT(dlc))
                    dlformattedchanges = DLC_LISTTOSTR(dlchanges,dlcfcl)
                    await message.channel.send(dlformattedchanges)
                    await message.channel.send("**" + message.author.name + "**: Changes logged. Use ??sendchanges to send "
                                                                            "the changes to servers!")
                else:
                    await message.channel.send("**" + message.author.name +
                                               "**: No Updates found for the Demons List!  (Last Updated: "
                                               + getlatest("changesdata.txt") + ")")
    if str(message.content).startswith("??currentchanges"):
        if inallowedguild(message.guild, message.author):
            if len(CURRENTCHANGES) == 0:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: No active changes found!")
            else:
                dlchanges = CURRENTCHANGES[0]
                dlcfcl = []
                for dlc in dlchanges: dlcfcl.append(DLC_FORMAT(dlc))
                dlformattedchanges = DLC_LISTTOSTR(dlchanges, dlcfcl)
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send(dlformattedchanges)
    if str(message.content).startswith("??highlight "):
        if inallowedguild(message.guild, message.author):
            hdm = str(message.content).replace("??highlight ", ""); hdp = paramquotationlist(hdm)
            if hdp is None:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: Invalid parameters!")
            else:
                hdf = False
                for d in DEMONSLIST:
                    if d['name'].lower() == str(hdp[0]).lower(): hdf = True
                if not hdf:
                    await message.add_reaction(CHAR_FAILED)
                    await message.channel.send("**Error**: Demon not found!")
                else:
                    dlchanges = strtolod(
                        datasettings(file="changesc.txt", method="get", line=getlatest("changesc.txt")))
                    for dlc in dlchanges:
                        if dlc['name'].lower() == str(hdp[0]).lower():
                            if dlc['important']:
                                dlc['important'] = False
                                await message.add_reaction(CHAR_SUCCESS)
                                await message.channel.send(
                                    "**" + message.author.name + "**: *" + str(hdp[0]) + "* marked as NOT IMPORTANT")
                                break
                            elif not dlc['important']:
                                dlc['important'] = True
                                await message.add_reaction(CHAR_SUCCESS)
                                await message.channel.send(
                                    "**" + message.author.name + "**: *" + str(hdp[0]) + "* marked as IMPORTANT")
                                break
                    datasettings(file="changesc.txt", method="change", line=getlatest("changesc.txt"),
                                 newvalue=str(dlchanges))
    if str(message.content).startswith("??sendannouncement "):
        if inallowedguild(message.guild,message.author):
            sam = str(message.content).replace("??sendannouncement ",""); sap = paramquotationlist(sam)
            if len(sap) != 1:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: Invalid command!")
            else:
                am = sap[0]
                if am == "" or am == " " or len(am) > 1990:
                    await message.add_reaction(CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid message!")
                else:
                    dlcc = 0
                    if alldatakeys("changesguilds.txt") != []:
                        for gid in alldatakeys("changesguilds.txt"):
                            g = int(str(gid).replace("UPDATES", ""))
                            for guild in client.guilds:
                                if guild.id == g:
                                    cid = int(datasettings(file="changesguilds.txt", method="get", line=gid))
                                    for channel in guild.channels:
                                        if channel.id == cid:
                                            dlcc += 1
                                            try: await channel.send(am)
                                            except: dlcc -= 1
                                            break
                    await message.channel.send(
                        "**" + message.author.name + "**: *Sent Announcement to " + str(dlcc) + " servers*")
    if str(message.content).startswith("??sendchanges"):
        if inallowedguild(message.guild, message.author):
            dlchanges = strtolod(datasettings(file="changesc.txt", method="get", line=getlatest("changesc.txt")))
            if dlchanges is not None:
                dlcfcl = []
                for dlc in dlchanges: dlcfcl.append(DLC_FORMAT(dlc))
                dlformattedchanges = DLC_LISTTOSTR(dlchanges,dlcfcl)
                dlsformatted = "**Demons List Changes** " + getlatest("changesdata.txt") + ":\n" + dlformattedchanges
                dlcc = 0
                if alldatakeys("changesguilds.txt") != []:
                    for gid in alldatakeys("changesguilds.txt"):
                        g = int(str(gid).replace("UPDATES", ""))
                        for guild in client.guilds:
                            if guild.id == g:
                                cid = int(datasettings(file="changesguilds.txt", method="get", line=gid))
                                for channel in guild.channels:
                                    if channel.id == cid:
                                        dlcc += 1
                                        try:
                                            await channel.send(dlsformatted)
                                        except:
                                            dlcc -= 1
                                        break
                await message.channel.send("**" + message.author.name + "**: *Sent Changes to " + str(dlcc) + " servers*")
                CURRENTCHANGES = []
            else:
                await message.channel.send("**" + message.author.name +
                                           "**: No Updates found for the Demons List!  (Last Updated: "
                                           + getlatest("changesdata.txt") + ")")



client.run(SECRET)