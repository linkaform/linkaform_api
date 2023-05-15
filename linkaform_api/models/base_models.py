# coding: utf-8
#!/usr/bin/python

#python libs
import re
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, validator, StrictBool, AnyUrl
from bson import ObjectId
from typing import (
    Deque, Optional, Union, List
)
from uuid import UUID

#lkf libs
# from ..utils import InvalidAPIUsage
from ..settings import *

##Basic models

class UnitTime(BaseModel):
    value: int
    value_unit: str
    seconds: int = 0
    kind: Optional[str]

    @validator('value_unit')
    def value_unit_valid(cls, v):
        value_type_options = ['seconds','minutes','hours','days','weeks','months']
        if v and v not in value_type_options:
            raise InvalidAPIUsage('user_type: Resource Type {}, is not a valid options'.format(v, value_type_options))
        return v

    @validator('seconds')
    def seconds_valid(cls, v, values):
        unit = values['value_unit']
        value = values['value']
        x = 1
        if unit == 'minutes':
            x =  60
        elif unit == 'hours':
            x =  3600
        elif unit == 'days':
            x =  86400
        elif unit == 'weeks':
            x =  604800
        return value * x

class Geolocation(BaseModel):
    lat: float
    long: float

class UserAddress(BaseModel):
    name:str
    street:str
    municipality:str
    city:str
    zip:int
    country:str
    geolocation:Optional[Geolocation]

class RelationTask(BaseModel):
    # realation: Literal['CHILD,PARENT,SIBLING']
    task_id:str

class UserPhone(BaseModel):
    ph_type: str
    country_code: str
    phone: int

    @validator('phone')
    def phone_valid(cls, value):
        value_str = str(value)
        if len(value_str) == 10:
            return value
        else:
            raise InvalidAPIUsage('Phone number must be 10 digits long')

    @validator('country_code')
    def country_code_valid(cls, value):
        starts = value[:1]
        if starts == '+':
            code = int(value[1:])
        else:
            code = int(value)
        if code > 999:
            raise InvalidAPIUsage('Country code MUST be lower than 1000')
        return '+{}'.format(code)

class UserData(BaseModel):
    account_id: int
    user_id: int
    name: str
    resource_id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    group_id: Optional[int]
    resource_kind: Optional[str]
    user_type: Optional[list] #Literal['follower', 'onwer', 'supervisor', 'admin']]
    phone: Optional[List[UserPhone]]
    properties: Optional[dict]
    user_icon: Optional[AnyUrl]
    user_url: Optional[AnyUrl]
    user_tag: Optional[List[str]]
    timezone: Optional[str]

    @validator('user_type')
    def usertype_valid(cls, v):
        user_type_options = ['follower', 'onwer', 'supervisor', 'admin']
        if v and v not in user_type_options:
            raise InvalidAPIUsage('user_type: User Type {}, is not a valid options'.format(v, user_type_options))
        return v

    @validator('resource_kind')
    def resource_valid(cls, v):
        _options = ['user','group','catalog_id']
        if v and v not in _options:
            raise InvalidAPIUsage('user_type: Resource Kind {}, is not a valid options'.format(v, _options))
        return v

    @validator('email')
    def email_valid(cls, v):
        print('v',v)
        email = v.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise InvalidAPIUsage('email provided is not valid')
        # if User.query.filter_by(email=email).first():
        #     raise InvalidAPIUsage('email already registered')
        return v

class ResourceData(BaseModel):
    resource_id: str
    resouce_name: str
    resouce_email: str
    catalog_id: Optional[int]
    phone: Optional[List[UserPhone]]
    user_icon: Optional[AnyUrl]
    user_url: Optional[AnyUrl]
    properties: Optional[dict]
    resource_type: Optional[str]
    resource_tag: Optional[List[str]]
    role: Optional[str]

    @validator('resource_type')
    def resource_type_valid(cls, v, values, **kwargs):
        resource_type_options = ['branch', 'user', 'asset', 'supplier', 'customer', 'partner']
        if v not in resource_type_options:
            raise InvalidAPIUsage('Resource Type {}, is not a va valid options'.format(v, resource_type_options))

    @validator('resouce_email')
    def resouce_email_valid(cls, v):
        email = v.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise InvalidAPIUsage('email provided is not valid')
        # if User.query.filter_by(email=email).first():
        #     raise InvalidAPIUsage('email already registered')
        return v

##DagUtils
class DagDefaultArgs(BaseModel):
    email: list
    retries: Optional[int] = 3
    email_on_failure : StrictBool
    retry_delay : str


    # custom validation on email field
    @validator('email')
    def email_valid(cls, value_list):
        for v in value_list:
            email = v.lower()
            if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
                raise InvalidAPIUsage('email provided is not valid')
            # if User.query.filter_by(email=email).first():
            #     raise InvalidAPIUsage('email already registered')
        return value_list

