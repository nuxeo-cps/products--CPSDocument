##parameters=datastructure, layout
# verifying dates integrity
import DateTime
effective_date = datastructure['EffectiveDate']
expiration_date = datastructure['ExpirationDate']
creation_date = datastructure['CreationDate']

"""
XXXX need to fix effective_date algo that does not manage seconds
  ie : effective_date CAN be < to creation_date at 1 minute

if effective_date is not None and effective_date <= (creation_date):
    datastructure.setError('EffectiveDate', 'cpsschemas_err_bad_date')
    return 0
else
"""
if expiration_date is not None and expiration_date <= creation_date:
    datastructure.setError('ExpirationDate', 'cpsschemas_err_bad_date')
    return 0
return 1
