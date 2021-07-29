from flask import request
from flask_restx import Resource
from api.restplus import api
from api.serializers import projecting_return_params
from pricing.returns import ProjectingReturn

projecting_return = api.namespace('api/projecting_return', description='Methods related to projecting returns')

@projecting_return.route('/')
class ProjectingReturnAPI(Resource):

    @api.expect(projecting_return_params, validation=True)

    def post(self):

        output = request.json
        Term = output['term']
        Interest_Rate = output['interest_rate']
        UPOR_Curve = list(map(float, output['upor_curve'].split(",")))
        UCOR_Curve = list(map(float, output['ucor_curve'].split(",")))
        Recovery_Rate = output['recovery_rate']
        Effective_Collection_Fee = output['effective_collection_fee']
        Recovery_Fee = output['recovery_fee']
        Holding_Days = output['holding_days']
        Service_Fee_PI = output['service_fee_pi']
        Service_Fee_UPB = output['service_fee_upb']
        Bank_Fee = output['bank_fee']

        # Term = 36
        # Interest_Rate = 7.2/100
        #         UPOR_Curve=[0.005,0.009,0.004,0.007,0.004,0.01,0.004,0.008,0.009,0.006,0.006,0.007,0.005,0.004,0.009,0.004,0.008,0.007,0.005,0.006,0.01,0.01,0.005,0.009,0.004,0.007,0.004,0.01,0.01,0.005,0.009,0.004,0.007,0.004,0.01,0.004] # Unit Paid-off Rate
        #         UCOR_Curve=[0,0,0.0018,0.0028,0.003,0.003,0.0028,0.0027,0.0025,0.0024,0.0022,0.0021,0.002,0.0019,0.0018,0.0017,0.0016,0.0015,0.0014,0.0014,0.0013,0.0012,0.0012,0.0011,0.0011,0.001,0.001,0.0009,0.0009,0.0009,0.0008,0.0008,0.0008,0.0007,0.0007,0.0007] # Unit Charge-off Rate
        # Recovery_Rate = .095
        # Effective_Collection_Fee = .0003
        # Recovery_Fee = .18
        # Holding_Days = 2.8
        # Service_Fee_PI = .01
        # Service_Fee_UPB = 0
        # Bank_Fee = 0

        results = ProjectingReturn(
            Term, # Term in months
            Interest_Rate, # Annual Interest Rate
            UPOR_Curve, # Unit Paid-off Rate
            UCOR_Curve, # Unit Charge-off Rate
            Recovery_Rate,
            Effective_Collection_Fee, # Pre Charge-Off Collection fee; expressed as percentage of all P&I payment (and not just payments from delinquent loans)
            Recovery_Fee, # Post Charge-Off Collection fee; e.g. 18%
            Holding_Days, # Number of holding days by issuing bank; e.g 2-5 days, average 2.8 days
            Service_Fee_PI, # P&I Based servicing fee; e.g. 1%
            Service_Fee_UPB,  # Principal-based servicing fee, Annualized; e.g. 1%
            Bank_Fee
        )

        return results
