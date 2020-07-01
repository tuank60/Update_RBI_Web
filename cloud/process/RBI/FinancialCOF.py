import math
import numpy as np
#from rbi import MYSQL_CAL as DAL_CAL
from cloud.process.RBI import Postgresql as DAL_CAL
from cloud import models

class FinancialCOF: #LEVEL 1
    def __init__(self,proposalID,FLUID,TOXIC_FLUID,toxic_percent,API_COMPONENT_TYPE_NAME,MATERIAL_COST,CA_cmd,CA_inj):
        self.proposalID = proposalID
        self.FLUID = FLUID
        self.TOXIC_FLUID = TOXIC_FLUID
        self.toxic_percent = toxic_percent
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.MATERIAL_COST =MATERIAL_COST
        self.CA_cmd = CA_cmd
        self.CA_inj = CA_inj

    def outage_cmd_n(self,i):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        try:
            if i==1: return obj[9]
            if i==2: return obj[10]
            if i==3: return obj[11]
            if i==4: return obj[12]
        except Exception as e:
            return 0

    def HoleCost(self,i):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        try:
            if i == 1: return obj[5]
            if i == 2: return obj[6]
            if i == 3: return obj[7]
            if i == 4: return obj[8]
        except Exception as e:
            return 0

    def FC_cmd(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        return ((obj[0]*self.HoleCost(1)+obj[1]*self.HoleCost(2)+obj[2]*self.HoleCost(3)+obj[3]*self.HoleCost(4))/obj[4])*self.MATERIAL_COST

    def FC_affa(self):
        try:
            rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
            equipcost = rwInputCa.process_unit
            return self.CA_cmd *equipcost
        except:
            return 0

    def Outage_affa(self):
        try:
            return pow(10,(1.242+0.585*math.log10(self.FC_affa()*pow(10,-6))))
        except Exception as e:
            print(e)
            return 0

    def outage_cmd(self):
        rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
        outage_multiplier = rwInputCa.outage_multiplier
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        return ((obj[0]*obj[9]+obj[1]*obj[10]+obj[2]*obj[11]+obj[3]*obj[12])/obj[4])*outage_multiplier

    def FC_prod(self):
        try:
            rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
            return (self.outage_cmd() + self.Outage_affa()) * rwInputCa.production_cost
        except Exception as e:
            print(e)
            return 0

    def FC_inj(self):
        rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
        popdens = rwInputCa.personal_density
        injcost = rwInputCa.injure_cost
        return self.CA_inj * popdens * injcost

    def NBP(self):
        data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
        nbp  = ((data[2] -32)/1.8)
        return nbp

    def frac_evap(self):
        try:
            C12= DAL_CAL.POSTGRESQL.GET_TBL_3B21(12)
            C41 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(41)
            return -7.1408 + 8.5827*math.pow(10,-3)*C12*(self.NBP()+C41)-3.5594*pow(10,-6)*pow((C12*(self.NBP()+C41)),2)+(2331.1/(C12*(self.NBP()+C41)))-(203545/pow((C12*(self.NBP()+C41)),2))
        except:
            return 0

    def mass_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i==1:
            return rwcofholesize.mass_n_small
        elif i==2:
            return rwcofholesize.mass_n_medium
        elif i==3:
            return rwcofholesize.mass_n_large
        else:
            return rwcofholesize.mass_n_rupture

    def liquid_density(self):
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            return data[1] * 16.02
            # return data[1]
        except:
            return 0

    def Vol_env_n(self,i):
        try:
            C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
            return (C13*self.mass_n(i)*(1-self.frac_evap()))/self.liquid_density()
        except:
            return 0

    def FC_environ(self):
        try:
            rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
            evironment_cost = rwInputCa.evironment_cost
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            x = obj[0]*self.Vol_env_n(1) + obj[1]*self.Vol_env_n(2) + obj[2]*self.Vol_env_n(3) + obj[3]*self.Vol_env_n(4)
            return (x/obj[4])*evironment_cost
        except:
            return 0

    def FC_total(self):
        try:
            return self.FC_cmd()+self.FC_affa()+self.FC_prod()+self.FC_inj()+self.FC_environ()
        except:
            return 0

    def FC_Category(self):
        if (self.FC_total() <= 10000):
            return "A"
        elif (self.FC_total() <= 100000):
            return "B"
        elif (self.FC_total() <= 1000000):
            return "C"
        elif (self.FC_total() <= 10000000):
            return "D"
        else:
            return "E"

