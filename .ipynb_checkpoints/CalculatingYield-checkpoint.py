
import os as os
#import logging
import numpy as np


import os

os.system('open yieldCalc.xlsm')
os.system('pip install xlwings')

import xlwings as xw
import pandas as pd
from numpy import *

#logging.basicConfig(filename='CalculatingYield.log', level=logging.INFO)

roudning_decimals = 4

Effective_Collection_Fees = {'36A': 0.0003,
                             '36B': 0.0007,
                             '36C': 0.0012,
                             '36D': 0.0019,
                             '36E': 0.0024,
                             '36F': 0.0036,
                             '36G': 0.0035,
                             '36F/G': (0.0036+0.0035)/2,
                             '60A': 0.0002,
                             '60B': 0.0004,
                             '60C': 0.0007,
                             '60D': 0.0011,
                             '60E': 0.0017,
                             '60F': 0.0022,
                             '60G': 0.0032,
                             '60F/G': (0.0022+0.0032)/2,
                             '36NP': 0.0023,
                             '60NP': 0.0017
                             }

def calculate_portfolio_irrs():
    global Effective_Collection_Fees, roudning_decimals

    sht = xw.sheets['Portfolio']

    # Product_Type = 'SP'
    Recovery_Rate = sht.range('D3').value
    Holding_Days = sht.range('D4').value
    Bank_Fee = sht.range('D5').value
    Service_Fee_PI = sht.range('D6').value
    Service_Fee_UPB = sht.range('D7').value
    Effective_Collection_Fee = 0
    Recovery_Fee = sht.range('D8').value

    DATA_PORTFOLIO = xw.sheets['data rates'].range('A2').expand('table').value
    DATA_PORTFOLIO = pd.DataFrame(DATA_PORTFOLIO, columns=['PRODUCT','TERM','GRADE','INTEREST RATE','VOLUME','LOSS MULTIPLIER','PREPAY MULTIPLIER'])

    DATA_CREDIT = xw.sheets['data estimates'].range('A2').expand('table').value
    DATA_CREDIT = pd.DataFrame(DATA_CREDIT, columns=['TERM','GRADE','MOB','UCOR','UPOR'])

    #DATA_FEES = xw.sheets['data fees'].range('A2').expand('table').value
    #DATA_FEES = pd.DataFrame(DATA_FEES, columns=['TERM','GRADE','EFFECTIVE_COLLECTION_FEE'])

    portfolio = DATA_PORTFOLIO.copy(deep=True)

    data_conditional = pd.DataFrame(columns=['TERM','GRADE','INTEREST_RATE','MOB','UPOR','UCOR','DPOR','DCOR','SMM','CPR','MDR','CDR'])

    for index, row in portfolio.iterrows():

        Product = row['PRODUCT']
        Term = int(row['TERM'])
        Grade = row['GRADE']

        if Term == 60 and Grade == 'NP 640-659':
            Grade = 'NP'
        Interest_Rate = np.around(row['INTEREST RATE'],roudning_decimals)
        Weight = np.around(row['VOLUME'],roudning_decimals)

        # Effective Collection Fee
        if 'NP' in Grade:
            Effective_Collection_Fee = Effective_Collection_Fees[str(Term)+'NP']
        else:
            Effective_Collection_Fee = Effective_Collection_Fees[str(Term)+str(Grade)]

        Multiplier_UCOR = row['LOSS MULTIPLIER']
        Multiplier_UPOR = row['PREPAY MULTIPLIER']

        subdata = DATA_CREDIT[(DATA_CREDIT.TERM==Term)&(DATA_CREDIT.GRADE==Grade)]
        UCOR = np.around(Multiplier_UCOR*np.array(subdata.UCOR),roudning_decimals)
        UPOR = np.around(Multiplier_UPOR*np.array(subdata.UPOR),roudning_decimals)

        if sum(UPOR)>=0 and sum(UCOR)>=0 and (sum(UPOR)+sum(UCOR))<=1:

            CF, SMM, CPR, MDR, CDR, DPOR, DCOR, GCL, NCL, ACL, IRR, YIELD, NAR, DURATION = \
            ProjectingReturn(
                        Term,Interest_Rate,
                        UPOR,UCOR,
                        Recovery_Rate,
                        Effective_Collection_Fee,
                        Recovery_Fee,
                        Holding_Days,
                        Service_Fee_PI,
                        Service_Fee_UPB,
                        Bank_Fee
                        )

            data_conditional = data_conditional.append(pd.DataFrame({
                                        'TERM':Term,
                                        'GRADE':Grade,
                                        'INTEREST_RATE':Interest_Rate,
                                        'MOB': np.array(SMM.MOB),
                                        'UPOR': UPOR,
                                        'UCOR': UCOR,
                                        'DPOR': np.around(np.array(DPOR.DPOR),roudning_decimals),
                                        'DCOR': np.around(np.array(DCOR.DCOR),roudning_decimals),
                                        'SMM': np.around(np.array(SMM.SMM),roudning_decimals),
                                        'CPR': np.around(np.array(CPR.CPR),roudning_decimals),
                                        'MDR': np.around(np.array(MDR.MDR),roudning_decimals),
                                        'CDR': np.around(np.array(CDR.CDR),roudning_decimals)}))


        else:
            GCL, NCL, ACL, IRR, DURATION = 0,0,0,0,0

        portfolio.loc[index,'WEIGHT'] = Weight
        portfolio.loc[index,'RATE'] = Interest_Rate
        portfolio.loc[index,'GCL'] = np.around(GCL,roudning_decimals)
        portfolio.loc[index,'NCL'] = np.around(NCL,roudning_decimals)
        portfolio.loc[index,'ACL'] = np.around(ACL,roudning_decimals)
        portfolio.loc[index,'IRR'] = np.around(IRR,roudning_decimals)
        portfolio.loc[index,'DURATION'] = np.around(DURATION,roudning_decimals)

    # Publish Results in Excel
    sht.range('B16').options(index=False).value = portfolio[['PRODUCT','TERM','GRADE','WEIGHT','RATE','GCL','NCL','ACL','IRR','DURATION']]
    sht = xw.sheets['Conditional Rates']
    sht.range('A1').options(index=False).value = data_conditional[['TERM','GRADE','INTEREST_RATE','MOB','UPOR','UCOR','DPOR','DCOR','SMM','CPR','MDR','CDR']]

    # Risk Metrics
    #sht.range('G7').value = Effective_Collection_Fee

    return
    
