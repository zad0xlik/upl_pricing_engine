#### Inputs: 

| Inputs/Assumptions          | Values         |
| --------------------------- | -------------- |
| Term                        | 36             |
| Grade                       | C              |
| Interest Rate               | 14.17%         |
| Recovery Rate               | 9.50%          |
| Recovery Fee                | 18%            |
| Effective Collection Fee    | 0.12%          |
| Holding Days                | 2.8            |
| InterBank Fee               | 0.00%          |
| Servicing Fee (P&I)         | 1.00%          |
| Servicing Fee (UPB)         | 0.00%          |
			

Results											
			Measure of Returns…						IRR	"Yield"	NAR
GCL	9.51%		   - No Fees						7.40%	7.16%	7.40%
NCL	8.60%		  - w/ Collection Fees						7.30%	7.06%	7.29%
ACL	6.59%		  - w/ Collection and Recovery Fees						7.18%	6.93%	7.16%
			  - w/ Collection, Recovery Fees and Holding Period						7.08%	6.85%	7.07%
Duration	1.19		  - w/ Collection, Recovery Fees, Holding Period and Servicing Fees						6.35%	6.12%	6.29%
			  - w/ Collection, Recovery Fees, Holding, Servicing and WebBank Fees						6.35%	6.12%	6.29%


Effect of Fees on… 			IRR	"Yield"	NAR
  -  Collection Fee Effect			-0.10%	-0.10%	-0.11%
  -  Recovery Fee Effect			-0.12%	-0.12%	-0.13%
  -  Holding Effect			-0.09%	-0.08%	-0.09%
  -  Servicing Fee Effect			-0.74%	-0.73%	-0.78%
  - WebBank Fee Effect			0.00%	0.00%	0.00%


MOB	Month on Book	
UPOR	Unit Paid-Off Rate	
UCOR	Unit Charge-Off Rate	
SBB	Scheduled Beginning Balance	
SP	Scheduled (Contractual) Payment	= PMT(R/12,T,-P)
SIP	Scheduled Interest Payment	= R/12*SBB
SPP	Scheduled Principal Payment	= SP - SIP
EBB	Expected Beginning (Performing) Balance	=EEB(MOB-1)
ESU	Expected Surviving Units	
EIP	Expected Interest Payment	
ESPP	Expected Scheduled Principal Payment	
EUPP	Expected Unscheduled Principal Payment (prepayment)	
ED	Expected Default (Amount)	
ER	Expected Recovery (Amount)	
EWF	Expected WebBank Fees	
ECF	Expected Collection Fees	
ERF	Expected Recovery Fees	
ESF	Expected Servicing Fees	
ETP	Expected Total Payment	= EIP + ESPP + EUPP + ER - EWF - ECF - ERF - ESF
EEB	Expected Ending (Performing) Balance	= EBB - (ED + ESPP + EUPP)
EPU	Expected Paid-Off Units	
DPOR	Dollar Paid-Off Rate	
SMM	Single Monthly Mortality (Rate)	
CPR	Conditional Prepayment Rate	
ECU	Expected Charge-Off Units	
DCOR	Dollar Charge-Off Rate	
MDR	Monthly Default Rate	
CDR	Conditional Default Rate	


     Select Curves:		Risk	Projected Cash Flows																								
			Scheduled (Original Balance = 100)				Expected (Original Balance = 10,000)													Pre-Payment				Charge-Off			
MOB	UPOR	UCOR	SBB	SP	SIP	SPP	EBB	ESU	EIP	ESPP	EUPP	ED	ER	EWF	ECF	ERF	ESF	ETP	EEB	EPU	DPOR	SMM	CPR	ECU	DCOR	MDR	CDR

##data rates

PRODUCT	TERM	GRADE	INTEREST_RATE	VOLUME	LOSS MULTIPLIER	PREPAY MULTIPLIER
Prime	36	A	0.0697	0.1420	1	1


##data estimates
TERM	GRADE	MOB	UCOR	UPOR
36	A	1	0.0000	0.0079



