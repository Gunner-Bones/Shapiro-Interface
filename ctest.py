import urllib.request, json, ast, operator, copy, datetime

DEMONSLIST = []

def datetostr(d):
    dt = str(d).split(" ")
    return dt[0]

def timetostr(d):
    dt = str(d).split(" "); dt = str(dt[1]).split(":")
    return dt[0] + ":" + dt[1]


def formattoday():
    return datetostr(datetime.datetime.now()) + " " + timetostr(datetime.datetime.now())

print(formattoday())

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
    print(dlchanges)
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

DEMONSLISTREFRESH()
print(DEMONSLIST)
testchange = DLC_SIMULATECHANGE(DEMONSLIST,[{'name':'Sonic Wave','new pos':1,'new':False},{'name':'Celestial Force','new pos':11,'new':False},{'name':'Crimson Planet','new pos':1,'new':True}])
print(testchange)
print(DLC_CHANGES(DEMONSLIST,testchange))