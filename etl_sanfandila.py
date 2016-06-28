from datetime import datetime

from linkaform_api import settings
from linkaform_api import network

config = {
    'USERNAME' : 'infosync@sanfandila.com',
    'PASS' : '123456',
    'COLLECTION' : 'form_answer',
    'HOST' : 'db2.linkaform.com',
    'PORT' : 27017,
    'USER_ID' : '414',
    'KEYS_POSITION' : {},
    'IS_USING_APIKEY' : True,
    'AUTHORIZATION_EMAIL_VALUE' : 'infosync@sanfandila.com',
    'AUTHORIZATION_TOKEN_VALUE' : '530bd4396d7ffd9f6ee76aea4f621e7d00cd9e21',
}

max_days = 7 * 5

settings.config = config


cr = network.get_collections()

def get_all_farms():
    all_farms = cr.distinct('answers.000000000000000000000002')
    return all_farms

def get_all_receptions():
    query = {'form_id':2760,
            'answers.000000000000000000000001' : { '$exists': True },
            'answers.000000000000000000000002' : { '$exists': True },
            'answers.276000000000000000000006' : { '$exists': True }}
    recived_pigs = cr.find(query , {'answers':1, 'folio':1})
    pigs = []
    print 'stating recived pigs = ', recived_pigs.count()
    receptions_by_date = {}
    for recibos in recived_pigs:
        date = recibos['answers']['000000000000000000000001']
        if not receptions_by_date.has_key(date):
            receptions_by_date[date] = []
        res = {'fecha': recibos['answers']['000000000000000000000001'],
        'granja': recibos['answers']['000000000000000000000002'],
        'cerdos': recibos['answers']['276000000000000000000006'],}
        receptions_by_date[date].append(res)
    return receptions_by_date

def get_calendar():
    calenar_weeks = cr.find({'form_id': 6335}, {'answers':1})
    calendar = {}
    for weeks in calenar_weeks:
        date = weeks['answers']['f00000000000000000000001']
        week = weeks['answers']['f00000000000000000000002']
        year = weeks['answers']['f00000000000000000000003']
        year_week =  str(year) + '/' + '%02d'%week
        if not calendar.has_key(date):
            calendar[date] = year_week
        #calendar[date].append(year_week)
    return calendar

def populate_weeks(all_farms, weeks):
    print ' weeks', weeks
    res = {}
    for week in weeks:
        print 'week', week
        res[week] = {'semana':week}
        for farm in all_farms:
            res[week].update({farm:  0})
    return res

def populate_farms_inventory( all_farms):
    res = {}
    for farm in all_farms:
        res.update({farm:  0})
    return res

def populate_farms(all_farms, frist_week, first_day):
    res = {}
    for farm in all_farms:
        res[farm] = {'last_date': first_day, 'inventory': 0}
    return res

def get_farm_inventory(farms_inventory, reception):
    farm = reception['granja']
    reception_date =  datetime.strptime(reception['fecha'], '%Y-%m-%d')
    last_reception = datetime.strptime(farms_inventory[farm]['last_date'], '%Y-%m-%d')
    days_delta = reception_date - last_reception
    if farm == 'soledad':
        print '777',days_delta
        print 'last_reception', last_reception
        print 'reception_date',reception_date
        print 'days_delta', days_delta
        print 'farms_inventory', farms_inventory['soledad']
        print ' reception[cerdos]',  reception['cerdos']
        print 'farm', farm
        print 'days_delaata',days_delta
    days_delta = days_delta.days
    farms_inventory[farm]['last_date'] = reception['fecha']
    if days_delta > 35:

        farms_inventory[farm]['inventory'] = reception['cerdos']
        if farm == 'soledad':
            print 'reception[cerdos]',reception['cerdos']
            print '----------------------------'
        return farms_inventory, reception['cerdos']
    inventory_addup = farms_inventory[farm]['inventory'] +  reception['cerdos']
    farms_inventory[farm]['inventory'] = inventory_addup
    if farm == 'soledad':
        print 'inventory_addup',inventory_addup
        print '----------------------------'
    return farms_inventory, inventory_addup


all_farms = get_all_farms()
calendar = get_calendar()

recived_pigs = get_all_receptions()
days = recived_pigs.keys()
days.sort()


### Populate the inventory with all the farms with 0 inventory
### Using the first day as the first week
all_weeks = [week[0] for week in  calendar.values()]
all_weeks = list(set(all_weeks))
all_weeks.sort()
#inventory_by_week = populate_weeks(all_farms, all_weeks)
inventory_by_week = {}
farms_inventory = populate_farms(all_farms, calendar[days[0]], days[0])

for day in days:
    farm_done = []
    day_receptions = recived_pigs[day]
    week = calendar[day]
    if not inventory_by_week.has_key(week):
        inventory_by_week[week] = {'semana':week}
        inventory_by_week[week].update(populate_farms_inventory(all_farms))
    for reception in day_receptions:
        farms_inventory, inventory = get_farm_inventory(farms_inventory, reception)
        farm = reception['granja']
        farm_done.append(farm)
        new_inventory = {farm:inventory}
        inventory_by_week[week].update(new_inventory)
    missing_farms = list(set(all_farms) - set(farm_done))
    for missing_farm in missing_farms:
        last_inventory = {missing_farm:farms_inventory[missing_farm]['inventory'] }
        inventory_by_week[week].update(last_inventory)



collecition_inventory = network.get_collections('inventario')
collecition_inventory.drop()
collecition_inventory = network.get_collections('inventario', True)
collecition_inventory.insert(inventory_by_week.values())

# cal_days = calendar.keys()
# cal_days.sort()
# day_farms = []
# for day in cal_days:
#     for farm in all_farms:
#         res = {'Fecha': day,
#                 'Semana Calendario': calendar[day],
#                 'Granja': farm}
#         day_farms.append(res)