def IRR():
    global Effective_Collection_Fees, roudning_decimals
    
    sht = xw.sheets['Main']

    Term = int(sht.range('D3').value)
    Grade = str(sht.range('D4').value)

    if Term == 60 and Grade == 'NP 640-659':
        Grade = 'NP'
    Recovery_Rate = sht.range('D6').value

    Holding_Days = sht.range('G3').value
    Bank_Fee = sht.range('G4').value
    Service_Fee_PI = sht.range('G5').value
    Service_Fee_UPB = sht.range('G6').value   
    Effective_Collection_Fee = 0
    Recovery_Fee = sht.range('G8').value

    DATA_RATES = xw.sheets['data rates'].range('A2').expand('table').value
    DATA_RATES = pd.DataFrame(DATA_RATES, columns=['PRODUCT','TERM','GRADE','INTEREST RATE','VOLUME','LOSS MULTIPLIER','PREPAY MULTIPLIER'])

    DATA_CREDIT = xw.sheets['data estimates'].range('A2').expand('table').value
    DATA_CREDIT = pd.DataFrame(DATA_CREDIT, columns=['TERM','GRADE','MOB','UCOR','UPOR'])

#    DATA_FEES = xw.sheets['data fees'].range('A2').expand('table').value
#    DATA_FEES = pd.DataFrame(DATA_FEES, columns=['SOURCE','TERM','GRADE','EFFECTIVE_COLLECTION_FEE'])
   
    #Effective_Collection_Fee = Effective_Collection_Fees[str(Term)+str(Grade)]
    # Collection_Fee = Range('G6').value

    # Effective Collection Fee
    if 'NP' in Grade:
        Effective_Collection_Fee = Effective_Collection_Fees[str(Term)+'NP']
    else:        
        Effective_Collection_Fee = Effective_Collection_Fees[str(Term)+str(Grade)]

    Interest_Rate = DATA_RATES[(DATA_RATES.TERM == Term)&(DATA_RATES.GRADE==Grade)]['INTEREST RATE'].values[0]

    # Read Prepayment/Loss Rate Curves
    CURVE_SOURCE = str(sht.range('D10').value)

    # Stress Factor
    #Stress_UPOR = Range('C11').value
    #Stress_UCOR = Range('D11').value

    # Read CPR/CDR Curves
    if CURVE_SOURCE == 'Custom': # Read from Excel
        if Term == 36:
            UPOR_CUSTOM = sht.range('C13:C48').value
            UPOR = np.array(UPOR_CUSTOM)
            UCOR_CUSTOM = sht.range('D13:D48').value
            UCOR = np.array(UCOR_CUSTOM)
        elif Term == 60:
            UPOR_CUSTOM = sht.range('C13:C72').value
            UPOR = np.array(UPOR_CUSTOM)
            UCOR_CUSTOM = sht.range('D13:D72').value
            UCOR = np.array(UCOR_CUSTOM)

    else: # Read from Dataset
        
       
        subdata = DATA_CREDIT[(DATA_CREDIT.TERM==Term)&(DATA_CREDIT.GRADE==Grade)]
        Multiplier_UCOR = DATA_RATES[(DATA_RATES.TERM == Term)&(DATA_RATES.GRADE==Grade)]['LOSS MULTIPLIER'].values[0]
        Multiplier_UPOR = DATA_RATES[(DATA_RATES.TERM == Term)&(DATA_RATES.GRADE==Grade)]['PREPAY MULTIPLIER'].values[0]

        UCOR = np.around(Multiplier_UCOR*np.array(subdata.UCOR),roudning_decimals)
        UPOR = np.around(Multiplier_UPOR*np.array(subdata.UPOR),roudning_decimals)

        # Adjusting UCOR for certains Term/Grades!
        
    #UPOR = Stress_UPOR*UPOR
    #UCOR = Stress_UCOR*UCOR

    if sum(UPOR)>=0 and sum(UCOR)>=0 and (sum(UPOR)+sum(UCOR))<=1:
           
        # Without Any Fees
        CF0, SMM0, CPR0, MDR0, CDR0, DPOR0, DCOR0, GCL0, NCL0, ACL0, IRR0, YIELD0, NAR0, DURATION0 = \
        ProjectingReturn(
                    Term,Interest_Rate,
                    UPOR,UCOR,
                    Recovery_Rate,
                    Effective_Collection_Fee=0,
                    Recovery_Fee=0,
                    Holding_Days=0,
                    Service_Fee_PI=0,
                    Service_Fee_UPB=0,
                    Bank_Fee=0         
                    )

        # with Collection Fees
        CF1, SMM1, CPR1, MDR1, CDR1, DPOR1, DCOR1, GCL1, NCL1, ACL1, IRR1, YIELD1, NAR1, DURATION1 = \
        ProjectingReturn(
                    Term,Interest_Rate,
                    UPOR,UCOR,
                    Recovery_Rate,
                    Effective_Collection_Fee,
                    Recovery_Fee=0,
                    Holding_Days=0,
                    Service_Fee_PI=0,
                    Service_Fee_UPB=0,
                    Bank_Fee=0         
                    )

        # with Collection Fees, and Recovery Fees
        CF2, SMM2, CPR2, MDR2, CDR2, DPOR2, DCOR2, GCL2, NCL2, ACL2, IRR2, YIELD2, NAR2, DURATION2 = \
        ProjectingReturn(
                    Term,Interest_Rate,
                    UPOR,UCOR,
                    Recovery_Rate,
                    Effective_Collection_Fee,
                    Recovery_Fee,
                    Holding_Days=0,
                    Service_Fee_PI=0,
                    Service_Fee_UPB=0,
                    Bank_Fee=0         
                    )

        # with Collection Fees, Recovery Fees, and Holding Days
        CF3, SMM3, CPR3, MDR3, CDR3, DPOR3, DCOR3, GCL3, NCL3, ACL3, IRR3, YIELD3, NAR3, DURATION3 = \
        ProjectingReturn(
                    Term,Interest_Rate,
                    UPOR,UCOR,
                    Recovery_Rate,
                    Effective_Collection_Fee,
                    Recovery_Fee,
                    Holding_Days,
                    Service_Fee_PI=0,
                    Service_Fee_UPB=0,
                    Bank_Fee=0         
                    )

        # with Collection Fees, Recovery Fees, Holding Days, and Servicing Fees
        CF4, SMM4, CPR4, MDR4, CDR4, DPOR4, DCOR4, GCL4, NCL4, ACL4, IRR4, YIELD4, NAR4, DURATION4 = \
        ProjectingReturn(
                    Term,Interest_Rate,
                    UPOR,UCOR,
                    Recovery_Rate,
                    Effective_Collection_Fee,
                    Recovery_Fee,
                    Holding_Days,
                    Service_Fee_PI,
                    Service_Fee_UPB,
                    Bank_Fee=0         
                    )

        # with Collection Fees, Recovery Fees, Holding Days, Servicing Fees, and Bank Trailing Fees
        CF5, SMM5, CPR5, MDR5, CDR5, DPOR5, DCOR5, GCL5, NCL5, ACL5, IRR5, YIELD5, NAR5, DURATION5 = \
        ProjectingReturn(
                    Term,Interest_Rate,
                    UPOR,UCOR,
                    Recovery_Rate,
                    Effective_Collection_Fee,
                    Recovery_Fee,
                    Holding_Days,
                    Service_Fee_PI,
                    Service_Fee_UPB,
                    Bank_Fee
                    )
               
        CF = CF5[['MOB','UPOR','UCOR','SBB','SP','SIP','SPP','EBB','ESU','EIP','ESPP','EUPP','ED','ER','EWF','ECF','ERF','ESF','ETP','EEB','EPU','DPOR','SMM','CPR','ECU','DCOR','MDR','CDR']]
    
        # Publish Results in Excel
        sht.range('D5').value = Interest_Rate
        sht.range('B12').options(index=False).value = CF
    
        # Risk Metrics
        sht.range('G7').value = Effective_Collection_Fee
        sht.range('J4').value = GCL5
        sht.range('J5').value = NCL5
        sht.range('J6').value = ACL5
        sht.range('J8').value = DURATION5
    
        # IRR
        sht.range('R4').value = IRR0
        sht.range('R5').value = IRR1
        sht.range('R6').value = IRR2
        sht.range('R7').value = IRR3
        sht.range('R8').value = IRR4
        sht.range('R9').value = IRR5
    
        # Yield
        sht.range('S4').value = YIELD0
        sht.range('S5').value = YIELD1
        sht.range('S6').value = YIELD2
        sht.range('S7').value = YIELD3
        sht.range('S8').value = YIELD4
        sht.range('S9').value = YIELD5
    
        # NAR
        sht.range('T4').value = NAR0
        sht.range('T5').value = NAR1
        sht.range('T6').value = NAR2
        sht.range('T7').value = NAR3
        sht.range('T8').value = NAR4
        sht.range('T9').value = NAR5
    elif (sum(UPOR)+sum(UCOR))>1:
        
        sht.range('J4').value = ''
        sht.range('J5').value = ''
        sht.range('J6').value = ''
        sht.range('J8').value = ''

        # IRR
        sht.range('R4').value = ''
        sht.range('R5').value = ''
        sht.range('R6').value = ''
        sht.range('R7').value = ''
        sht.range('R8').value = ''
        sht.range('R9').value = ''

        # Yield
        sht.range('S4').value = ''
        sht.range('S5').value = ''
        sht.range('S6').value = ''
        sht.range('S7').value = ''
        sht.range('S8').value = ''
        sht.range('S9').value = ''
        
        # NAR
        sht.range('T4').value = ''
        sht.range('T5').value = ''
        sht.range('T6').value = ''
        sht.range('T7').value = ''
        sht.range('T8').value = ''
        sht.range('T9').value = ''
        sht.range('U9').value = 'Sum of UCOR and UPOR exceeds 100%.'
        return

