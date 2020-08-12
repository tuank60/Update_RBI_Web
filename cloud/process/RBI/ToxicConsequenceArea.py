import math
import numpy as np
#from rbi import MYSQL_CAL as DAL_CAL
from cloud.process.RBI import Postgresql as DAL_CAL
from cloud import models

class CA_Toxic: #LEVEL 1
    def __init__(self,proposalID,TOXIC_FLUID,ReleasePhase,toxic_percent,API_COMPONENT_TYPE_NAME):
        self.proposalID = proposalID
        self.TOXIC_FLUID = TOXIC_FLUID
        self.ReleasePhase =ReleasePhase
        self.toxic_percent = toxic_percent
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME

    def ld_n_max(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i==1:
            return rwcofholesize.ld_max_n_small
        elif i==2:
            return rwcofholesize.ld_max_n_medium
        elif i==3:
            return rwcofholesize.ld_max_n_large
        else:
            return rwcofholesize.ld_max_n_rupture

    def mass_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.mass_n_small
        elif i == 2:
            return rwcofholesize.mass_n_medium
        elif i == 3:
            return rwcofholesize.mass_n_large
        else:
            return rwcofholesize.mass_n_rupture

    def W_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.wn_small
        elif i == 2:
            return rwcofholesize.wn_medium
        elif i == 3:
            return rwcofholesize.wn_large
        else:
            return rwcofholesize.wn_rupture

    def ReleasetType(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.releasetype_small
        elif i == 2:
            return rwcofholesize.releasetype_medium
        elif i == 3:
            return rwcofholesize.releasetype_large
        else:
            return rwcofholesize.releasetype_rupture

    def ld_tox_n(self,i):
        try:
            return min(3600,(self.mass_n(i)/self.W_n(i)),(60*self.ld_n_max(i)))
        except:
            return 0

    def ContantC(self,i):
        if self.TOXIC_FLUID == "HF Acid":
            if self.ReleasetType(i)=="Continuous":
                return 1.1401
            else:
                return 1.4056
        elif self.TOXIC_FLUID == "H2S":
            if self.ReleasetType(i)=="Continuous":
                return 1.2411
            else:
                return 0.974
        else:
            return 0

    def ContantD(self,i):
        if self.TOXIC_FLUID == "HF Acid":
            if self.ReleasetType(i)=="Continuous":
                return 3.5683
            else:
                return 33.606
        elif self.TOXIC_FLUID == "H2S":
            if self.ReleasetType(i)=="Continuous":
                return 3.9686
            else:
                return 2.7840
        else:
            return 0

    def ContantE(self,i):
        if self.TOXIC_FLUID == "Ammonia":
            if self.ReleasetType(i)=="Continuous":
                return 636.7
            else:
                return 2.684
        elif self.TOXIC_FLUID == "Chlorine":
            if self.ReleasetType(i)=="Continuous":
                return 3350
            else:
                return 3.528
        elif self.TOXIC_FLUID == "AlCl3" :
            if self.ReleasePhase=="Gas":
                return 3.4531
            else:
                return 0
        elif self.TOXIC_FLUID == "CO" :
            if self.ReleasePhase=="Gas":
                return 9.55
            else:
                return 0
        elif self.TOXIC_FLUID == "HCl" :
            if self.ReleasePhase=="Gas":
                return 47.39
            else:
                return 0
        elif self.TOXIC_FLUID == "Nitric Acid" :
            if self.ReleasePhase=="Gas":
                return 13230.9
            else:
                return 1114.96
        elif self.TOXIC_FLUID == "NO2" :
            if self.ReleasePhase=="Gas":
                return 1071.74
            else:
                return 430
        elif self.TOXIC_FLUID == "Phosgene" :
            if self.ReleasePhase=="Gas":
                return 3095.33
            else:
                return 733.39
        elif self.TOXIC_FLUID == "TDI" :
            if self.ReleasePhase=="Gas":
                return 0
            else:
                return 793.04
        elif self.TOXIC_FLUID == "EE" :
            if self.ReleasePhase=="Gas":
                return 0.8954
            else:
                return 0
        elif self.TOXIC_FLUID == "EO" :
            if self.ReleasePhase=="Gas":
                return 0.5085
            else:
                return 0
        elif self.TOXIC_FLUID == "PO" :
            if self.ReleasePhase=="Gas":
                return 0.0008
            else:
                return 0
        else:
            return 0

    def ContantF(self,i):
        if self.TOXIC_FLUID == "Ammonia":
            if self.ReleasetType(i)=="Continuous":
                return 1.183
            else:
                return 0.9011
        elif self.TOXIC_FLUID == "Chlorine":
            if self.ReleasetType(i)=="Continuous":
                return 1.097
            else:
                return 1.177
        elif self.TOXIC_FLUID == "AlCl3" :
            if self.ReleasePhase=="Gas":
                return 0.9411
            else:
                return 0
        elif self.TOXIC_FLUID == "CO" :
            if self.ReleasePhase=="Gas":
                return 1.15
            else:
                return 0
        elif self.TOXIC_FLUID == "HCl" :
            if self.ReleasePhase=="Gas":
                return 1.09
            else:
                return 0
        elif self.TOXIC_FLUID == "Nitric Acid" :
            if self.ReleasePhase=="Gas":
                return 1.25
            else:
                return 1.08
        elif self.TOXIC_FLUID == "NO2" :
            if self.ReleasePhase=="Gas":
                return 0.70
            else:
                return 0.98
        elif self.TOXIC_FLUID == "Phosgene" :
            if self.ReleasePhase=="Gas":
                return 1.20
            else:
                return 1.06
        elif self.TOXIC_FLUID == "TDI" :
            if self.ReleasePhase=="Gas":
                return 0
            else:
                return 1.06
        elif self.TOXIC_FLUID == "EE" :
            if self.ReleasePhase=="Gas":
                return 1.171
            else:
                return 0
        elif self.TOXIC_FLUID == "EO" :
            if self.ReleasePhase=="Gas":
                return 1.222
            else:
                return 0
        elif self.TOXIC_FLUID == "PO" :
            if self.ReleasePhase=="Gas":
                return 1.913
            else:
                return 0
        else:
            return 0

    def mfrac_tox(self):
        return self.toxic_percent

    def Rate_tox_n(self,i):
        return (self.mfrac_tox() * self.W_n(i))/100

    def Mass_tox_n(self,i):
        return (self.mass_n(i) * self.mfrac_tox())/100

    def CA_tox_Cont_inj_n(self,i):
        try:
            C8 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(8)
            C4 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(4)
            if self.TOXIC_FLUID == "HF Acid" or self.TOXIC_FLUID == "H2S":
                return C8 * math.pow(10,(self.ContantC(i)*math.log10(C4*self.Rate_tox_n(i))+self.ContantD(i)))
            else:
                return self.ContantE(i) * pow(self.Rate_tox_n(i),self.ContantF(i))
        except Exception as e:
            print(e)

    def CA_tox_Inst_inj_n(self, i):
        try:
            C8 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(8)
            C4 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(4)
            if self.TOXIC_FLUID == "HF Acid" or self.TOXIC_FLUID == "H2S":
                return C8 * math.pow(10,(self.ContantC(i) * math.log10(C4 * self.Mass_tox_n(i)) + self.ContantD(i)))
            else:
                return self.ContantE(i) * pow(self.Mass_tox_n(i), self.ContantF(i))
        except Exception as e:
            print(e)

    def CA_toxic(self,i):
        return min(self.CA_tox_Cont_inj_n(i),self.CA_tox_Inst_inj_n(i))

    def CA_toxic_inj(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        return (obj[0] * self.CA_toxic(1) + obj[1] * self.CA_toxic(2) + obj[2] * self.CA_toxic(3) + obj[3] * self.CA_toxic(4)) / obj[4]


    #None Toxic

    def Rate_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.rate_n_small
        elif i == 2:
            return rwcofholesize.rate_n_medium
        elif i == 3:
            return rwcofholesize.rate_n_large
        else:
            return rwcofholesize.rate_n_rupture

    def NoneCA_cont_Inj_n(self,i):
        C9 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(9)
        return C9 * self.Rate_n(i)

    def NoneCA_Inst_Inj_n(self,i):
        C10 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(10)
        return C10 * pow(self.mass_n(i),0.6384)

    def Fact_IC(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.factIC_n_small
        elif i == 2:
            return rwcofholesize.factIC_n_medium
        elif i == 3:
            return rwcofholesize.factIC_n_large
        else:
            return rwcofholesize.factIC_n_rupture

    def NoneCA_leck_Inj_n(self,i):
        try:
            return self.NoneCA_Inst_Inj_n(i)*self.Fact_IC(i)+self.NoneCA_cont_Inj_n(i)(1-self.Fact_IC(i))
        except:
            return 0

    def NoneCA_leck(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return (obj[0] * self.NoneCA_leck_Inj_n(1) + obj[1] * self.NoneCA_leck_Inj_n(2) + obj[2] * self.NoneCA_leck_Inj_n(3) + obj[
                3] * self.NoneCA_leck_Inj_n(4)) / obj[4]
        except:
            return 0

    def CA_total(self, flammable_cmd,flammable_inj):
        print("tuan")
        cainj = max(flammable_inj,self.CA_toxic_inj(),self.NoneCA_leck())
        return max(flammable_cmd,cainj)

    def CA_Category(self,flammable_cmd,flammable_inj):
        if (self.CA_total(flammable_cmd,flammable_inj) <= 9.29):
            return "A"
        elif (self.CA_total(flammable_cmd,flammable_inj) <= 92.9):
            return "B"
        elif (self.CA_total(flammable_cmd,flammable_inj) <= 279):
            return "C"
        elif (self.CA_total(flammable_cmd,flammable_inj) <= 929):
            return "D"
        else:
            return "E"