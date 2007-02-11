##parameters=datastructure, layout
# $Id$
"""Verify metadata information.

For now it only verify some dates.
"""

import DateTime

effective_date = datastructure['EffectiveDate']
expiration_date = datastructure['ExpirationDate']
creation_date = datastructure['CreationDate']

# Disabling this check since it's possible to create and publish documents after
# the effective date of the event. This happens when one creates documents to
# cover past events.
#
#if effective_date is not None and effective_date <= creation_date:
#    datastructure.setError('EffectiveDate', 'cpsschemas_err_bad_date')
#    return False

# It is useless to create an already expired document
if expiration_date is not None and expiration_date <= creation_date:
    datastructure.setError('ExpirationDate', 'cpsschemas_err_bad_date')
    return False

return True
