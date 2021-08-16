#### Overview:
All loan-related yields, durations, convexities and holding-period returns should be calculated uniformly on a 
semiannual-compounding basis, regardless of the frequency of the actual cash flows used in computing these measures.


#### Ports open on:
```
EXPOSE 5000 - rest api - used for calling requests to container  
EXPOSE 8888 - jupyterlab - if code inside of the container should be modified while running (experimental)
EXPOSE 6379 - redis-server - redis server for tracking jobs and/or parallel requests
EXPOSE 9181 - rq-dashboard - redis dashboard to track jobs
```

#### Make sure ports are free:
```shell script
nc -z 127.0.0.1 8888 && echo "IN USE" || echo "FREE"
```

#### Build image on local:
```shell script
sh build_image_local.sh
```

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
			
#### Output:

| Calc | Results   |
|------|-----------|
|GCL   |0.039045534|
|NCL   |0.035336208|
|ACL   |0.024569544|

|Measure of Returns						                             | IRR	 | Yield  |  NAR |
|--------------------------------------------------------------------|-------|--------|------|
|- No Fees						                                     | 4.63% |	4.63% |	4.73%|
|- w/ Collection Fees						                         | 4.61% |  4.61% | 4.71%|
|- w/ Collection and Recovery Fees						             | 4.57% |  4.57% | 4.66%|
|- w/ Collection, Recovery Fees and Holding Period				     | 4.53% |  4.53% | 4.62%|
|- w/ Collection, Recovery Fees, Holding Period and Servicing Fees   | 3.85% |  3.83% | 3.90%|
|- w/ Collection, Recovery Fees, Holding, Servicing and Bank Fees	 | 3.70% |  3.69% |	3.75%|


|Effect of Fees on       |      IRR    |       Yield      |       NAR      |
|------------------------|-------------|------------------|----------------|
|- Collection Fee Effect | 0.000217775 |    0.000221722	  |   0.000231303  |
|- Recovery Fee Effect   | 0.000464199 |    0.000464242	  |   0.00048415   |
|- Holding Effect		 | 0.000401105 |    0.000384688	  |   0.000401028  |
|- Servicing Fee Effect	 | 0.006810343 |    0.006931017	  |   0.00720134   |
|- Bank Fee Effect		 | 0.001460195 |    0.00147738	  |   0.001529113  |

#### Terminology Legend:

| Acronym   | Definition                                                                |
|-----------|---------------------------------------------------------------------------|
|MOB      	| Month on Book   |	
|UPOR      	| Unit Paid-Off Rate   |	
|UCOR      	| Unit Charge-Off Rate   |	
|SBB      	| Scheduled Beginning Balance   |	
|SP      	| Scheduled (Contractual) Payment	= PMT(R/12,T,-P)   |
|SIP      	| Scheduled Interest Payment	= R/12*SBB   |
|SPP      	| Scheduled Principal Payment	= SP - SIP   |
|EBB      	| Expected Beginning (Performing) Balance	=EEB(MOB-1)   |
|ESU      	| Expected Surviving Units   |	
|EIP      	| Expected Interest Payment   |	
|ESPP      	| Expected Scheduled Principal Payment   |	
|EUPP      	| Expected Unscheduled Principal Payment (prepayment)   |	
|ED      	| Expected Default (Amount)   |	
|ER      	| Expected Recovery (Amount)   |	
|EWF      	| Expected WebBank Fees   |	
|ECF      	| Expected Collection Fees   |	
|ERF      	| Expected Recovery Fees   |	
|ESF      	| Expected Servicing Fees   |	
|ETP      	| Expected Total Payment	= EIP + ESPP + EUPP + ER - EWF - ECF - ERF - ESF   |
|EEB      	| Expected Ending (Performing) Balance	= EBB - (ED + ESPP + EUPP)   |
|EPU      	| Expected Paid-Off Units   |	
|DPOR      	| Dollar Paid-Off Rate   |	
|SMM      	| Single Monthly Mortality (Rate)   |	
|CPR      	| Conditional Prepayment Rate   |	
|ECU      	| Expected Charge-Off Units   |	
|DCOR      	| Dollar Charge-Off Rate   |	
|MDR      	| Monthly Default Rate   |	
|CDR      	| Conditional Default Rate   |	



