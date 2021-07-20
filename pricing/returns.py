import os
import pandas as pd
import numpy as np
import numpy_financial as npf

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

    IRR = npf.irr(np.append(-P,(CF.ETP)))*12
    YIELD = 12*(sum(CF.EIP - CF.ED + CF.ER - CF.EWF - CF.ECF - CF.ERF - CF.ESF)/T)/(sum(CF.EBB)/T)
    NAR = (1+sum(CF.EIP - CF.ED + CF.ER - CF.EWF - CF.ECF - CF.ERF - CF.ESF)/sum(CF.EBB))**12-1

    DURATION_MACAULY = npf.npv(IRR/12,np.append(0,CF.ETP*CF.MOB/12))/npf.npv(IRR/12,np.append(0,CF.ETP))
    DURATION_MODIFIED = DURATION_MACAULY/(1+IRR/12)

    DURATION = DURATION_MODIFIED

    results = dict()

    results['IRR'] = IRR
    # results['SMM'] = SMM

    # CF, SMM, CPR, MDR, CDR, DPOR, DCOR, GCL, NCL, ACL, IRR, YIELD, NAR, DURATION
    return results