def ProjectingReturn(
            Term, # Term in months
            Interest_Rate, # Annual Interest Rate
            UPOR_Curve, # Unit Paid-off Rate
            UCOR_Curve, # Unit Charge-off Rate
            Recovery_Rate,
            Effective_Collection_Fee = 0, # Pre Charge-Off Collection fee; expressed as percentage of all P&I payment (and not just payments from delinquent loans)
            Recovery_Fee = 0, # Post Charge-Off Collection fee; e.g. 18%
            Holding_Days = 0, # Number of holding days by issuing bank; e.g 2-5 days, average 2.8 days
            Service_Fee_PI = 0, # P&I Based servicing fee; e.g. 1%
            Service_Fee_UPB = 0,  # Principal-based servicing fee, Annualized; e.g. 1%
            Bank_Fee = 0 # Trailing (issuing bank) fee; e.g. 0.10%
            ):
              
    r = Interest_Rate/12
    OU0 = 100
    OA0 = 10000
    P = OA0/OU0
    
    T = Term

    # Check UPOR_Curve and UCOR_Curve
    # All data points

    SP = r*(1+r)**T/((1+r)**T-1)*P
      
    CF = pd.DataFrame(columns=['MOB',
                               'SBB','SP','SIP','SPP',
                               'ESU',
                               'EBB',
                               'UCOR','ECU','ED',
                               'EIP','ESPP',
                               'UPOR','EPU','EUPP',
                               'EEB',
                               'SMM','CPR',
                               'MDR','CDR',
                               'DPOR','DCOR'])

    # Generate expected cash flows
    for t in range(1,T+1):

        MOB = t

        # Scheduled payments
        SBB = ((1+r)**T-(1+r)**(t-1))/((1+r)**T-1)*P
        SIP = r*SBB
        SPP = SP-SIP

        if t == 1:
            ESU = OU0
        else:
            ESU = max(CF.ESU[t-1]-CF.EPU[t-1]-CF.ECU[t-1],0)

        # Old Way
        # EBB = ESU*SBB # Expected Beginning Balance        
        if t == 1:
            EBB = ESU*SBB
        else:
            EBB = CF.EEB[t-1]
   
        # Default AMount
        UCOR = UCOR_Curve[int(t-1)]
        ECU = UCOR*OU0
        if t <= 4:        
            ED = ECU*P
        else:
            ED = ECU*CF.SBB[t-4]

        # Expected Scheduled Payments                
        ECU4 = sum(UCOR_Curve[int(t-1):min(t+4,T)])*OU0
        EIP = (ESU-ECU4)*SIP  # Prepaid units also pay interest
        ESPP = (ESU-ECU4)*SPP # Prepaid units also pay scheduled principal

        # Prepayment Amount
        UPOR = UPOR_Curve[int(t-1)]
        EPU = UPOR*OU0
        EUPP = EPU*(SBB-SPP)

        # Expected Ending Balance
        EEB = EBB - ED - ESPP - EUPP

        # Calculating Conditional Rates
        SMM = EUPP/(EBB-(ESU*SPP))
        MDR = ED/EBB

        CPR = 1-(1-SMM)**12.0
        CDR = 1-(1-MDR)**12.0
        
        # DPOR and DCOR
        DPOR = EUPP/OA0
        DCOR = ED/OA0
        
        #ETP = EIP + ESPP + EUPP + 0.12*ED        
        CF.loc[t] = [MOB,
                    SBB,SP,SIP,SPP,
                    ESU,
                    EBB,
                    UCOR,ECU,ED,
                    EIP,ESPP,
                    UPOR,EPU,EUPP,
                    EEB,
                    SMM,CPR,
                    MDR,CDR,
                    DPOR,DCOR]
    
    #return CF, CF[['MOB','SMM']], CF[['MOB','CPR']], CF[['MOB','MDR']], CF[['MOB','CDR']], CF[['MOB','DPOR']], CF[['MOB','DCOR']]

    # Calculating Risk Measures
    SMM = CF[['MOB','SMM']]
    CPR = CF[['MOB','CPR']]
    MDR = CF[['MOB','MDR']]
    CDR = CF[['MOB','CDR']]
    DPOR = CF[['MOB','DPOR']]
    DCOR = CF[['MOB','DCOR']]
   
    P = max(CF.EBB)        
    T = len(CF)

    # Calculating Return MEasures

    # Adjust first interest payment for holding period
    CF.loc[CF.MOB==1,'EIP'] = (1-Holding_Days/30)*CF.loc[CF.MOB==1,'EIP'].values[0]

    # Collection Fees (pre Charge-Off)
    CF['ECF'] = CF.apply(lambda row: (Effective_Collection_Fee)*(row.EIP+row.ESPP+row.EUPP),axis=1)

    # Expected Recovery
    CF['ER'] = Recovery_Rate*CF.ED

    # Expected Recovery Fee
    CF['ERF'] = Recovery_Fee*CF.ER

    # Expected Service Fee
    # Waive fees on prepayment within the first year
    CF['ESF'] = CF.apply(lambda row: (Service_Fee_PI)*(row.EIP+row.ESPP+row.EUPP) + (Service_Fee_UPB/12)*row.EEB if row.MOB > 12 \
                                else (Service_Fee_PI)*(row.EIP+row.ESPP) + (Service_Fee_UPB/12)*row.EEB,axis=1)

    # Expected Bank (trailing) Fee
    CF['EWF'] = CF.apply(lambda row: (Bank_Fee)*(row.EIP+row.ESPP+row.EUPP),axis=1)

    CF['ETP'] = CF.EIP + CF.ESPP + CF.EUPP + CF.ER - CF.EWF - CF.ECF - CF.ERF - CF.ESF
    
    GCL  = sum(CF.ED)/P
    NCL = (1-Recovery_Rate)*GCL
    ACL = (12*sum(CF.ED-CF.ER)/T)/(sum(CF.EBB)/T)

    IRR = np.irr(np.append(-P,(CF.ETP)))*12
    YIELD = 12*(sum(CF.EIP - CF.ED + CF.ER - CF.EWF - CF.ECF - CF.ERF - CF.ESF)/T)/(sum(CF.EBB)/T)
    NAR = (1+sum(CF.EIP - CF.ED + CF.ER - CF.EWF - CF.ECF - CF.ERF - CF.ESF)/sum(CF.EBB))**12-1

    DURATION_MACAULY = np.npv(IRR/12,np.append(0,CF.ETP*CF.MOB/12))/np.npv(IRR/12,np.append(0,CF.ETP))
    DURATION_MODIFIED = DURATION_MACAULY/(1+IRR/12)

    DURATION = DURATION_MODIFIED
            
    return CF, SMM, CPR, MDR, CDR, DPOR, DCOR, GCL, NCL, ACL, IRR, YIELD, NAR, DURATION


#calculate_portfolio_irrs()