from flask_restx import fields
from api.restplus import api

# Term = 36
# Interest_Rate = 7.2/100
# UPOR_Curve=[0.005,0.009,0.004,0.007,0.004,0.01,0.004,0.008,0.009,0.006,0.006,0.007,0.005,0.004,0.009,0.004,0.008,0.007,0.005,0.006,0.01,0.01,0.005,0.009,0.004,0.007,0.004,0.01,0.01,0.005,0.009,0.004,0.007,0.004,0.01,0.004] # Unit Paid-off Rate
# UCOR_Curve=[0,0,0.0018,0.0028,0.003,0.003,0.0028,0.0027,0.0025,0.0024,0.0022,0.0021,0.002,0.0019,0.0018,0.0017,0.0016,0.0015,0.0014,0.0014,0.0013,0.0012,0.0012,0.0011,0.0011,0.001,0.001,0.0009,0.0009,0.0009,0.0008,0.0008,0.0008,0.0007,0.0007,0.0007] # Unit Charge-off Rate
# Recovery_Rate = .095description=
# Effective_Collection_Fee = .0003
# Recovery_Fee = .18
# Holding_Days = 2.8
# Service_Fee_PI = .01
# Service_Fee_UPB = 0
# Bank_Fee = 0

projecting_return_params = api.model('return_params', {
    'term': fields.Integer(required=True, description='Term of the loan (upl: 24,36,60,80..)', example=36),
    'interest_rate': fields.Float(required=True, description='interest rate of the loan', example=.072),
    'upor_curve': fields.String(required=True, description='units paid off', example='0.005,0.009,0.004,0.007,0.004,0.01,0.004,0.008,0.009,0.006,0.006,0.007,0.005,0.004,0.009,0.004,0.008,0.007,0.005,0.006,0.01,0.01,0.005,0.009,0.004,0.007,0.004,0.01,0.01,0.005,0.009,0.004,0.007,0.004,0.01,0.004'),
    'ucor_curve': fields.String(required=True, description='units charged off', example='0,0,0.0018,0.0028,0.003,0.003,0.0028,0.0027,0.0025,0.0024,0.0022,0.0021,0.002,0.0019,0.0018,0.0017,0.0016,0.0015,0.0014,0.0014,0.0013,0.0012,0.0012,0.0011,0.0011,0.001,0.001,0.0009,0.0009,0.0009,0.0008,0.0008,0.0008,0.0007,0.0007,0.0007'),
    'recovery_rate': fields.Float(required=True, description='recovery rate', example=.095),
    'effective_collection_fee': fields.Float(required=True, description='effective collection fee', example=.0003),
    'recovery_fee': fields.Float(required=True, description='recovery fee', example=.18),
    'holding_days': fields.Float(required=True, description='holding days', example=2.8),
    'service_fee_pi': fields.Float(required=True, description='service fee on principal & interest', example=.01),
    'service_fee_upb': fields.Float(required=True, description='service fee on unpaid principal balance', example=0),
    'bank_fee': fields.Float(required=True, description='correspondent bank fee', example=0)
})