class DagParams(BaseModel):
    api_key: str

class DagScheduleConfig(BaseModel):
    daily :Optional[StrictBool]
    hourly: Optional[StrictBool]
    weekly: Optional[StrictBool]
    monthly: Optional[StrictBool]
    yearly: Optional[StrictBool]
    at_beginning :Optional[StrictBool]
    every_week_day:Optional[Union[int, str, list]]
    week_number: Optional[int]
    every_month: Optional[Union[int, str]]
    every_other_month: Optional[int]
    every_day: Optional[Union[int, str]]
    every_other_day: Optional[int]
    every_hour: Optional[Union[int, str]]
    every_other_hour: Optional[int]
    every_minute: Optional[Union[int, str]]
    every_other_minute: Optional[int]


    @validator('every_week_day')
    def every_week_day_valid(cls, value):
        valid_options = ['weekdays','sunday', 'sun', 'monday','mon', 'tuesday', 'tues', 'wednesday',
        'wed', 'thursday','thur', 'friday', 'fri', 'saturday', 'sat']
        if isinstance(value, str):
            value = [value,]
        for val in value:
            if val not in valid_options:
                raise InvalidAPIUsage('Every Week day {} is not a valid option'.format(val))
        return value

    @validator('every_day')
    def every_day_valid(cls, value):
        if value == '*':
            return value
        value = int(value)
        if value < 1 or value > 31:
            raise InvalidAPIUsage('Every Day must be between 1 and 31')
        return value

    @validator('every_other_day')
    def every_other_day_valid(cls, value):
        if value == '*':
            return value
        value = int(value)
        if value < 1 or value > 30:
            raise InvalidAPIUsage('Every Other Day must be between 1 and 30')
        return value

    @validator('every_hour')
    def every_hour_valid(cls, value):
        if value == '*':
            return value
        value = int(value)
        if value < 0 or value > 23:
            raise InvalidAPIUsage('Every Hour must be between 1 and 23')
        return value

    @validator('every_other_hour')
    def every_other_hour_valid(cls, value):
        if value < 0 or value > 23:
            raise InvalidAPIUsage('Every Other Hour must be between 1 and 22')
        return value

    @validator('every_minute')
    def every_minute_valid(cls, value):
        if value == '*':
            return value
        value = int(value)
        if value < 0 or value > 60:
            raise InvalidAPIUsage('Every Minute must be between 1 and 60')
        return value

    @validator('every_other_minute')
    def every_other_minutevalid(cls, value):
        if value < 1 or value > 59:
            raise InvalidAPIUsage('Every Minute must be between 1 and 59')
        return value

    @validator('week_number')
    def week_number_valid(cls, value):
        if value < 1 or value > 5:
            raise InvalidAPIUsage('Week Number must be between 1 and 5')
        return value

    @validator('every_month')
    def every_month_valid(cls, value):
        if value == '*':
            return value
        value = int(value)
        if value < 1 or value > 12:
            raise InvalidAPIUsage('Every Month must be between 1 and 12')
        return value

    @validator('every_other_month')
    def every_other_month_valid(cls, value):
        if value < 1 or value > 11:
            raise InvalidAPIUsage('Every Month must be between 1 and 11')
        return value

class DagDagParams(BaseModel):
    #https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dagrun/index.html#airflow.models.dagrun.DagRun
    schedule_config: Optional[DagScheduleConfig]
    schedule_interval :Optional[str]
    dag_id_suffix: Optional[str]
    start_date: datetime
    end_date: Optional[datetime]
    due_window_time: UnitTime = {'value':1, 'value_unit':'hours'}
    concurrency: int
    catchup: StrictBool
    duration: Optional[float]

class DagAssign(BaseModel):
    assign_users: Optional[List[UserData]]
    assign_in_advance: UnitTime = {'value':2, 'value_unit':'hours'}

class DagTaskParams(BaseModel):
    script_id:Optional[int]
    form_id:Optional[int]
    assigne_user_id:Optional[int]
    answers:Optional[dict]

    # @validator('assigne_user_id')
    # def assigne_user_id_valid(cls, v, values, **kwargs):
    #     return v

class DagTasks(BaseModel):
    id: Optional[str]
    name: str
    operator_lib: str
    operator: str
    cron_model_id: str
    # downstream_task_id:Optional[int]
    downstream_task_id: Optional[List[int]]
    params:Optional[DagTaskParams]

    # @validator('operator')
    # def operator_valid(cls, v, values, **kwargs):
    #     operator_lib = values.get('operator_lib')
    #     valid_operators = settings.config['LKF_OPERATORS']
    #     if operator_lib == 'lkf_operator':
    #         if v not in valid_operators:
    #             raise InvalidAPIUsage('Operator {}, is not a va valid lkf_operator: {}'.format(v, valid_operators))
    #     return v
